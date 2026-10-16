// Local model via Ollama (https://ollama.com) — fully offline once a model is pulled.
// The hosted site must be allowed by Ollama's CORS check: set OLLAMA_ORIGINS (see README).
import { RESULT_SCHEMA, SYSTEM_PROMPT, buildUserPrompt } from './protocol.js';

export default {
  id: 'ollama',
  name: 'Ollama',
  async generate(req, p) {
    const base = (p.endpoint || 'http://localhost:11434').replace(/\/+$/, '');
    let res;
    try {
      res = await fetch(`${base}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: p.model || 'llama3.1',
          stream: false,
          format: RESULT_SCHEMA,
          messages: [
            { role: 'system', content: SYSTEM_PROMPT },
            { role: 'user', content: buildUserPrompt(req) },
          ],
        }),
      });
    } catch {
      throw new Error(`Can't reach Ollama at ${base} (running? OLLAMA_ORIGINS set?)`);
    }
    if (!res.ok) throw new Error(`Ollama ${res.status}: ${(await res.text()).slice(0, 200)}`);
    const j = await res.json();
    return JSON.parse(j.message?.content || '{}');
  },
};
