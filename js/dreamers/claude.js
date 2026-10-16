// Claude dreamer. The SDK is loaded from a CDN only when this dreamer is used,
// so the rest of the app works fully offline.
import { RESULT_SCHEMA, SYSTEM_PROMPT, buildUserPrompt } from './protocol.js';

const SDK_URL = 'https://cdn.jsdelivr.net/npm/@anthropic-ai/sdk@0.130.0/+esm';
let sdk = null;

export default {
  id: 'claude',
  name: 'Claude',
  async generate(req, p) {
    if (!p.apiKey) throw new Error('No Claude API key (Settings → Dreamer)');
    sdk ||= await import(SDK_URL);
    const Anthropic = sdk.default;
    // Personal, self-hosted use: the key lives only in this browser's localStorage.
    const client = new Anthropic({ apiKey: p.apiKey, dangerouslyAllowBrowser: true });

    const body = {
      model: p.model || 'claude-opus-5-5',
      max_tokens: 16000,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: buildUserPrompt(req) }],
      output_config: {
        effort: p.effort || 'medium',
        format: { type: 'json_schema', schema: RESULT_SCHEMA },
      },
    };

    let res;
    if (p.refusalFallback) {
      try {
        // If a safety classifier declines, the API retries on Anthropic's recommended fallback model.
        res = await client.beta.messages.create({ ...body, fallbacks: 'default', betas: ['server-side-fallback-2026-07-01'] });
      } catch (err) {
        if (!(err instanceof Anthropic.BadRequestError)) throw err;
        res = await client.messages.create(body);
      }
    } else {
      res = await client.messages.create(body);
    }

    if (res.stop_reason === 'refusal') {
      throw new Error(`Claude declined${res.stop_details?.explanation ? ': ' + res.stop_details.explanation : ''}`);
    }
    if (res.stop_reason === 'max_tokens') throw new Error('Response was cut off (max_tokens)');
    const text = res.content.filter((b) => b.type === 'text').map((b) => b.text).join('');
    return JSON.parse(text);
  },
};
