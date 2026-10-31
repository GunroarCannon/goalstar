// Groq (https://console.groq.com) — fast hosted open models with a free tier.
// Uses JSON mode; the schema is spelled out in the prompt so small models follow it.
import { RESULT_SCHEMA, SYSTEM_PROMPT, buildUserPrompt } from './protocol.js';

const SHAPE = `Reply with ONLY a JSON object of this exact shape (no prose, no markdown):
{"states":[{"key":"s1","label":"...","note":"...","h":12}],
 "actions":[{"from":"START","to":"s1","label":"...","note":"...","time":3,"money":1,"effort":4,"risk":2,"duration":"2–3 weeks","steps":["...","..."]}]}
JSON Schema: ${JSON.stringify(RESULT_SCHEMA)}`;

// No key baked into the bundle: with no personal key the request goes through
// this project's server, which reads GROQ_API_KEY from its own .env.

export default {
  id: 'groq',
  name: 'Groq',
  async generate(req, p) {
    const apiKey = p.apiKey || '';
    const model = p.model || 'openai/gpt-oss-120b';
    const endpoint = apiKey ? 'https://api.groq.com/openai/v1/chat/completions' : '/api/llm/groq';
    // Free tier is rate-limited per minute: wait as long as Groq asks, a few times.
    for (let attempt = 0; ; attempt++) {
      let res;
      try {
        res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}) },
          body: JSON.stringify({
            model,
            temperature: 0.6,
            max_completion_tokens: 8192,
            ...(model.startsWith('openai/gpt-oss') ? { reasoning_effort: 'low' } : {}),
            response_format: { type: 'json_object' },
            messages: [
              { role: 'system', content: `${SYSTEM_PROMPT}\n\n${SHAPE}` },
              { role: 'user', content: buildUserPrompt(req) },
            ],
          }),
        });
      } catch {
        throw new Error("Can't reach Groq (offline?)");
      }
      if (res.status === 429 && attempt < 3) {
        const wait = Number(res.headers.get('retry-after')) || 5;
        await new Promise((r) => setTimeout(r, Math.min(30, wait + 0.5) * 1000));
        continue;
      }
      if (!res.ok) {
        let msg = `${res.status}`;
        try {
          msg += ` ${(await res.json()).error?.message || ''}`;
        } catch {
          /* keep status */
        }
        throw new Error(`Groq ${msg.trim()}`);
      }
      const j = await res.json();
      return JSON.parse(j.choices?.[0]?.message?.content || '{}');
    }
  },
};
