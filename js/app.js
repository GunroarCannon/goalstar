import { loadData, saveData, createBoard, applyDream, deleteNode, uid, now } from './model.js';
import { astar, edgeCost, nextActions, heuristic, estimateMissingH } from './astar.js';
import { tidy, placeNew, COL } from './layout.js';
import { Canvas, esc } from './render.js';
import { generate } from './dreamers/index.js';
import * as gist from './sync.js';

const $ = (s, el = document) => el.querySelector(s);
const fmt = (v) => (v == null || !Number.isFinite(v) ? '?' : Math.round(v * 10) / 10);

const data = loadData();
let sel = null;            // { type: 'node' | 'edge', id }
let busy = false;
let stopRequested = false;
let pulseId = null;
let lastPath = null;
const logLines = [];

const board = () => data.boards[data.currentId];
const settings = () => data.settings;

// ---------- persistence ----------
let syncTimer = null;
function persist({ touch = true } = {}) {
  if (touch && board()) board().updated = now();
  saveData(data);
  const g = settings().gist;
  if (g.auto && g.token) {
    clearTimeout(syncTimer);
    syncTimer = setTimeout(() => syncNow(true), 8000);
  }
}

// ---------- UI helpers ----------
function toast(msg, kind = '') {
  const t = $('#toast');
  t.textContent = msg;
  t.className = `toast show ${kind}`;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => (t.className = 'toast'), kind === 'err' ? 6000 : 3000);
}

function log(msg) {
  logLines.unshift({ t: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), msg });
  logLines.length = Math.min(logLines.length, 30);
  $('#log').innerHTML = logLines.map((l) => `<li><span class="muted">${l.t}</span> ${esc(l.msg)}</li>`).join('');
}

function setBusy(on, label = '') {
  busy = on;
  $('#status').innerHTML = on ? `<span class="spin">✦</span> ${esc(label)}` : '';
  for (const id of ['#dreamBtn', '#searchBtn', '#newGoalBtn']) $(id).disabled = on;
  for (const b of document.querySelectorAll('.inspector .dream')) b.disabled = on;
}

// ---------- canvas ----------
const canvas = new Canvas($('#canvas'), {
  onSelect: (s) => select(s),
  onBackgroundClick: () => {
    if (canvas.linkFrom) { canvas.setLinkMode(null); toast('Link cancelled'); }
    select(null);
  },
  onBackgroundDblClick: (x, y) => addState(x, y),
  onNodeMoved: () => persist(),
  onToggleDone: (id) => toggleDone(id),
  onLink: (from, to) => link(from, to),
});

function refresh({ inspector = true } = {}) {
  const b = board();
  $('#empty').hidden = !!b;
  document.body.classList.toggle('no-board', !b);
  renderBoardPick();
  if (!b) { $('#inspector').hidden = true; return; }

  const w = settings().weights;
  const r = astar(b, w);
  lastPath = r;
  canvas.render(b, {
    path: r.found ? { nodes: new Set(r.nodes), edges: new Set(r.edges) } : null,
    g: r.g, sel, weights: w, pulse: pulseId,
  });

  $('#goalTitle').textContent = b.nodes[b.goalId].label;
  const d = settings().dreamer;
  $('#dreamerBadge').textContent = `dreamer: ${d}${d === 'claude' ? ' · ' + settings().claude.model.replace('claude-', '') : d === 'ollama' ? ' · ' + settings().ollama.model : d === 'groq' ? ' · ' + settings().groq.model : ''}`;
  renderPath(b, r, w);
  renderNext(b, w);
  if (inspector) renderInspector();
}

function renderBoardPick() {
  const boards = Object.values(data.boards).sort((a, b) => b.updated - a.updated);
  $('#boardPick').innerHTML = boards.map((b) => `<option value="${b.id}" ${b.id === data.currentId ? 'selected' : ''}>${esc(b.nodes[b.goalId]?.label || b.title)}</option>`).join('');
  $('#boardPick').hidden = !boards.length;
}

