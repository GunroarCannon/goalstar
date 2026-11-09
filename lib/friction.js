// Turns Walrus memories into route costs.
//
// Walrus decides which memories are about a step (semantic distance from recall).
// This module decides what each one says about it: a blocker raises the step's cost
// according to how bad it was, a win lowers it, and anything else leaves it alone.

export const MAX_PENALTY = 4;
export const MAX_DISCOUNT = 1;

// Cosine distance from the relayer. At or below NEAR a memory is squarely about the
// step; at or beyond FAR it is unrelated. On real mainnet recalls, matching steps
// landed between 0.33 and 0.59 and unrelated goals at 0.74 or more.
export const NEAR = 0.5;
export const FAR = 0.68;

const RECALL_LIMIT = 8;
const HALF_LIFE_DAYS = 30;
const CACHE_MS = 60 * 1000;
const CONCURRENCY = 3;

const BLOCKER = /\b(block(?:ed|er|ers|ing)?|stuck|stall(?:ed|s|ing)?|fail(?:ed|s|ure|ures|ing)?|broke|broken|breaks?|breaking|crash(?:ed|es|ing)?|bottlenecks?|regressions?|exhaust(?:ed|ing)|burn(?:ed|t)?[ -]?out|overwhelm(?:ed|ing)|frustrat(?:ed|ing)|fighting|struggl(?:e|ed|ing)|abandon(?:ed)?|delays?|delayed|procrastinat\w*|wasted?|lost|can'?t|cannot|unable|anxiety|dropoff|time sink|painful|nightmare|underestimat\w*|leaks?|friction|404|injury)\b/gi;
const SEVERE = /\b(exhaust(?:ed|ing)|burn(?:ed|t)?[ -]?out|overwhelm(?:ed|ing)|abandon(?:ed)?|severe|stalled|nightmare|injury|can'?t|cannot|repeated(?:ly)?|consistently)\b/i;
const WIN = /\b(worked|works|smooth(?:ly)?|easy|easily|painless|fast(?:er)?|quick(?:ly)?|finished|completed|shipped|solved|victory|success(?:ful|fully)?|passed|peaks?)\b/gi;
const NEGATED = /\b(?:no|not|never|without|zero|isn'?t|wasn'?t|didn'?t|doesn'?t)\s+(?:\w+\s+)?/gi;
const CLAUSE_SPLIT = /(?<=[a-z0-9)'"])[.;:]\s+|,?\s+(?:but|whereas|however|though)\s+/i;
const STOPWORDS = new Set('a an and are as at be by for from in into is it its of on or our so that the their them then this to up was we were will with your you user'.split(' '));

const stem = (w) => w.replace(/(ing|ers|er|ed|es|s)$/, '');

function tokens(text) {
  return new Set(
    String(text).toLowerCase().match(/[a-z0-9]+/g)?.filter((w) => w.length > 1 && !STOPWORDS.has(w)).map(stem) || [],
  );
}

function countMatches(text, pattern) {
  return (text.match(pattern) || []).length;
}

function hoursLost(text) {
  let hours = 0;
  for (const [, n, unit] of text.matchAll(/(\d+(?:\.\d+)?)\s*-?\s*(hours?|hrs?|days?|weeks?)\b/gi)) {
    const scale = /^h/i.test(unit) ? 1 : /^d/i.test(unit) ? 8 : 40;
    hours = Math.max(hours, Number(n) * scale);
  }
  return hours;
}

function readClause(raw) {
  // "When a task stalls, split it" is a rule, not a report of something going wrong.
  if (/^s*(when|if|whenever)/i.test(raw)) return { kind: 'neutral', severity: 0, hoursLost: 0 };
  // "never block a request" and "no blockers" are not complaints.
  const clause = raw.replace(new RegExp(NEGATED.source + BLOCKER.source, 'gi'), ' ');
  const blockers = countMatches(clause, BLOCKER);
  const wins = countMatches(clause, WIN);
  if (blockers > wins) {
    const lost = hoursLost(clause);
    const severity = 0.5 + Math.min(0.3, lost * 0.03) + (SEVERE.test(clause) ? 0.2 : 0) + Math.min(0.1, (blockers - 1) * 0.05);
    return { kind: 'blocker', severity: Math.min(1, severity), hoursLost: lost };
  }
  if (wins > blockers) return { kind: 'win', severity: Math.min(1, 0.5 + wins * 0.15), hoursLost: 0 };
  return { kind: 'neutral', severity: 0, hoursLost: 0 };
}

// What a memory says about a step. A memory can blame one thing and praise another
// ("Docker failed; PaaS worked"), so the clause naming the step wins when one does.
export function assessMemory(text, label = '') {
  const body = String(text).replace(/^\s*\[[^\]]*\]\s*/, '').replace(/^NOTE on "[^"]*":\s*/i, '');
  const clauses = body.split(CLAUSE_SPLIT).filter(Boolean);
  const wanted = tokens(label);
  const read = clauses.map((clause) => {
    const words = tokens(clause);
    return { ...readClause(clause), overlap: [...wanted].filter((w) => words.has(w)).length };
  });

  const named = read.filter((c) => c.overlap > 0 && c.kind !== 'neutral');
  if (named.length) {
    const top = Math.max(...named.map((c) => c.overlap));
    const best = named.filter((c) => c.overlap === top).sort((a, b) => (a.kind === 'blocker' ? -1 : 1) - (b.kind === 'blocker' ? -1 : 1))[0];
    return { kind: best.kind, severity: best.severity, hoursLost: best.hoursLost, mixed: false };
  }

  const blockers = read.filter((c) => c.kind === 'blocker');
  const wins = read.filter((c) => c.kind === 'win');
  if (blockers.length) {
    const worst = blockers.sort((a, b) => b.severity - a.severity)[0];
    return { kind: 'blocker', severity: worst.severity, hoursLost: worst.hoursLost, mixed: wins.length > 0 };
  }
  if (wins.length) return { kind: 'win', severity: wins[0].severity, hoursLost: 0, mixed: false };
  return { kind: 'neutral', severity: 0, hoursLost: 0, mixed: false };
}

export function relevance(distance) {
  return Math.max(0, Math.min(1, (FAR - distance) / (FAR - NEAR)));
}

function recencyWeight(createdAt, now) {
  const at = Date.parse(createdAt);
  if (!Number.isFinite(at)) return 0.75;
  const ageDays = Math.max(0, (now - at) / 86400000);
  return 0.5 + 0.5 * Math.pow(2, -ageDays / HALF_LIFE_DAYS);
}

const isDocument = (text) => /^\s*\[BLOB /.test(String(text));
const round = (n) => Math.round(n * 10) / 10;

// The cost change for one step, given the memories Walrus recalled for it.
export function scoreStep(label, hits, now = Date.now()) {
  let blocker = null;
  let win = null;

  for (const hit of hits) {
    if (isDocument(hit.text)) continue;
    const r = relevance(hit.distance);
    if (r <= 0) continue;
    const read = assessMemory(hit.text, label);
    if (read.kind === 'neutral') continue;
    const weight = read.severity * r * recencyWeight(hit.created_at, now) * (read.mixed ? 0.5 : 1);
    const scored = { ...read, weight, hit };
    if (read.kind === 'blocker' && (!blocker || weight > blocker.weight)) blocker = scored;
    if (read.kind === 'win' && (!win || weight > win.weight)) win = scored;
  }

  let penalty = 0;
  let cause = null;
  if (blocker) {
    // A newer success counts only if it is at least as much about this step as the
    // blocker was: moving to gRPC working out says nothing good about JSON-RPC.
    const overcome = win && win.hit.distance <= blocker.hit.distance && Date.parse(win.hit.created_at) > Date.parse(blocker.hit.created_at) ? win.weight : 0;
    penalty = MAX_PENALTY * blocker.weight * (1 - overcome);
    cause = blocker;
  } else if (win) {
    penalty = -MAX_DISCOUNT * win.weight;
    cause = win;
  }

  penalty = round(penalty);
  if (Math.abs(penalty) < 0.2 || !cause) return { penalty: 0, because: null };
  return {
    penalty,
    because: {
      kind: cause.kind,
      text: cause.hit.text,
      blob: cause.hit.blob_id,
      at: cause.hit.created_at || null,
      distance: round(cause.hit.distance * 100) / 100,
      hoursLost: cause.hoursLost || 0,
      sample: !!cause.hit.sample,
    },
  };
}

// ---- Walrus lookups ----
const cache = new Map();

export function forgetCachedFriction() {
  cache.clear();
}

async function recallForStep(mw, label, namespace, expected) {
  const known = expected?.(namespace);
  if (known === 0) return [];
  const want = Math.min(RECALL_LIMIT, known ?? RECALL_LIMIT);
  let response = await mw.recall({ query: label, limit: RECALL_LIMIT, namespace });
  // A cold relayer can answer with only part of the namespace; ask again once.
  if (response.results.length < want) {
    response = await mw.recall({ query: label, limit: RECALL_LIMIT, namespace });
  }
  return response.results;
}

export async function frictionForSteps(mw, labels, namespaces, { fresh = false, expected = null, sampleNamespace = null } = {}) {
  const scopes = [namespaces].flat();
  const queue = [...new Set(labels)];
  const out = {};
  const now = Date.now();

  async function worker() {
    while (queue.length) {
      const label = queue.shift();
      const key = `${scopes.join(',')}|${label}`;
      const cached = cache.get(key);
      if (!fresh && cached && now - cached.at < CACHE_MS) {
        out[label] = cached.value;
        continue;
      }
      const found = await Promise.all(scopes.map(async (ns) => {
        const hits = await recallForStep(mw, label, ns, expected);
        return hits.map((hit) => ({ ...hit, sample: ns === sampleNamespace }));
      }));
      const value = scoreStep(label, found.flat(), now);
      cache.set(key, { at: now, value });
      out[label] = value;
    }
  }

  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  return out;
}
