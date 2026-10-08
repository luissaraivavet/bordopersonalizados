import test from 'node:test';
import assert from 'node:assert/strict';
import { buildQuote, normalizeServices, handleRequest } from './worker.mjs';
const catalog = { settings: { giftPrice: 15 }, collections: [{ id: 'jardim', published: true }], products: [{ id: 'daisy', collection: 'jardim', published: true, price: 49.90, options: ['Presilha'] }] };
const env = { ORIGIN_POSTAL_CODE: '36580000', SHIPMENT_PROFILES: JSON.stringify({ daisy: { width: 20, height: 5, length: 30, weight: 0.2 } }) };
const input = { postalCode: '01001-000', items: [{ id: 'daisy', variation: 'Presilha', qty: 2, price: 0.01, weight: 0.001 }] };
test('cotação usa medidas e preço do servidor, não do visitante', () => {
  const quote = buildQuote(input, env, catalog);
  assert.equal(quote.products[0].insurance_value, 49.90);
  assert.equal(quote.products[0].weight, 0.2);
  assert.equal(quote.products[0].quantity, 2);
  assert.equal(quote.from.postal_code, '36580000');
  assert.equal(quote.to.postal_code, '01001000');
});
test('recusa CEP, quantidade, opção e produto inválidos', () => {
  for (const change of [{ postalCode: 'abc' }, { items: [{ ...input.items[0], qty: 1.5 }] }, { items: [{ ...input.items[0], variation: 'Elástico' }] }, { items: [{ ...input.items[0], id: 'inexistente' }] }, { gift: 'false' }]) assert.throws(() => buildQuote({ ...input, ...change }, env, catalog));
});
test('não inventa dimensões para produto ou embalagem de presente', () => {
  assert.throws(() => buildQuote(input, { ...env, SHIPMENT_PROFILES: '{}' }, catalog));
  assert.throws(() => buildQuote({ ...input, gift: true }, env, catalog));
});
test('agrega linhas da mesma peça e impede mais de 99 unidades', () => {
  assert.equal(buildQuote({ ...input, items: [input.items[0], input.items[0]] }, env, catalog).products[0].quantity, 4);
  assert.throws(() => buildQuote({ ...input, items: [{ ...input.items[0], qty: 99 }, input.items[0]] }, env, catalog));
});
test('usa customizações e elimina fretes indisponíveis ou malformados', () => {
  const services = normalizeServices([{ id: 1, price: '30', custom_price: '20', delivery_time: 5, custom_delivery_time: 7 }, { id: 2, price: '10', delivery_time: 3 }, { id: 3, price: null, delivery_time: 3 }, { id: 4, price: 1, delivery_time: 3, error: 'Indisponível' }]);
  assert.deepEqual(services.map(s => [s.id, s.price, s.transitDays]), [['2', 10, 3], ['1', 20, 7]]);
});
test('origem indevida e configuração incompleta não chamam provedor', async () => {
  const fakeFetch = () => { throw new Error('Não deveria consultar o provedor'); };
  assert.equal((await handleRequest(new Request('https://worker.example/shipping/quote', { method: 'POST', headers: { Origin: 'https://malicious.example' } }), {}, fakeFetch)).status, 403);
  const response = await handleRequest(new Request('https://worker.example/shipping/quote', { method: 'POST', headers: { Origin: 'https://bordopersonalizados.com.br' } }), {}, fakeFetch);
  assert.equal(response.status, 503);
  assert.equal(response.headers.get('Access-Control-Allow-Origin'), 'https://bordopersonalizados.com.br');
});
test('limite de consultas bloqueia sem chamar provedor', async () => {
  const response = await handleRequest(new Request('https://worker.example/shipping/quote', { method: 'POST', headers: { Origin: 'https://bordopersonalizados.com.br' } }), { MELHOR_ENVIO_ENVIRONMENT: 'sandbox', MELHOR_ENVIO_TOKEN: 'test', MELHOR_ENVIO_CONTACT: 'test@example.com', QUOTE_LIMITER: { limit: async () => ({ success: false }) } }, () => { throw new Error('Não consultar'); });
  assert.equal(response.status, 429);
});