function renderPath(b, r, w) {
  const list = $('#pathList');
  if (b.nodes[b.goalId].done) {
    list.innerHTML = '<li class="win">🎉 Goal achieved!</li>';
    $('#pathTotal').textContent = '';
    return;
  }
  if (!r.found) {
    list.innerHTML = `<li class="muted">No path to the goal yet. Try <b>✦ Dream map</b> or <b>★ Search</b>, or select a state and link it onward.</li>`;
    $('#pathTotal').textContent = '';
    return;
  }
  list.innerHTML = r.edges.map((eid) => {
    const e = b.edges[eid], to = b.nodes[e.to];
    return `<li data-edge="${eid}" class="${sel?.id === eid ? 'sel' : ''}">
      <div class="step">${esc(e.label)}</div>
      <div class="sub">→ ${esc(to.label)} <span class="cost">${fmt(edgeCost(e, w))}</span></div>
    </li>`;
  }).join('');
  $('#pathTotal').textContent = `${r.edges.length} step${r.edges.length === 1 ? '' : 's'} · total cost ${fmt(r.cost)} · explored ${r.explored.length} states`;
}

function renderNext(b, w) {
  const items = nextActions(b, w).slice(0, 6);
  const onPath = new Set(lastPath?.edges || []);
  $('#nextList').innerHTML = items.length
    ? items.map(({ e, c }) => `<li data-edge="${e.id}">
        <button class="tick-sm" data-done="${e.to}" title="I did this">✓</button>
        <div><div class="step">${onPath.has(e.id) ? '★ ' : ''}${esc(e.label)}</div>
        <div class="sub">→ ${esc(b.nodes[e.to].label)} <span class="cost">${fmt(c)}</span></div></div>
      </li>`).join('')
    : '<li class="muted">Nothing available from where you are. Dream or add states.</li>';
}

function renderWeights() {
  const w = settings().weights;
  const names = { time: 'Time', money: 'Money', effort: 'Effort', risk: 'Risk' };
  $('#weights').innerHTML = Object.keys(names).map((k) => `
    <label><span>${names[k]}</span><input type="range" min="0" max="3" step="0.5" value="${w[k]}" data-w="${k}"><output>${w[k]}</output></label>`).join('');
}

// ---------- inspector ----------
function select(s) {
  sel = s;
  refresh();
}

function renderInspector() {
  const el = $('#inspector');
  const b = board();
  if (!sel || !b || (sel.type === 'node' && !b.nodes[sel.id]) || (sel.type === 'edge' && !b.edges[sel.id])) {
    el.hidden = true;
    sel = null;
    return;
  }
  el.hidden = false;
  if (sel.type === 'node') {
    const n = b.nodes[sel.id];
    const g = lastPath?.g.get(n.id);
    const outs = Object.values(b.edges).filter((e) => e.from === n.id).length;
    el.innerHTML = `
      <div class="ins-head"><span class="kind">${n.kind === 'goal' ? '★ Goal' : n.kind === 'start' ? '● Where you are' : 'State'}</span><button class="icon close" data-act="close">×</button></div>
      <label>State <textarea data-f="label" rows="3">${esc(n.label)}</textarea></label>
      <label>Notes <textarea data-f="note" rows="4" placeholder="Details, links, numbers…">${esc(n.note)}</textarea></label>
      ${n.kind === 'goal' || n.kind === 'start' ? '' : `
        <div class="grid2">
          <label>h (cost left) <input type="number" step="0.5" min="0" data-f="h" value="${n.h ?? ''}"></label>
          <label class="row ach"><input type="checkbox" data-f="done" ${n.done ? 'checked' : ''}> Achieved</label>
        </div>`}
      <div class="muted small">${g != null ? `g (cost so far) ${fmt(g)} · ` : 'not reachable from where you are · '}${outs} outgoing action${outs === 1 ? '' : 's'}</div>
      <div class="btns">
        ${n.kind === 'goal' ? '' : `<button class="dream primary" data-act="expand" ${busy ? 'disabled' : ''}>✦ Dream next states</button>`}
        ${n.kind === 'goal' ? '' : '<button data-act="link">Link → another state</button>'}
        ${n.kind === 'goal' ? '' : '<button data-act="child">+ Add next state</button>'}
        <button data-act="center">Center</button>
        ${n.kind === 'state' ? '<button data-act="delete" class="danger">Delete</button>' : ''}
      </div>`;
  } else {
    const e = b.edges[sel.id];
    const w = settings().weights;
    const slider = (k, hint) => `<label class="slider"><span>${k}</span><input type="range" min="0" max="10" step="1" data-c="${k}" value="${e.cost[k] ?? 3}"><output>${e.cost[k] ?? 3}</output><span class="muted small">${hint}</span></label>`;
    el.innerHTML = `
      <div class="ins-head"><span class="kind">Action</span><button class="icon close" data-act="close">×</button></div>
      <div class="muted small">${esc(b.nodes[e.from].label)} → ${esc(b.nodes[e.to].label)}</div>
      <label>Action <textarea data-f="label" rows="3">${esc(e.label)}</textarea></label>
      <label>Notes <textarea data-f="note" rows="3">${esc(e.note)}</textarea></label>
      ${slider('time', 'week≈3 · month≈5 · years=10')}
      ${slider('money', 'month of income≈5')}
      ${slider('effort', '')}
      ${slider('risk', 'chance it fails')}
      <div class="muted small">cost with your weights: <b id="edgeCostOut">${fmt(edgeCost(e, w))}</b>${e.by ? ` · dreamed by ${esc(e.by)}` : ''}</div>
      <div class="btns">
        <button class="dream primary" data-act="breakdown" ${busy ? 'disabled' : ''}>✦ Break into smaller steps</button>
        <button data-act="done">✓ I did this</button>
        <button data-act="delete" class="danger">Delete</button>
      </div>`;
  }
}

