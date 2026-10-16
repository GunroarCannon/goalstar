// Left-to-right layered layout: start on the left, goal on the right.

export const COL = 300, ROW = 150;
const X0 = 80, Y0 = 80;

export function tidy(board) {
  const nodes = board.nodes;
  const ids = Object.keys(nodes);
  const edges = Object.values(board.edges).filter((e) => nodes[e.from] && nodes[e.to]);
  const N = ids.length;
  const depth = {};

  for (const id of ids) if (nodes[id].kind === 'start') depth[id] = 0;
  const relax = () => {
    for (let it = 0; it < N; it++) {
      let changed = false;
      for (const e of edges) {
        if (depth[e.from] == null || nodes[e.to].kind === 'start') continue;
        const d = depth[e.from] + 1;
        if (d <= N && (depth[e.to] == null || depth[e.to] < d)) { depth[e.to] = d; changed = true; }
      }
      if (!changed) break;
    }
  };
  relax();
  // Islands not reachable from the start: seed them in column 1.
  let seeded = false;
  for (const id of ids) if (depth[id] == null && !edges.some((e) => e.to === id)) { depth[id] = 1; seeded = true; }
  if (seeded) relax();
  for (const id of ids) if (depth[id] == null) depth[id] = 1;

  const maxOther = Math.max(0, ...ids.filter((id) => id !== board.goalId).map((id) => depth[id]));
  depth[board.goalId] = Math.max(depth[board.goalId], maxOther + 1);

  const cols = [];
  for (const id of ids) (cols[depth[id]] ||= []).push(id);
  const pos = {};
  const index = () => cols.forEach((c) => c && c.forEach((id, i) => (pos[id] = i - (c.length - 1) / 2)));
  index();
  for (let pass = 0; pass < 3; pass++) {
    for (let d = 1; d < cols.length; d++) {
      if (!cols[d]) continue;
      const bary = (id) => {
        const ps = edges.filter((e) => e.to === id && depth[e.from] < d).map((e) => pos[e.from]);
        return ps.length ? ps.reduce((a, b) => a + b, 0) / ps.length : pos[id];
      };
      const b = Object.fromEntries(cols[d].map((id) => [id, bary(id)]));
      cols[d].sort((p, q) => b[p] - b[q]);
      index();
    }
  }

  const tallest = Math.max(...cols.map((c) => (c ? c.length : 0)));
  const midY = Y0 + ((tallest - 1) / 2) * ROW;
  for (const id of ids) {
    nodes[id].x = X0 + depth[id] * COL;
    nodes[id].y = midY + pos[id] * ROW;
  }
}

function collide(board, n) {
  for (let tries = 0; tries < 60; tries++) {
    const hit = Object.values(board.nodes).some(
      (o) => o !== n && o.x != null && Math.abs(o.x - n.x) < 230 && Math.abs(o.y - n.y) < 115,
    );
    if (!hit) return;
    n.y += 60;
  }
}

// Place freshly dreamed nodes next to whatever they connect to.
export function placeNew(board, ids) {
  const nodes = board.nodes;
  const edges = Object.values(board.edges);
  const pending = new Set(ids.filter((id) => nodes[id] && nodes[id].x == null));
  const childCount = {};

  for (let guard = 0; pending.size && guard < 50; guard++) {
    let progress = false;
    for (const id of [...pending]) {
      const n = nodes[id];
      const inE = edges.find((e) => e.to === id && nodes[e.from]?.x != null && e.from !== board.goalId);
      const outE = edges.find((e) => e.from === id && nodes[e.to]?.x != null && e.to !== board.goalId);
      if (inE) {
        const p = nodes[inE.from];
        const k = (childCount[p.id] = (childCount[p.id] ?? -1) + 1);
        n.x = p.x + COL;
        n.y = p.y + k * ROW;
      } else if (outE) {
        const c = nodes[outE.to];
        n.x = c.x - COL;
        n.y = c.y + ROW;
      } else continue;
      collide(board, n);
      pending.delete(id);
      progress = true;
    }
    if (!progress) break;
  }
  for (const id of pending) {
    const placed = Object.values(nodes).filter((n) => n.x != null);
    nodes[id].x = nodes[board.startId].x + COL;
    nodes[id].y = Math.max(...placed.map((n) => n.y)) + ROW;
  }

  const goal = nodes[board.goalId];
  const maxX = Math.max(...Object.values(nodes).filter((n) => n !== goal).map((n) => n.x ?? 0));
  if (goal.x < maxX + COL - 40) { goal.x = maxX + COL; collide(board, goal); }
}
