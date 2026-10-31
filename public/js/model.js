// Data model + local persistence for goalstar.
// A board is one goal: a graph of STATES (nodes) joined by ACTIONS (edges).

export const uid = (p = 'n') => `${p}_${Math.random().toString(36).slice(2, 9)}`;
export const now = () => Date.now();

const KEY = 'goalstar.v1';

export const DEFAULT_SETTINGS = {
  settingsRev: 2,              // bumped when a default changes for existing saves
  dreamer: 'groq',             // offline | groq | claude | ollama | webhook
  fallbackOffline: true,       // use the built-in dreamer when the chosen one fails
  detail: 'normal',            // default for new goals: brief | normal | detailed | deep
  routes: 'many',              // default for new goals: one | some | many
  searchBudget: 12,            // max expansions per Search run
  display: { paper: 'lined', notes: true, numbers: true, minimap: true, motion: true, arrowGlow: false, font: 'hand' },
  weights: { time: 1, money: 1, effort: 1, risk: 1 },
  groq: { apiKey: '', model: 'openai/gpt-oss-120b' }, // key comes from this project's .env
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

export function getStarterBoard() {
  const bId = 'b_starter_total_recall';
  const startId = 'n_start';
  const s1Id = 'n_arch';
  const s2Id = 'n_devops';
  const s3Id = 'n_paas';
  const s4Id = 'n_auth';
  const goalId = 'n_goal';

  return {
    id: bId,
    title: 'Launch SaaS with Walrus Memory & Sui',
    constraints: 'Solo developer, 3-week hackathon window',
    timeframe: '3 weeks',
    budget: '$100',
    detail: 'normal',
    routes: 'many',
    startId: startId,
    goalId: goalId,
    nodes: {
      [startId]: { id: startId, kind: 'start', label: 'Now: Prototype Idea Ready', note: 'Ready to build autonomous workflow agent', h: 8.5, x: 80, y: 240, done: true },
      [s1Id]: { id: s1Id, kind: 'state', label: 'Architecture & API Specs Finalized', note: 'Endpoints and schemas defined', h: 6.5, x: 340, y: 240, done: true },
      [s2Id]: { id: s2Id, kind: 'state', label: 'Kubernetes Cluster & Docker Compose', note: 'Heavy DevOps configuration', h: 5.0, x: 620, y: 120, done: false },
      [s3Id]: { id: s3Id, kind: 'state', label: 'Alternative: Deploy to Managed Cloud / PaaS', note: 'Zero-config serverless deployment', h: 3.5, x: 620, y: 360, done: false },
      [s4Id]: { id: s4Id, kind: 'state', label: 'Walrus Memory & Sui Proofs Tested', note: '10 memories on Mainnet and Sui verification', h: 2.0, x: 880, y: 240, done: false },
      [goalId]: { id: goalId, kind: 'goal', label: 'Production Launch on Mainnet', note: 'Live submission for Total Recall', h: 0, x: 1140, y: 240, done: false },
    },
    edges: {
      'e1': { id: 'e1', from: startId, to: s1Id, label: 'Design system & Walrus data model', cost: { time: 2, money: 0, effort: 3, risk: 1 }, duration: '2 days', steps: [{ text: 'Draft schemas', done: true }] },
      'e2_devops': { id: 'e2_devops', from: s1Id, to: s2Id, label: 'Setup Docker cluster and k8s config', cost: { time: 5, money: 1, effort: 8, risk: 6 }, duration: '5 days', steps: [{ text: 'Write compose file', done: false }] },
      'e3_paas': { id: 'e3_paas', from: s1Id, to: s3Id, label: 'Deploy to Managed Cloud / PaaS (Low Friction)', cost: { time: 1, money: 0, effort: 2, risk: 1 }, duration: '1 day', steps: [{ text: 'Connect repo', done: false }] },
      'e4': { id: 'e4', from: s2Id, to: s4Id, label: 'Wire Walrus client & Sui RPC', cost: { time: 3, money: 0, effort: 4, risk: 2 }, duration: '2 days' },
      'e5': { id: 'e5', from: s3Id, to: s4Id, label: 'Wire Walrus client & Sui RPC', cost: { time: 2, money: 0, effort: 3, risk: 1 }, duration: '2 days' },
      'e6': { id: 'e6', from: s4Id, to: goalId, label: 'Submit to Hackathon & Share Demo', cost: { time: 1, money: 0, effort: 2, risk: 1 }, duration: '1 day' }
    },
    created: now(),
    updated: now()
  };
}

export function loadData() {
  let d = {};
  try { d = JSON.parse(localStorage.getItem(KEY)) || {}; } catch { d = {}; }
  let boards = d.boards || {};
  let currentId = d.currentId || null;

  // If no boards, provide starter board
  if (!Object.keys(boards).length) {
    const starter = getStarterBoard();
    boards[starter.id] = starter;
    currentId = starter.id;
  }

  const settings = deepMerge(DEFAULT_SETTINGS, d.settings || {});
  // Path creation now runs on the dreamer agent instead of the fixed template
  // planner, which used to produce filler states that ignored the goal.
  if ((d.settings?.settingsRev ?? 1) < 2) {
    if (!d.settings?.dreamer || d.settings.dreamer === 'offline') settings.dreamer = 'groq';
    settings.settingsRev = 2;
  }

  return {
    boards,
    deleted: d.deleted || {},
    currentId,
    settings,
  };
}

export function saveData(data) {
  try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) { console.warn('save failed', e); }
}