$('#inspector').addEventListener('input', (ev) => {
  const b = board();
  const t = ev.target;
  if (!sel || !b) return;
  const obj = sel.type === 'node' ? b.nodes[sel.id] : b.edges[sel.id];
  if (t.dataset.f === 'label' || t.dataset.f === 'note') obj[t.dataset.f] = t.value;
  else if (t.dataset.f === 'h') obj.h = t.value === '' ? null : Math.max(0, Number(t.value));
  else if (t.dataset.f === 'done') obj.done = t.checked;
  else if (t.dataset.c) {
    obj.cost[t.dataset.c] = Number(t.value);
    t.nextElementSibling.textContent = t.value;
    $('#edgeCostOut').textContent = fmt(edgeCost(obj, settings().weights));
  }
  if (sel.type === 'node' && obj.kind === 'goal' && t.dataset.f === 'label') b.title = obj.label;
  persist();
  refresh({ inspector: t.dataset.f === 'done' });
});

$('#inspector').addEventListener('click', async (ev) => {
  const act = ev.target.closest('[data-act]')?.dataset.act;
  if (!act || !sel) return;
  const b = board();
  if (act === 'close') return select(null);
  if (sel.type === 'node') {
    const id = sel.id;
    if (act === 'expand') { await expandNode(id); refresh(); }
    if (act === 'link') { canvas.setLinkMode(id); toast('Click the state this leads to (click paper to cancel)'); }
    if (act === 'child') {
      const n = b.nodes[id];
      const c = addState(n.x + COL, n.y + 40, { select: false });
      link(id, c);
    }
    if (act === 'center') canvas.centerOn(id);
    if (act === 'delete' && deleteNode(b, id)) { sel = null; persist(); refresh(); }
  } else {
    const e = b.edges[sel.id];
    if (act === 'breakdown') { await breakdownEdge(e.id); refresh(); }
    if (act === 'done') toggleDone(e.to, true);
    if (act === 'delete') { delete b.edges[e.id]; sel = null; persist(); refresh(); }
  }
});

// ---------- editing ----------
function addState(x, y, { select: doSelect = true } = {}) {
  const b = board();
  if (!b) return null;
  const n = { id: uid(), kind: 'state', label: 'New state', note: '', h: null, x, y, done: false };
  b.nodes[n.id] = n;
  persist();
  if (doSelect) {
    select({ type: 'node', id: n.id });
    const ta = $('#inspector textarea[data-f="label"]');
    ta?.focus();
    ta?.select();
  }
  return n.id;
}

