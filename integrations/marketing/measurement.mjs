// Preparation only: attach to the storefront after account IDs and consent UI are verified.
const eventNames = new Set(['view_collection', 'view_item', 'add_to_cart', 'view_cart', 'whatsapp_click', 'lead_signup_click']);
const campaignKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'];
const allowedCampaignValues = new Set(['instagram', 'whatsapp', 'facebook', 'organic_social', 'referral', 'social', 'bordo_lancamento', 'story_jardim', 'reel_sinfonia', 'bio', 'presente', 'atelier']);

export function cleanCampaign(search) {
  const params = new URLSearchParams(search), result = {};
  for (const key of campaignKeys) {
    const value = params.get(key);
    if (allowedCampaignValues.has(value)) result[key] = value;
  }
  return result;
}
export function cleanEvent(name, data = {}) {
  if (!eventNames.has(name)) return null;
  const result = {};
  for (const key of ['item_id', 'collection_id']) if (typeof data[key] === 'string' && /^[a-z0-9-]{1,60}$/.test(data[key])) result[key] = data[key];
  if (Number.isInteger(data.quantity) && data.quantity > 0 && data.quantity <= 99) result.quantity = data.quantity;
  if (Number.isFinite(data.value) && data.value >= 0 && data.value <= 100000) { result.value = data.value; result.currency = 'BRL'; }
  if (['product', 'cart', 'custom', 'footer', 'newsletter'].includes(data.placement)) result.placement = data.placement;
  return { name, data: result };
}
export function createMeasurement({ measurementId = '', win = window, doc = document } = {}) {
  let enabled = false, loaded = false;
  const validId = /^G-[A-Z0-9]+$/.test(measurementId);
  function gtag() { win.dataLayer.push(arguments); }
  function consent(granted) {
    enabled = granted === true && validId;
    if (!loaded && !enabled) return;
    win.dataLayer = win.dataLayer || [];
    win.gtag = gtag;
    win[`ga-disable-${measurementId}`] = !enabled;
    const values = { analytics_storage: enabled ? 'granted' : 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' };
    gtag('consent', loaded ? 'update' : 'default', values);
    if (loaded) return;
    loaded = true;
    const script = doc.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    doc.head.appendChild(script);
    gtag('js', new Date());
    // Disable automatic collection: never send URL query strings or free text from the site.
    gtag('config', measurementId, { send_page_view: false, allow_google_signals: false, allow_ad_personalization_signals: false, page_location: `${win.location.origin}${win.location.pathname}`, page_referrer: '' });
    gtag('event', 'page_view', { page_location: `${win.location.origin}${win.location.pathname}`, page_title: 'Bordô | Laços e bordados personalizados', page_referrer: '', ...cleanCampaign(win.location.search) });
  }
  function track(name, data) {
    const event = cleanEvent(name, data);
    if (!enabled || !event) return false;
    gtag('event', event.name, event.data);
    return true;
  }
  return { consent, track };
}
