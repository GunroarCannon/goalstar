// Data model + local persistence for goalstar.
// A board is one goal: a graph of STATES (nodes) joined by ACTIONS (edges).

export const uid = (p = 'n') => `${p}_${Math.random().toString(36).slice(2, 9)}`;
export const now = () => Date.now();

const KEY = 'goalstar.v1';

export const DEFAULT_SETTINGS = {
  dreamer: 'offline',          // offline | groq | claude | ollama | webhook
  fallbackOffline: true,       // use the built-in dreamer when the chosen one fails
  maxStates: 8,                // roughly how many states a full "dream" should create
  searchBudget: 12,            // max expansions per ★ Search run
  weights: { time: 1, money: 1, effort: 1, risk: 1 },
  groq: { apiKey: '', model: 'openai/gpt-oss-20b' },
  claude: { apiKey: '', model: 'claude-opus-5-5', effort: 'medium', refusalFallback: true },
  ollama: { endpoint: 'http://localhost:11434', model: 'llama3.1' },
  webhook: { url: '', headers: '' },
  gist: { token: '', id: '', auto: false },
};

function deepMerge(def, val) {
  if (typeof def !== 'object' || def === null || Array.isArray(def)) return val === undefined ? def : val;
  const out = { ...def };
  for (const k of Object.keys(val || {})) out[k] = deepMerge(def[k], val[k]);
  return out;
}

export function loadData() {
  let d = {};
  try { d = JSON.parse(localStorage.getItem(KEY)) || {}; } catch { d = {}; }
  return {
    boards: d.boards || {},
    deleted: d.deleted || {},
    currentId: d.currentId || null,
    settings: deepMerge(DEFAULT_SETTINGS, d.settings || {}),
  };
}

export function saveData(data) {
  try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) { console.warn('save failed', e); }
}

const short = (s, n) => (s.length > n ? s.slice(0, n - 1).trimEnd() + '…' : s);

export function createBoard({ goal, context = '', constraints = '' }) {
  const firstLine = context.split(/[.\n]/)[0].trim();
  const start = {
    id: uid(), kind: 'start', label: firstLine ? short('Now: ' + firstLine, 70) : 'Where I am now',
    note: context, h: null, x: 80, y: 240, done: true,
  };
  const goalNode = {
    id: uid(), kind: 'goal', label: goal, note: '', h: 0, x: 900, y: 240, done: false,
  };
  return {
    id: uid('b'), title: goal, constraints,
    startId: start.id, goalId: goalNode.id,
    nodes: { [start.id]: start, [goalNode.id]: goalNode },
    edges: {},
    created: now(), updated: now(),
  };
}

export const normLabel = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

// Merge a dreamer result ({states, actions}) into a board.
// ctx: { by, hereId, fromId, toId, replaceEdgeId }
export function applyDream(board, result, ctx = {}) {
  const keymap = {};
  const created = [];
  const byLabel = new Map(Object.values(board.nodes).map((n) => [normLabel(n.label), n.id]));

  for (const s of result.states) {
    const hit = byLabel.get(normLabel(s.label));
    if (hit) { keymap[s.key] = hit; continue; }
    const n = { id: uid(), kind: 'state', label: s.label, note: s.note, h: s.h, x: null, y: null, done: false, by: ctx.by };
    board.nodes[n.id] = n;
    keymap[s.key] = n.id;
    byLabel.set(normLabel(s.label), n.id);
    created.push(n.id);
  }

  const special = { START: board.startId, GOAL: board.goalId, HERE: ctx.hereId, FROM: ctx.fromId, TO: ctx.toId };
  const ref = (k) => special[k] ?? keymap[k] ?? (board.nodes[k] ? k : null);
  const newEdges = [];
  for (const a of result.actions) {
    const from = ref(a.from), to = ref(a.to);
    if (!from || !to || from === to) continue;
    if (Object.values(board.edges).some((e) => e.from === from && e.to === to)) continue;
    const e = {
      id: uid('e'), from, to, label: a.label, note: a.note,
      cost: { time: a.time, money: a.money, effort: a.effort, risk: a.risk }, by: ctx.by,
    };
    board.edges[e.id] = e;
    newEdges.push(e.id);
  }

  if (ctx.replaceEdgeId && newEdges.length >= 2) delete board.edges[ctx.replaceEdgeId];

  // States the dreamer forgot to connect are just noise.
  const linked = new Set(Object.values(board.edges).flatMap((e) => [e.from, e.to]));
  for (const id of created) if (!linked.has(id)) delete board.nodes[id];

  board.updated = now();
  return { nodes: created.filter((id) => board.nodes[id]), edges: newEdges };
}

export function deleteNode(board, id) {
  if (id === board.startId || id === board.goalId) return false;
  delete board.nodes[id];
  for (const e of Object.values(board.edges)) if (e.from === id || e.to === id) delete board.edges[e.id];
  return true;
}