function link(from, to) {
  canvas.setLinkMode(null);
  const b = board();
  if (from === to) return toast('A state can\'t lead to itself');
  if (Object.values(b.edges).some((e) => e.from === from && e.to === to)) return toast('Those are already linked');
  const e = { id: uid('e'), from, to, label: 'New action', note: '', cost: { time: 3, money: 3, effort: 3, risk: 3 } };
  b.edges[e.id] = e;
  persist();
  select({ type: 'edge', id: e.id });
  const ta = $('#inspector textarea[data-f="label"]');
  ta?.focus();
  ta?.select();
}

function toggleDone(id, value) {
  const n = board().nodes[id];
  if (!n || n.kind === 'start') return;
  n.done = value ?? !n.done;
  if (n.done) toast(n.kind === 'goal' ? '🎉 Goal achieved!' : `✓ ${n.label}`);
  persist();
  refresh();
}

// ---------- dreaming ----------
function request(mode, focus = null) {
  const b = board();
  const s = settings();
  return {
    mode,
    goal: { label: b.nodes[b.goalId].label, note: b.nodes[b.goalId].note },
    start: { label: b.nodes[b.startId].label, note: b.nodes[b.startId].note },
    constraints: b.constraints || '',
    focus,
    existing: Object.values(b.nodes).slice(0, 80).map((n) => ({ id: n.id, label: n.label, kind: n.kind, done: !!n.done })),
    params: { maxStates: s.maxStates, weights: s.weights },
  };
}

async function dream(req, ctx, label) {
  const b = board();
  setBusy(true, label);
  try {
    const { result, by, warning } = await generate(settings(), req);
    const added = applyDream(b, result, { ...ctx, by });
    estimateMissingH(b, settings().weights);
    placeNew(b, added.nodes);
    log(`${by}: ${req.mode} → +${added.nodes.length} states, +${added.edges.length} actions`);
    if (warning) { toast(warning, 'err'); log(warning); }
    persist();
    return added;
  } catch (err) {
    console.error(err);
    toast(`Dream failed: ${err.message}`, 'err');
    log(`failed: ${err.message}`);
    return null;
  } finally {
    setBusy(false);
  }
}

async function dreamMap() {
  const b = board();
  if (!b || busy) return;
  if (Object.keys(b.edges).length && !confirm('Dream a fresh map onto this board? Existing states are kept; matching ones are merged.')) return;
  const added = await dream(request('dream'), {}, 'dreaming a map…');
  if (added) { tidy(b); persist(); refresh(); canvas.fit(); }
}

async function expandNode(id) {
  const b = board();
  const n = b.nodes[id];
  const added = await dream(request('expand', { node: { id, label: n.label, note: n.note, h: n.h } }), { hereId: id }, `expanding “${n.label.slice(0, 30)}”…`);
  if (added) n.expanded = true;
  return added;
}

async function breakdownEdge(eid) {
  const b = board();
  const e = b.edges[eid];
  const focus = { edge: { label: e.label, note: e.note, from: b.nodes[e.from].label, to: b.nodes[e.to].label, cost: e.cost } };
  const added = await dream(request('breakdown', focus), { fromId: e.from, toId: e.to, replaceEdgeId: eid }, 'breaking it down…');
  if (added && !b.edges[eid]) sel = null;
  return added;
}

// Lazy A*: the dreamer is the successor function. Expand the most promising
// unexpanded state (lowest g + h, leaves first) until a path reaches the goal.
async function search() {
  const b = board();
  if (!b || busy) return;
  stopRequested = false;
  $('#stopBtn').hidden = false;
  const w = settings().weights;
  const h = heuristic(b);
  for (let i = 0; i < settings().searchBudget && !stopRequested; i++) {
    const r = astar(b, w);
    if (r.found) break;
    const hasOut = new Set(Object.values(b.edges).map((e) => e.from));
    const cands = [...r.g.keys()].filter((id) => id !== b.goalId && !b.nodes[id].expanded);
    if (!cands.length) { toast('Nothing left to expand — add or link a state by hand.'); break; }
    const f = (id) => (hasOut.has(id) ? 1e6 : 0) + r.g.get(id) + h(id);
    cands.sort((p, q) => f(p) - f(q));
    const id = cands[0];
    pulseId = id;
    refresh();
    canvas.centerOn(id);
    log(`★ expanding “${b.nodes[id].label}” (f = ${fmt(r.g.get(id) + h(id))})`);
    const added = await expandNode(id);
    pulseId = null;
    refresh();
    if (!added) break;
  }
  pulseId = null;
  $('#stopBtn').hidden = true;
  const r = astar(b, w);
  refresh();
  if (r.found) { toast(`★ Path found: ${r.edges.length} steps, cost ${fmt(r.cost)}`); canvas.fit(); }
  else if (stopRequested) toast('Search stopped');
  else toast('No path yet — run ★ Search again or raise the budget in Settings');
}

