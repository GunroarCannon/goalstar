// Dreamer registry. To add your own, write a module that exports
// { id, name, async generate(request, params) } and add it to this list.
import offline from './offline.js';
import groq from './groq.js';
import claude from './claude.js';
import ollama from './ollama.js';
import webhook from './webhook.js';
import { normalize } from './protocol.js';

export const dreamers = { offline, groq, claude, ollama, webhook };

export async function generate(settings, req) {
  const d = dreamers[settings.dreamer] || offline;
  try {
    const result = normalize(await d.generate(req, settings[d.id] || {}));
    if (!result.actions.length) throw new Error(`${d.name} returned no actions`);
    return { result, by: d.name };
  } catch (err) {
    if (d === offline || !settings.fallbackOffline) throw err;
    const result = normalize(await offline.generate(req, {}));
    return { result, by: 'Offline', warning: `${d.name} failed (${err.message}) — used offline dreamer` };
  }
}
