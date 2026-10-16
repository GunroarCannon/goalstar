// A* over the goal graph.
// g = summed action cost from any achieved state, h = node.h (the dreamer's
// estimate of remaining cost). Costs are a weighted average of four 0–10
// ratings, so "weights" are how much you care about time vs money vs effort vs risk.

const KEYS = ['time', 'money', 'effort', 'risk'];

export function edgeCost(e, w) {
  let s = 0, ws = 0;
  for (const k of KEYS) {
    const wk = w?.[k] ?? 1;
    s += wk * (e.cost?.[k] ?? 3);
    ws += wk;
  }
  return ws ? s / ws : 0;
}

export const isAchieved = (n) => !!n && (n.kind === 'start' || n.done);

export function heuristic(board) {
  return (id) => (id === board.goalId ? 0 : Math.max(0, board.nodes[id]?.h ?? 0));
}

// opts.fromStart: plan from the start only, as if nothing were achieved yet (for progress).
export function astar(board, w, opts = {}) {
  const { nodes, goalId } = board;
  const out = {};
  for (const e of Object.values(board.edges)) (out[e.from] ||= []).push(e);
  const h = heuristic(board);

  const g = new Map(), came = new Map(), open = new Set(), closed = new Set(), explored = [];
  for (const n of Object.values(nodes)) {
    if (opts.fromStart ? n.id === board.startId : isAchieved(n)) { g.set(n.id, 0); open.add(n.id); }
  }

  while (open.size) {
    let cur = null, best = Infinity;
    for (const id of open) {
      const f = g.get(id) + h(id);
      if (f < best || (f === best && h(id) < h(cur))) { best = f; cur = id; }
    }
    open.delete(cur);
    closed.add(cur);
    explored.push(cur);

    if (cur === goalId) {
      const pathNodes = [goalId], pathEdges = [];
      let c = goalId;
      while (came.has(c)) {
        const { from, edge } = came.get(c);
        pathEdges.unshift(edge);
        pathNodes.unshift(from);
        c = from;
      }
      return { found: true, nodes: pathNodes, edges: pathEdges, cost: g.get(goalId), g, explored };
    }

    for (const e of out[cur] || []) {
      if (!nodes[e.to]) continue;
      const t = g.get(cur) + edgeCost(e, w);
      if (t < (g.get(e.to) ?? Infinity)) {
        g.set(e.to, t);
        came.set(e.to, { from: cur, edge: e.id });
        closed.delete(e.to); // reopen: dreamed heuristics aren't guaranteed consistent
        open.add(e.to);
      }
    }
  }
  return { found: false, nodes: [], edges: [], cost: Infinity, g, explored };
}

// Actions you can take right now: edges leaving an achieved state toward one that isn't.
export function nextActions(board, w) {
  const h = heuristic(board);
  return Object.values(board.edges)
    .filter((e) => isAchieved(board.nodes[e.from]) && board.nodes[e.to] && !isAchieved(board.nodes[e.to]))
    .map((e) => { const c = edgeCost(e, w); return { e, c, f: c + h(e.to) }; })
    .sort((a, b) => a.f - b.f);
}

// Fill in h for states that have none (e.g. after a breakdown) from what follows them.
export function estimateMissingH(board, w) {
  const missing = Object.values(board.nodes).filter((n) => n.h == null && n.id !== board.goalId && n.kind !== 'start');
  if (!missing.length) return;
  const est = {};
  const val = (id) => (id === board.goalId ? 0 : board.nodes[id]?.h ?? est[id]);
  for (let it = 0; it < missing.length + 1; it++) {
    for (const n of missing) {
      for (const e of Object.values(board.edges)) {
        if (e.from !== n.id || val(e.to) == null) continue;
        const v = edgeCost(e, w) + val(e.to);
        if (est[n.id] == null || v < est[n.id]) est[n.id] = v;
      }
    }
  }
  for (const n of missing) if (est[n.id] != null) n.h = Math.round(est[n.id] * 10) / 10;
}

// The time rating (0–10) on a rough log scale: 0 ≈ an hour, 3 ≈ a week,
// 5 ≈ a month, 7 ≈ six months, 10 ≈ three years.
const TIME_ANCHORS = [[0, 1 / 24], [1, 1], [3, 7], [5, 30], [7, 182], [10, 1095]];
export function timeToDays(t) {
  const v = Math.min(10, Math.max(0, t ?? 3));
  for (let i = 1; i < TIME_ANCHORS.length; i++) {
    const [x0, d0] = TIME_ANCHORS[i - 1], [x1, d1] = TIME_ANCHORS[i];
    if (v <= x1) return Math.exp(Math.log(d0) + ((v - x0) / (x1 - x0)) * (Math.log(d1) - Math.log(d0)));
  }
  return 1095;
}

export function fmtDays(d) {
  if (!Number.isFinite(d)) return '?';
  if (d < 0.5) return 'hours';
  if (d < 1.5) return '1 day';
  if (d < 13) return `${Math.round(d)} days`;
  if (d < 60) return `${Math.round(d / 7)} wk`;
  if (d < 700) return `${Math.round(d / 30.4)} mo`;
  return `${Math.round(d / 36.5) / 10} yr`;
}