// ---------- boards ----------
function openNewGoal() {
  const f = $('#newGoalForm');
  f.reset();
  $('#newGoalDlg').returnValue = '';
  $('#newGoalDlg').showModal();
}

$('#newGoalDlg').addEventListener('close', async () => {
  if ($('#newGoalDlg').returnValue !== 'ok') return;
  const f = new FormData($('#newGoalForm'));
  const goal = String(f.get('goal') || '').trim();
  if (!goal) return;
  const b = createBoard({ goal, context: String(f.get('context') || '').trim(), constraints: String(f.get('constraints') || '').trim() });
  data.boards[b.id] = b;
  data.currentId = b.id;
  sel = null;
  persist();
  refresh();
  canvas.fit();
  if (f.get('dream')) {
    const added = await dream(request('dream'), {}, 'dreaming a map…');
    if (added) { tidy(b); persist(); refresh(); canvas.fit(); }
  }
});

function switchBoard(id) {
  data.currentId = id;
  sel = null;
  canvas.setLinkMode(null);
  persist({ touch: false });
  refresh();
  canvas.fit();
}

// ---------- settings ----------
const getPath = (obj, path) => path.split('.').reduce((o, k) => o?.[k], obj);
const setPath = (obj, path, v) => {
  const ks = path.split('.');
  const last = ks.pop();
  ks.reduce((o, k) => o[k], obj)[last] = v;
};

function openSettings() {
  const f = $('#settingsForm');
  for (const el of f.elements) {
    if (!el.name) continue;
    const v = getPath(settings(), el.name);
    if (el.type === 'radio') el.checked = v === el.value;
    else if (el.type === 'checkbox') el.checked = !!v;
    else el.value = v ?? '';
  }
  showPane();
  $('#settingsDlg').returnValue = '';
  $('#settingsDlg').showModal();
}

function showPane() {
  const v = $('#settingsForm').elements.dreamer.value;
  for (const p of document.querySelectorAll('.pane')) p.hidden = p.dataset.pane !== v;
}
$('#dreamerSeg').addEventListener('change', showPane);

$('#settingsDlg').addEventListener('close', () => {
  if ($('#settingsDlg').returnValue !== 'ok') return;
  const f = $('#settingsForm');
  for (const el of f.elements) {
    if (!el.name || (el.type === 'radio' && !el.checked)) continue;
    let v = el.type === 'checkbox' ? el.checked : el.value.trim();
    if (el.type === 'number') v = Math.max(Number(el.min) || 1, Math.min(Number(el.max) || 99, Number(v) || 1));
    setPath(settings(), el.name, v);
  }
  persist({ touch: false });
  refresh();
  toast('Settings saved');
});

// ---------- sync / import / export ----------
async function syncNow(quiet = false) {
  const g = settings().gist;
  if (!g.token) { if (!quiet) { toast('Add a GitHub token in Settings → Cloud sync'); openSettings(); } return; }
  $('#syncBtn').classList.add('spinning');
  try {
    if (g.id) {
      const remote = await gist.pull(g);
      if (remote) {
        const m = gist.mergeData(data, remote);
        data.boards = m.boards;
        data.deleted = m.deleted;
        if (!data.boards[data.currentId]) data.currentId = Object.keys(data.boards)[0] || null;
      }
    }
    const id = await gist.push(g, { version: 1, boards: data.boards, deleted: data.deleted, saved: now() });
    if (!g.id) { g.id = id; toast(`Created secret gist ${id} — paste this id on your other devices`); }
    else if (!quiet) toast('Synced ✓');
    saveData(data);
    refresh();
  } catch (err) {
    toast(`Sync failed: ${err.message}`, 'err');
  } finally {
    $('#syncBtn').classList.remove('spinning');
  }
}

