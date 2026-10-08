import test from 'node:test';
import assert from 'node:assert/strict';
import { cleanCampaign, cleanEvent, createMeasurement } from './measurement.mjs';
test('não transmite e-mail, telefone, mensagens, nomes ou valores arbitrários de URL', () => {
  assert.deepEqual(cleanCampaign('?utm_source=instagram&utm_campaign=ana@example.com&email=private@example.com'), { utm_source: 'instagram' });
  assert.deepEqual(cleanEvent('whatsapp_click', { placement: 'cart', name: 'Ana', phone: '31999999999', message: 'Contato privado', email: 'ana@example.com' }), { name: 'whatsapp_click', data: { placement: 'cart' } });
});
test('não contabiliza clique como compra ou cadastro concluído', () => {
  assert.equal(cleanEvent('purchase', { value: 49.90 }), null);
  assert.equal(cleanEvent('generate_lead', {}), null);
});
test('não carrega tag sem ID ou sem consentimento; revogação interrompe eventos', () => {
  const scripts = [], win = { location: { origin: 'https://bordopersonalizados.com.br', pathname: '/', search: '?email=private@example.com&utm_source=instagram' } };
  const doc = { createElement: () => ({}), head: { appendChild: value => scripts.push(value) } };
  const empty = createMeasurement({ win, doc });
  empty.consent(true);
  assert.equal(scripts.length, 0);
  const measurement = createMeasurement({ measurementId: 'G-TEST123', win, doc });
  assert.equal(measurement.track('view_cart'), false);
  measurement.consent(false);
  assert.equal(scripts.length, 0);
  measurement.consent(true);
  assert.equal(scripts.length, 1);
  assert.equal(measurement.track('view_cart'), true);
  assert.equal(win.dataLayer.some(args => JSON.stringify(args).includes('private@example.com')), false);
  measurement.consent(false);
  assert.equal(measurement.track('view_cart'), false);
  assert.equal(win['ga-disable-G-TEST123'], true);
  measurement.consent(true);
  assert.equal(scripts.length, 1);
});