const short = (s, n) => (s.length > n ? s.slice(0, n - 1).trimEnd() + '…' : s);

// How many states a full dream asks for at each detail level.
export const DETAIL_STATES = { brief: 6, normal: 10, detailed: 14, deep: 18 };

export function createBoard({ goal, context = '', constraints = '', timeframe = '', budget = '', detail = 'normal', routes = 'some' }) {
  const firstLine = context.split(/[.\n]/)[0].trim();
  const start = {
    id: uid(), kind: 'start', label: firstLine ? short('Now: ' + firstLine, 70) : 'Where I am now',
    note: context, h: null, x: 80, y: 240, done: true,
  };
  const goalNode = {
    id: uid(), kind: 'goal', label: goal, note: '', h: 0, x: 900, y: 240, done: false,
  };
  return {
    id: uid('b'), title: goal, constraints, timeframe, budget, detail, routes,
    startId: start.id, goalId: goalNode.id,
    nodes: { [start.id]: start, [goalNode.id]: goalNode },
    edges: {},
    created: now(), updated: now(),
  };
}

export const normLabel = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

// Merge a dreamer result ({states, actions}) into a board.
const toSteps = (list, old = []) => {
  const was = new Map(old.map((s) => [normLabel(s.text), s.done]));
  return (list || []).map((text) => ({ text, done: !!was.get(normLabel(text)) }));
};

