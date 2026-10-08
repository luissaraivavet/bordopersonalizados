import catalog from '../../content/site.json' with { type: 'json' };

const origins = new Set(['https://bordopersonalizados.com.br', 'https://www.bordopersonalizados.com.br']);
class QuoteError extends Error {
  constructor(message, status = 400) { super(message); this.status = status; }
}
function cep(value) {
  if (typeof value !== 'string' || !/^\d{5}-?\d{3}$/.test(value)) throw new QuoteError('Informe um CEP válido.');
  return value.replace('-', '');
}
export function buildQuote(input, env, source = catalog) {
  const destination = cep(input?.postalCode);
  if (!Array.isArray(input.items) || !input.items.length || input.items.length > 50) throw new QuoteError('Revise os itens da sacola.');
  let profiles;
  try { profiles = JSON.parse(env.SHIPMENT_PROFILES || '{}'); } catch { throw new QuoteError('Frete temporariamente indisponível.', 503); }
  const lines = new Map();
  let units = 0;
  for (const item of input.items) {
    if (!item || typeof item.id !== 'string' || !Number.isInteger(item.qty) || item.qty < 1 || item.qty > 99) throw new QuoteError('Revise as quantidades.');
    const product = source.products.find(p => p.id === item.id && p.published && source.collections.some(c => c.id === p.collection && c.published));
    if (!product || !Number.isFinite(product.price) || product.price <= 0 || !product.options.includes(item.variation)) throw new QuoteError('Uma peça precisa de confirmação pelo atendimento.');
    const profile = profiles[item.id];
    if (!profile || ['width', 'height', 'length', 'weight'].some(key => !Number.isFinite(profile[key]) || profile[key] <= 0)) throw new QuoteError('Precisamos confirmar a embalagem desta peça. Consulte a Bordô.', 422);
    units += item.qty;
    if (units > 99) throw new QuoteError('Para este volume, consulte a Bordô.');
    const previous = lines.get(item.id);
    lines.set(item.id, { id: product.id, width: profile.width, height: profile.height, length: profile.length, weight: profile.weight, insurance_value: product.price, quantity: (previous?.quantity || 0) + item.qty });
  }
  if (input.gift !== undefined && typeof input.gift !== 'boolean') throw new QuoteError('Revise a embalagem.');
  if (input.gift) {
    const profile = profiles['gift-packaging'];
    if (!profile || ['width', 'height', 'length', 'weight'].some(key => !Number.isFinite(profile[key]) || profile[key] <= 0)) throw new QuoteError('Precisamos confirmar a embalagem para presente.', 422);
    lines.set('gift-packaging', { id: 'gift-packaging', width: profile.width, height: profile.height, length: profile.length, weight: profile.weight, insurance_value: source.settings.giftPrice, quantity: 1 });
  }
  return { from: { postal_code: cep(env.ORIGIN_POSTAL_CODE) }, to: { postal_code: destination }, products: [...lines.values()], options: { receipt: false, own_hand: false } };
}
export function normalizeServices(data) {
  if (!Array.isArray(data)) throw new QuoteError('Não foi possível consultar o frete.', 502);
  return data.flatMap(service => {
    const rawPrice = service.custom_price ?? service.price;
    const rawDays = service.custom_delivery_time ?? service.delivery_time;
    if (service.error || rawPrice === null || rawPrice === '' || rawDays === null || rawDays === '' || rawPrice === undefined || rawDays === undefined) return [];
    const price = Number(rawPrice), transitDays = Number(rawDays);
    if (!Number.isFinite(price) || price <= 0 || !Number.isInteger(transitDays) || transitDays < 0 || service.id === undefined) return [];
    return [{ id: String(service.id), name: String(service.name || ''), company: String(service.company?.name || ''), price, transitDays }];
  }).sort((a, b) => a.price - b.price);
}
export async function handleRequest(request, env, fetcher = fetch) {
  const origin = request.headers.get('Origin');
  const headers = { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', Vary: 'Origin' };
  if (origins.has(origin)) headers['Access-Control-Allow-Origin'] = origin;
  const reply = (body, status = 200) => new Response(JSON.stringify(body), { status, headers });
  if (!origins.has(origin)) return reply({ error: 'Origem não permitida.' }, 403);
  if (new URL(request.url).pathname !== '/shipping/quote') return reply({ error: 'Recurso não encontrado.' }, 404);
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: { ...headers, 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' } });
  if (request.method !== 'POST') return reply({ error: 'Método não permitido.' }, 405);
  try {
    // The limiter is a platform binding, not an in-memory counter. Fail closed until configured.
    if (!env.QUOTE_LIMITER || !env.MELHOR_ENVIO_TOKEN || !env.MELHOR_ENVIO_CONTACT || !['sandbox', 'production'].includes(env.MELHOR_ENVIO_ENVIRONMENT)) throw new QuoteError('Cotação ainda não ativada. Consulte a Bordô.', 503);
    const limit = await env.QUOTE_LIMITER.limit({ key: request.headers.get('CF-Connecting-IP') || 'unknown' });
    if (!limit.success) return reply({ error: 'Aguarde um pouco antes de consultar novamente.' }, 429);
    if (!(request.headers.get('Content-Type') || '').startsWith('application/json')) throw new QuoteError('Formato inválido.', 415);
    const text = await request.text();
    if (text.length > 16000) throw new QuoteError('Sacola muito grande.', 413);
    let input;
    try { input = JSON.parse(text); } catch { throw new QuoteError('Dados inválidos.'); }
    const body = buildQuote(input, env);
    const host = env.MELHOR_ENVIO_ENVIRONMENT === 'sandbox' ? 'sandbox.melhorenvio.com.br' : 'www.melhorenvio.com.br';
    const response = await fetcher(`https://${host}/api/v2/me/shipment/calculate`, { method: 'POST', headers: { Authorization: `Bearer ${env.MELHOR_ENVIO_TOKEN}`, Accept: 'application/json', 'Content-Type': 'application/json', 'User-Agent': `BordoFretes (${env.MELHOR_ENVIO_CONTACT})` }, body: JSON.stringify(body), signal: AbortSignal.timeout(12000) });
    if (!response.ok) throw new QuoteError('Não foi possível consultar o frete agora. Tente novamente ou fale com a Bordô.', 502);
    const services = normalizeServices(await response.json());
    return reply({ services, sandbox: env.MELHOR_ENVIO_ENVIRONMENT === 'sandbox', note: 'Prazo de transporte estimado em dias úteis após a postagem. Produção e preparação são confirmadas separadamente.' });
  } catch (error) {
    return reply({ error: error instanceof QuoteError ? error.message : 'Frete temporariamente indisponível.' }, error instanceof QuoteError ? error.status : 502);
  }
}
export default { fetch(request, env) { return handleRequest(request, env); } };