$('#exportBtn').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify({ version: 1, boards: data.boards, deleted: data.deleted }, null, 1)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `goalstar-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
});
$('#importBtn').addEventListener('click', () => $('#importFile').click());
$('#importFile').addEventListener('change', async (ev) => {
  const file = ev.target.files[0];
  if (!file) return;
  try {
    const remote = JSON.parse(await file.text());
    const m = gist.mergeData(data, remote);
    data.boards = m.boards;
    data.deleted = m.deleted;
    data.currentId ||= Object.keys(data.boards)[0] || null;
    persist({ touch: false });
    refresh();
    toast(`Imported ${Object.keys(remote.boards || {}).length} goal(s)`);
  } catch (err) {
    toast(`Import failed: ${err.message}`, 'err');
  }
  ev.target.value = '';
});

// ---------- wiring ----------
$('#newGoalBtn').addEventListener('click', openNewGoal);
$('#emptyNewBtn').addEventListener('click', openNewGoal);
$('#boardPick').addEventListener('change', (e) => switchBoard(e.target.value));
$('#dreamBtn').addEventListener('click', dreamMap);
$('#searchBtn').addEventListener('click', search);
$('#stopBtn').addEventListener('click', () => { stopRequested = true; });
$('#tidyBtn').addEventListener('click', () => { if (board()) { tidy(board()); persist(); refresh(); canvas.fit(); } });
$('#fitBtn').addEventListener('click', () => canvas.fit());
$('#settingsBtn').addEventListener('click', openSettings);
$('#syncBtn').addEventListener('click', () => syncNow(false));
$('#sideToggle').addEventListener('click', () => document.body.classList.toggle('side-open'));

$('#deleteBoardBtn').addEventListener('click', () => {
  const b = board();
  if (!b || !confirm(`Delete “${b.nodes[b.goalId].label}”? This can't be undone (unless it's in a sync/export).`)) return;
  delete data.boards[b.id];
  data.deleted[b.id] = now();
  data.currentId = Object.values(data.boards).sort((x, y) => y.updated - x.updated)[0]?.id || null;
  sel = null;
  persist({ touch: false });
  refresh();
  canvas.fit();
});

$('#weights').addEventListener('input', (e) => {
  const k = e.target.dataset.w;
  if (!k) return;
  settings().weights[k] = Number(e.target.value);
  e.target.nextElementSibling.textContent = e.target.value;
  persist({ touch: false });
  refresh({ inspector: false });
});

for (const id of ['#pathList', '#nextList']) {
  $(id).addEventListener('click', (e) => {
    const done = e.target.closest('[data-done]');
    if (done) return toggleDone(done.dataset.done, true);
    const li = e.target.closest('[data-edge]');
    if (li) { select({ type: 'edge', id: li.dataset.edge }); canvas.centerOn(board().edges[li.dataset.edge].to); }
  });
}

document.addEventListener('keydown', (e) => {
  if (e.target.closest('input, textarea, select, dialog')) return;
  const b = board();
  if (e.key === 'Escape') { canvas.setLinkMode(null); select(null); }
  if ((e.key === 'Delete' || e.key === 'Backspace') && sel && b) {
    if (sel.type === 'node' && deleteNode(b, sel.id)) { sel = null; persist(); refresh(); }
    else if (sel.type === 'edge') { delete b.edges[sel.id]; sel = null; persist(); refresh(); }
  }
  if (e.key === 'f') canvas.fit();
});

window.addEventListener('resize', () => board() && canvas.drawEdges());

// ---------- boot ----------
if (!data.boards[data.currentId]) data.currentId = Object.keys(data.boards)[0] || null;
renderWeights();
refresh();
canvas.fit();
if (settings().gist.auto && settings().gist.token && settings().gist.id) syncNow(true);
