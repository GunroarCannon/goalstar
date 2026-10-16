// Bring-your-own dreamer: POSTs the request to any URL (a local script, a
// serverless function, n8n, another LLM…) and expects the result JSON back.
import { RESULT_SCHEMA } from './protocol.js';

export default {
  id: 'webhook',
  name: 'Webhook',
  async generate(req, p) {
    if (!p.url) throw new Error('No webhook URL (Settings → Dreamer)');
    let extra = {};
    if (p.headers?.trim()) {
      try { extra = JSON.parse(p.headers); } catch { throw new Error('Webhook headers must be a JSON object'); }
    }
    const res = await fetch(p.url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...extra },
      body: JSON.stringify({ request: req, schema: RESULT_SCHEMA }),
    });
    if (!res.ok) throw new Error(`Webhook ${res.status}: ${(await res.text()).slice(0, 200)}`);
    return res.json();
  },
};