// Merge a dreamer result ({states, actions}) into a board.
export function applyDream(board, result, ctx = {}) {
  if (ctx.updateEdgeId) {
    const e = board.edges[ctx.updateEdgeId];
    if (e && result.actions?.[0]) {
      const a = result.actions[0];
      if (a.label) e.label = a.label;
      if (a.note != null) e.note = a.note;
      if (a.duration != null) e.duration = a.duration;
      if (a.steps?.length) e.steps = toSteps(a.steps, e.steps);
      for (const k of ['time', 'money', 'effort', 'risk']) if (a[k] != null) e.cost[k] = a[k];
      e.by = ctx.by;
      board.updated = now();
      return { nodes: [], edges: [e.id], updated: true };
    }
    return { nodes: [], edges: [], updated: false };
  }

  const keyToId = {};
  if (ctx.fromId) keyToId['FROM'] = ctx.fromId;
  if (ctx.toId) keyToId['TO'] = ctx.toId;
  if (ctx.hereId) keyToId['HERE'] = ctx.hereId;
  keyToId['START'] = board.startId;
  keyToId['GOAL'] = board.goalId;

  const created = [];
  const byLabel = new Map(Object.values(board.nodes).map((n) => [(n.label || '').toLowerCase().trim(), n.id]));

  for (const s of result.states || []) {
    const norm = (s.label || '').toLowerCase().trim();
    const hit = byLabel.get(norm);
    if (hit) {
      keyToId[s.key] = hit;
      continue;
    }
    const id = uid();
    keyToId[s.key] = id;
    board.nodes[id] = {
      id,
      kind: 'state',
      label: s.label || 'Next State',
      note: s.note || '',
      h: (s.h != null && Number.isFinite(Number(s.h))) ? Math.max(0, Number(s.h)) : null,
      x: null,
      y: null,
      done: false,
      by: ctx.by
    };
    byLabel.set(norm, id);
    created.push(id);
  }

  if (ctx.replaceEdgeId) {
    delete board.edges[ctx.replaceEdgeId];
  }

  const newEdges = [];
  for (const a of result.actions || []) {
    const from = keyToId[a.from] || a.from;
    const to = keyToId[a.to] || a.to;
    if (!board.nodes[from] || !board.nodes[to] || from === to) continue;
    if (Object.values(board.edges).some((e) => e.from === from && e.to === to)) continue;
    const id = uid('e');
    board.edges[id] = {
      id,
      from,
      to,
      label: a.label || 'Action',
      note: a.note || '',
      cost: { time: a.time ?? 3, money: a.money ?? 3, effort: a.effort ?? 3, risk: a.risk ?? 3 },
      duration: a.duration || '',
      steps: toSteps(a.steps),
      by: ctx.by
    };
    newEdges.push(id);
  }

  // Prune disconnected states
  const linked = new Set(Object.values(board.edges).flatMap((e) => [e.from, e.to]));
  for (const id of created) {
    if (!linked.has(id)) {
      delete board.nodes[id];
    }
  }

  // Ensure newly created nodes are not left as dead-end leaf nodes;
  // link them so they can form a complete path to the goal.
  const validNodes = created.filter((id) => board.nodes[id]);
  for (const id of validNodes) {
    if (id === board.goalId || id === board.startId) continue;
    const hasOut = Object.values(board.edges).some((e) => e.from === id);
    if (!hasOut) {
      let targetId = null;
      if (ctx.hereId && board.nodes[ctx.hereId]) {
        const parentOuts = Object.values(board.edges).filter((e) => e.from === ctx.hereId && e.to !== id && !validNodes.includes(e.to));
        if (parentOuts.length > 0) targetId = parentOuts[0].to;
      }
      if (!targetId || targetId === id) {
        targetId = board.goalId;
      }
      if (targetId && board.nodes[targetId] && targetId !== id) {
        const targetLabel = board.nodes[targetId].label || 'Goal';
        const eid = uid('e');
        board.edges[eid] = {
          id: eid,
          from: id,
          to: targetId,
          label: targetId === board.goalId ? 'Complete milestone to achieve goal' : `Advance to ${targetLabel.slice(0, 36)}`,
          note: 'Linked forward to ensure a complete, navigable path to goal',
          cost: { time: 3, money: 2, effort: 3, risk: 2 },
          duration: '1–2 weeks',
          steps: toSteps([`Finalize progress on "${board.nodes[id].label.slice(0, 32)}"`, `Proceed to ${targetLabel.slice(0, 32)}`]),
          by: ctx.by || 'goalstar'
        };
        newEdges.push(eid);
      }
    }
  }

  board.updated = now();
  return { nodes: validNodes, edges: newEdges, updated: false };
}

export function deleteNode(board, id) {
  if (id === board.startId || id === board.goalId) return false;
  delete board.nodes[id];
  for (const [eid, e] of Object.entries(board.edges)) {
    if (e.from === id || e.to === id) delete board.edges[eid];
  }
  return true;
}
