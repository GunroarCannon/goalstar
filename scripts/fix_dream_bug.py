import sys

# 1. Patch js/model.js
with open(r'C:\Users\hmmm\goalstar-recall\js\model.js', 'r', encoding='utf-8') as f:
    model_code = f.read()

start_marker = "export function applyDream(board, result, ctx = {}) {"
end_marker = "export function deleteNode(board, id) {"

start_idx = model_code.find(start_marker)
end_idx = model_code.find(end_marker, start_idx)

assert start_idx != -1 and end_idx != -1, "Could not find applyDream in js/model.js"

new_apply_dream = """export function applyDream(board, result, ctx = {}) {
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
      h: s.h != null ? Math.max(0, s.h) : null,
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

  board.updated = now();
  const validNodes = created.filter((id) => board.nodes[id]);
  return { nodes: validNodes, edges: newEdges, updated: false };
}

"""

model_code = model_code[:start_idx] + new_apply_dream + model_code[end_idx:]
with open(r'C:\Users\hmmm\goalstar-recall\js\model.js', 'w', encoding='utf-8') as f:
    f.write(model_code)
print("Fixed js/model.js applyDream return value!")

# 2. Patch js/app.js to safeguard dream()
with open(r'C:\Users\hmmm\goalstar-recall\js\app.js', 'r', encoding='utf-8') as f:
    app_code = f.read()

old_dream_try = """    const { result, by, warning } = await generate(settings(), req);
    const added = applyDream(b, result, { ...ctx, by });
    estimateMissingH(b, settings().weights);
    placeNew(b, added.nodes);"""

new_dream_try = """    const { result, by, warning } = await generate(settings(), req);
    const added = applyDream(b, result, { ...ctx, by }) || { nodes: [], edges: [], updated: false };
    estimateMissingH(b, settings().weights);
    placeNew(b, added.nodes || []);"""

assert old_dream_try in app_code, "old_dream_try not found in js/app.js"
app_code = app_code.replace(old_dream_try, new_dream_try)

with open(r'C:\Users\hmmm\goalstar-recall\js\app.js', 'w', encoding='utf-8') as f:
    f.write(app_code)
print("Safeguarded js/app.js dream() against null added!")
