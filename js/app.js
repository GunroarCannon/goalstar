import { loadData, saveData, createBoard, applyDream, deleteNode, uid, now, DETAIL_STATES } from './model.js';
import { astar, edgeCost, nextActions, heuristic, estimateMissingH, timeToDays, fmtDays } from './astar.js';
import { tidy, placeNew, COL } from './layout.js';
import { Canvas, esc, costColor, durationText, stepsDone } from './render.js';
import { generate } from './dreamers/index.js';
import * as gist from './sync.js';

const $ = (s, el = document) => el.querySelector(s);
const fmt = (v) => (v == null || !Number.isFinite(v) ? '?' : Math.round(v * 10) / 10);
const KEYS = ['time', 'money', 'effort', 'risk'];
const KEY_NAMES = { time: 'Time', money: 'Money', effort: 'Effort', risk: 'Risk' };
const PRESETS = {
  Balanced: { time: 1, money: 1, effort: 1, risk: 1 },
  Fastest: { time: 3, money: 0.5, effort: 1, risk: 1 },
  Cheapest: { time: 1, money: 3, effort: 1, risk: 1 },
  Easiest: { time: 1, money: 1, effort: 3, risk: 0.5 },
  Safest: { time: 1, money: 1, effort: 1, risk: 3 },
};
const EXAMPLES = [
  ['Live and work in Canada', 'Software developer in Lagos, 3 years experience, some savings'],
  ['Top-100 app in the App Store', 'I can code a little and have one app idea'],
  ['Run a marathon', 'I can run 5 km slowly'],
  ['Land a remote job abroad', 'Mid-level designer, employed locally'],
  ['Save $20k', 'Earning $2k/month, no savings yet'],
];

const data = loadData();
let sel = null;            // { type: 'node' | 'edge', id }
let busy = false;
let stopRequested = false;
let pulseId = null;
let lastPath = null;
let profileKey = '';
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
  document.body.classList.toggle('busy', on);
  $('#status').hidden = !on;
  $('#status').innerHTML = on ? `<span class="spin">✦</span> ${esc(label)}` : '';
  for (const id of ['#dreamBtn', '#searchBtn', '#newGoalBtn', '#detailPathBtn']) $(id).disabled = on;
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
  onTidy: () => { if (board()) { tidy(board()); persist(); refresh(); canvas.fit(); } },
});

function applyDisplay() {
  const d = settings().display;
  document.body.dataset.paper = d.paper;
  canvas.setMotion(d.motion);
}

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
    g: r.g, sel, weights: w, pulse: pulseId, display: settings().display,
  });

  $('#goalTitle').textContent = b.nodes[b.goalId].label;
  const d = settings().dreamer;
  $('#dreamerBadge').textContent = `${d}${d === 'claude' ? ' · ' + settings().claude.model.replace('claude-', '') : d === 'ollama' ? ' · ' + settings().ollama.model : d === 'groq' ? ' · ' + settings().groq.model.replace(/^.*\//, '') : ''}`;
  $('#boardDetail').value = b.detail || 'normal';
  $('#boardRoutes').value = b.routes || 'some';
  for (const k of ['constraints', 'timeframe', 'budget']) {
    const el = $(`#ctx [data-b="${k}"]`);
    if (document.activeElement !== el) el.value = b[k] || '';
  }
  renderProgress(b, r, w);
  renderProfile(b, r, w);
  renderPath(b, r, w);
  renderNext(b, w);
  renderPresets();
  if (inspector) renderInspector();
}

function renderBoardPick() {
  const boards = Object.values(data.boards).sort((a, b) => b.updated - a.updated);
  $('#boardPick').innerHTML = boards.map((b) => `<option value="${b.id}" ${b.id === data.currentId ? 'selected' : ''}>${esc(b.nodes[b.goalId]?.label || b.title)}</option>`).join('');
  $('#boardPick').hidden = !boards.length;
}

// ---------- side panel: progress, charts, lists ----------
function renderProgress(b, r, w) {
  const goalDone = b.nodes[b.goalId].done;
  const full = astar(b, w, { fromStart: true });
  let pct = goalDone ? 100 : r.found && full.found && full.cost > 0 ? Math.round(Math.max(0, Math.min(1, 1 - r.cost / full.cost)) * 100) : 0;
  if (!r.found && !goalDone) pct = 0;
  $('#progress').innerHTML = `
    <div class="pbar"><i style="width:${pct}%"></i></div>
    <div class="pmeta"><b>${pct}%</b> of the way${r.found && !goalDone ? ` · <span title="estimated from the time ratings">${esc(fmtDays(r.edges.reduce((s, id) => s + timeToDays(b.edges[id].cost?.time), 0)))} to go</span>` : ''}</div>`;
}

function renderProfile(b, r, w) {
  const box = $('#profile');
  if (!r.found || !r.edges.length || b.nodes[b.goalId].done) { box.hidden = true; return; }
  box.hidden = false;
  const edges = r.edges.map((id) => b.edges[id]);
  const ws = KEYS.reduce((s, k) => s + (w[k] ?? 1), 0) || 1;
  const W = 268, H = 92, gap = 4, bw = Math.max(6, Math.min(30, (W - gap * (edges.length - 1)) / edges.length));
  const max = Math.max(4, ...edges.map((e) => edgeCost(e, w)));
  let x = (W - (bw + gap) * edges.length + gap) / 2;
  let bars = '';
  edges.forEach((e, i) => {
    let y = H;
    for (const k of KEYS) {
      const v = ((w[k] ?? 1) * (e.cost?.[k] ?? 3)) / ws;
      const hgt = (v / max) * (H - 6);
      y -= hgt;
      bars += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${bw.toFixed(1)}" height="${Math.max(0, hgt).toFixed(1)}" class="seg-${k}" rx="1.5"><title>${i + 1}. ${esc(e.label)}\n${KEY_NAMES[k]}: ${e.cost?.[k] ?? 3}/10</title></rect>`;
    }
    bars += `<text x="${(x + bw / 2).toFixed(1)}" y="${H + 12}" class="ax">${i + 1}</text>`;
    x += bw + gap;
  });
  // Timeline: each step's share of the estimated calendar time.
  const days = edges.map((e) => timeToDays(e.cost?.time));
  const total = days.reduce((s, d) => s + d, 0) || 1;
  const anim = profileKey !== r.edges.join();
  profileKey = r.edges.join();
  const tl = edges.map((e, i) => `<span class="tl-${i % 2}" style="flex:${days[i] / total}" title="${i + 1}. ${esc(e.label)} — ${esc(durationText(e))}">${days[i] / total > 0.09 ? i + 1 : ''}</span>`).join('');
  box.innerHTML = `
    <h3>Path profile <span class="muted">cost per step</span></h3>
    <svg viewBox="0 0 ${W} ${H + 16}" class="chart${anim ? ' anim' : ''}" role="img" aria-label="Cost of each step on the best path">${bars}</svg>
    <div class="legend">${KEYS.map((k) => `<span><i class="seg-${k}"></i>${KEY_NAMES[k]}</span>`).join('')}</div>
    <div class="tl-head"><span>Timeline</span><span>≈ ${esc(fmtDays(total))}</span></div>
    <div class="timeline">${tl}</div>`;
}

function renderPath(b, r, w) {
  const list = $('#pathList');
  if (b.nodes[b.goalId].done) {
    list.innerHTML = '<li class="win">🎉 Goal achieved!</li>';
    $('#pathTotal').textContent = '';
    $('#detailPathBtn').hidden = true;
    return;
  }
  if (!r.found) {
    list.innerHTML = `<li class="muted">No path to the goal yet. Try <b>✦ Dream map</b> or <b>★ Search</b>, or select a state and link it onward.</li>`;
    $('#pathTotal').textContent = '';
    $('#detailPathBtn').hidden = true;
    return;
  }
  $('#detailPathBtn').hidden = false;
  list.innerHTML = r.edges.map((eid) => {
    const e = b.edges[eid], to = b.nodes[e.to], c = edgeCost(e, w), sd = stepsDone(e);
    return `<li data-edge="${eid}" class="${sel?.id === eid ? 'sel' : ''}">
      <div class="step">${esc(e.label)}</div>
      <div class="sub">→ ${esc(to.label)}</div>
      <div class="chips"><span class="cost" style="--c:${costColor(c)}">${fmt(c)}</span><span class="chip">⏱ ${esc(durationText(e))}</span>${sd ? `<span class="chip">☑ ${sd}</span>` : ''}</div>
    </li>`;
  }).join('');
  $('#pathTotal').textContent = `${r.edges.length} step${r.edges.length === 1 ? '' : 's'} · total cost ${fmt(r.cost)} · A* explored ${r.explored.length} states`;
}

function renderNext(b, w) {
  const items = nextActions(b, w).slice(0, 6);
  const onPath = new Set(lastPath?.edges || []);
  $('#nextList').innerHTML = items.length
    ? items.map(({ e, c }) => `<li data-edge="${e.id}" class="${onPath.has(e.id) ? 'best' : ''}">
        <button class="tick-sm" data-done="${e.to}" title="I did this">✓</button>
        <div><div class="step">${onPath.has(e.id) ? '<span class="star-i">★</span> ' : ''}${esc(e.label)}</div>
        <div class="chips"><span class="cost" style="--c:${costColor(c)}">${fmt(c)}</span><span class="chip">⏱ ${esc(durationText(e))}</span></div></div>
      </li>`).join('')
    : '<li class="muted">Nothing available from where you are. Dream or add states.</li>';
}

function renderWeights() {
  const w = settings().weights;
  $('#weights').innerHTML = KEYS.map((k) => `
    <label><span><i class="dot seg-${k}"></i>${KEY_NAMES[k]}</span><input type="range" min="0" max="3" step="0.5" value="${w[k]}" data-w="${k}"><output>${w[k]}</output></label>`).join('');
}

function renderPresets() {
  const w = settings().weights;
  $('#presets').innerHTML = Object.entries(PRESETS).map(([name, p]) =>
    `<button class="chipbtn ${KEYS.every((k) => p[k] === w[k]) ? 'on' : ''}" data-preset="${name}">${name}</button>`).join('');
}

// ---------- inspector ----------
function select(s) {
  sel = s;
  refresh();
}

function edgeRow(b, e, dir) {
  const other = b.nodes[dir === 'in' ? e.from : e.to];
  return `<li data-goedge="${e.id}"><span class="step">${esc(e.label)}</span><span class="sub">${dir === 'in' ? 'from' : '→'} ${esc(other?.label || '?')}</span></li>`;
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
    const ins = Object.values(b.edges).filter((e) => e.to === n.id);
    const outs = Object.values(b.edges).filter((e) => e.from === n.id);
    el.innerHTML = `
      <div class="ins-head"><span class="kind k-${n.kind}">${n.kind === 'goal' ? '★ Goal' : n.kind === 'start' ? '● Where you are' : 'State'}</span><button class="icon close" data-act="close" title="Close (Esc)">×</button></div>
      <label>State <textarea data-f="label" rows="2">${esc(n.label)}</textarea></label>
      <label>Notes <textarea data-f="note" rows="4" placeholder="Details, links, numbers…">${esc(n.note)}</textarea></label>
      ${n.kind === 'goal' || n.kind === 'start' ? '' : `
        <div class="grid2">
          <label>h (cost left) <input type="number" step="0.5" min="0" data-f="h" value="${n.h ?? ''}"></label>
          <label class="row ach"><input type="checkbox" data-f="done" ${n.done ? 'checked' : ''}> Achieved</label>
        </div>`}
      <div class="muted small">${g != null ? `g (cost so far) ${fmt(g)}` : 'not reachable from where you are yet'}</div>
      <div class="btns">
        ${n.kind === 'goal' ? '' : `<button class="dream primary" data-act="expand" ${busy ? 'disabled' : ''}>✦ Dream next states</button>`}
        ${n.kind === 'goal' ? '' : '<button data-act="link">Link → state</button>'}
        ${n.kind === 'goal' ? '' : '<button data-act="child">+ Next state</button>'}
        <button data-act="center">Center</button>
        ${n.kind === 'state' ? '<button data-act="delete" class="danger">Delete</button>' : ''}
      </div>
      ${ins.length ? `<h4>Leads here (${ins.length})</h4><ul class="rel">${ins.map((e) => edgeRow(b, e, 'in')).join('')}</ul>` : ''}
      ${outs.length ? `<h4>From here (${outs.length})</h4><ul class="rel">${outs.map((e) => edgeRow(b, e, 'out')).join('')}</ul>` : ''}`;
  } else {
    const e = b.edges[sel.id];
    const w = settings().weights;
    const steps = e.steps || [];
    const allDone = steps.length && steps.every((s) => s.done) && !b.nodes[e.to].done;
    const slider = (k, hint) => `<label class="slider"><span><i class="dot seg-${k}"></i>${k}</span><input type="range" min="0" max="10" step="1" data-c="${k}" value="${e.cost[k] ?? 3}"><output>${e.cost[k] ?? 3}</output><span class="muted small">${hint}</span></label>`;
    el.innerHTML = `
      <div class="ins-head"><span class="kind">Action</span><button class="icon close" data-act="close" title="Close (Esc)">×</button></div>
      <div class="fromto"><span>${esc(b.nodes[e.from].label)}</span><b>→</b><span>${esc(b.nodes[e.to].label)}</span></div>
      <label>Action <textarea data-f="label" rows="2">${esc(e.label)}</textarea></label>
      <label>Notes <textarea data-f="note" rows="3" placeholder="How, where, who, links…">${esc(e.note)}</textarea></label>
      <div class="checklist">
        <h4>Checklist ${steps.length ? `<span class="muted">${stepsDone(e)}</span>` : ''}</h4>
        ${steps.map((s, i) => `<div class="ck ${s.done ? 'on' : ''}"><input type="checkbox" data-step="${i}" ${s.done ? 'checked' : ''} aria-label="done"><textarea class="ck-t" data-steptext="${i}" rows="1">${esc(s.text)}</textarea><button class="icon ck-x" data-act="delstep" data-i="${i}" title="Remove">×</button></div>`).join('')}
        <input class="ck-add" placeholder="+ add a step, press Enter">
        ${allDone ? '<button data-act="done" class="ok-btn">✓ All steps done — mark reached</button>' : ''}
      </div>
      <label>Duration <input data-f="duration" value="${esc(e.duration || '')}" placeholder="${esc(durationText({ cost: e.cost }))} (from the time rating)"></label>
      ${slider('time', 'week≈3 · month≈5 · 6 mo≈7 · years=10')}
      ${slider('money', 'month of income≈5')}
      ${slider('effort', '')}
      ${slider('risk', 'chance it fails')}
      <div class="muted small">cost with your weights: <b id="edgeCostOut">${fmt(edgeCost(e, w))}</b>${e.by ? ` · dreamed by ${esc(e.by)}` : ''}</div>
      <div class="btns">
        <button class="dream primary" data-act="detail" ${busy ? 'disabled' : ''} title="Ask the dreamer for a checklist, duration and specifics">✦ Add detail</button>
        <button class="dream" data-act="breakdown" ${busy ? 'disabled' : ''} title="Replace this action with a chain of smaller ones">✦ Break down</button>
        <button data-act="done">✓ I did this</button>
        <button data-act="delete" class="danger">Delete</button>
      </div>`;
    for (const t of el.querySelectorAll('.ck-t')) grow(t);
  }
}

// Checklist items wrap onto as many lines as they need.
function grow(t) {
  t.style.height = 'auto';
  t.style.height = `${t.scrollHeight}px`;
}

$('#inspector').addEventListener('input', (ev) => {
  const b = board();
  const t = ev.target;
  if (!sel || !b) return;
  const obj = sel.type === 'node' ? b.nodes[sel.id] : b.edges[sel.id];
  let full = false;
  if (['label', 'note', 'duration'].includes(t.dataset.f)) obj[t.dataset.f] = t.value;
  else if (t.dataset.f === 'h') obj.h = t.value === '' ? null : Math.max(0, Number(t.value));
  else if (t.dataset.f === 'done') { obj.done = t.checked; full = true; if (t.checked) canvas.burst(obj.id, 14); }
  else if (t.dataset.step != null) { obj.steps[t.dataset.step].done = t.checked; full = true; }
  else if (t.dataset.steptext != null) { obj.steps[t.dataset.steptext].text = t.value; grow(t); }
  else if (t.dataset.c) {
    obj.cost[t.dataset.c] = Number(t.value);
    t.nextElementSibling.textContent = t.value;
    $('#edgeCostOut').textContent = fmt(edgeCost(obj, settings().weights));
  } else return;
  if (sel.type === 'node' && obj.kind === 'goal' && t.dataset.f === 'label') b.title = obj.label;
  persist();
  refresh({ inspector: full });
});

$('#inspector').addEventListener('keydown', (ev) => {
  if (!ev.target.classList.contains('ck-add') || ev.key !== 'Enter') return;
  const text = ev.target.value.trim();
  const e = board()?.edges[sel?.id];
  if (!text || !e) return;
  (e.steps ||= []).push({ text, done: false });
  persist();
  refresh();
  $('#inspector .ck-add')?.focus();
});

$('#inspector').addEventListener('click', async (ev) => {
  const go = ev.target.closest('[data-goedge]');
  if (go) { select({ type: 'edge', id: go.dataset.goedge }); return; }
  const btn = ev.target.closest('[data-act]');
  const act = btn?.dataset.act;
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
    if (act === 'detail') { await detailEdge(e.id); refresh(); }
    if (act === 'breakdown') { await breakdownEdge(e.id); refresh(); }
    if (act === 'done') toggleDone(e.to, true);
    if (act === 'delstep') { e.steps.splice(Number(btn.dataset.i), 1); persist(); refresh(); }
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
  const e = { id: uid('e'), from, to, label: 'New action', note: '', cost: { time: 3, money: 3, effort: 3, risk: 3 }, duration: '', steps: [] };
  b.edges[e.id] = e;
  persist();
  select({ type: 'edge', id: e.id });
  const ta = $('#inspector textarea[data-f="label"]');
  ta?.focus();
  ta?.select();
}

function toggleDone(id, value) {
  const b = board();
  const n = b.nodes[id];
  if (!n || n.kind === 'start') return;
  n.done = value ?? !n.done;
  persist();
  refresh();
  if (n.done) {
    toast(n.kind === 'goal' ? '🎉 Goal achieved!' : `✓ ${n.label}`);
    canvas.burst(id, n.kind === 'goal' ? 48 : 16);
  }
}

// ---------- dreaming ----------
function request(mode, focus = null) {
  const b = board();
  const s = settings();
  const detail = b.detail || s.detail;
  return {
    mode,
    goal: { label: b.nodes[b.goalId].label, note: b.nodes[b.goalId].note },
    start: { label: b.nodes[b.startId].label, note: b.nodes[b.startId].note },
    constraints: b.constraints || '',
    timeframe: b.timeframe || '',
    budget: b.budget || '',
    focus,
    existing: Object.values(b.nodes).slice(0, 80).map((n) => ({ id: n.id, label: n.label, kind: n.kind, done: !!n.done })),
    params: { maxStates: DETAIL_STATES[detail] || 8, detail, routes: b.routes || s.routes, weights: s.weights },
  };
}

async function dream(req, ctx, label, near) {
  const b = board();
  setBusy(true, label);
  canvas.setDreaming(near);
  try {
    const { result, by, warning } = await generate(settings(), req);
    const added = applyDream(b, result, { ...ctx, by });
    estimateMissingH(b, settings().weights);
    placeNew(b, added.nodes);
    log(added.updated ? `${by}: added detail to “${b.edges[added.edges[0]].label}”` : `${by}: ${req.mode} → +${added.nodes.length} states, +${added.edges.length} actions`);
    if (warning) { toast(warning, 'err'); log(warning); }
    persist();
    return added;
  } catch (err) {
    console.error(err);
    toast(`Dream failed: ${err.message}`, 'err');
    log(`failed: ${err.message}`);
    return null;
  } finally {
    canvas.setDreaming(null);
    setBusy(false);
  }
}

async function dreamMap() {
  const b = board();
  if (!b || busy) return;
  if (Object.keys(b.edges).length && !confirm('Dream a fresh map onto this board? Existing states are kept; matching ones are merged.')) return;
  const added = await dream(request('dream'), {}, 'dreaming a map…', b.startId);
  if (added) await afterDream(b);
}

// Lay out a fresh map; if the dreamer left a gap before the goal, let ★ Search fill it.
async function afterDream(b) {
  tidy(b);
  persist();
  refresh();
  canvas.fit();
  const r = astar(b, settings().weights);
  if (r.found) setTimeout(() => canvas.scan(r.explored), 500);
  else {
    log('map doesn’t reach the goal yet — running ★ Search');
    await search();
  }
}

// mode 'bridge' asks the dreamer to finish the route from this state to the goal.
async function expandNode(id, mode = 'expand') {
  const b = board();
  const n = b.nodes[id];
  const what = mode === 'bridge' ? 'bridging' : 'expanding';
  const added = await dream(request(mode, { node: { id, label: n.label, note: n.note, h: n.h } }), { hereId: id }, `${what} “${n.label.slice(0, 30)}”…`, id);
  if (added) n.expanded = true;
  return added;
}

const edgeFocus = (b, e) => ({ edge: { label: e.label, note: e.note, from: b.nodes[e.from].label, to: b.nodes[e.to].label, cost: e.cost, steps: (e.steps || []).map((s) => s.text) } });

async function breakdownEdge(eid) {
  const b = board();
  const e = b.edges[eid];
  const added = await dream(request('breakdown', edgeFocus(b, e)), { fromId: e.from, toId: e.to, replaceEdgeId: eid }, 'breaking it down…', e.from);
  if (added && !b.edges[eid]) sel = null;
  return added;
}

async function detailEdge(eid) {
  const b = board();
  const e = b.edges[eid];
  return dream(request('detail', edgeFocus(b, e)), { fromId: e.from, toId: e.to, updateEdgeId: eid }, `adding detail to “${e.label.slice(0, 28)}”…`, e.from);
}

// Flesh out every step on the best path that has no checklist yet.
async function detailPath() {
  const b = board();
  if (!b || busy || !lastPath?.found) return;
  const todo = lastPath.edges.filter((id) => !b.edges[id]?.steps?.length);
  if (!todo.length) { toast('Every step on the path already has a checklist — use ✦ Add detail on one to redo it'); return; }
  stopRequested = false;
  $('#stopBtn').hidden = false;
  let n = 0;
  for (const id of todo) {
    if (stopRequested || !b.edges[id]) break;
    sel = { type: 'edge', id };
    refresh();
    canvas.centerOn(b.edges[id].to);
    if (!(await detailEdge(id))) break;
    n++;
    refresh();
  }
  $('#stopBtn').hidden = true;
  toast(`Added detail to ${n} step${n === 1 ? '' : 's'}`);
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
    canvas.scan(r.explored);
    canvas.centerOn(id);
    // Close to the goal (or running out of budget): ask for the rest of the route instead of more branches.
    const hTop = Math.max(0, ...Object.values(b.nodes).filter((n) => n.kind === 'state').map((n) => n.h).filter(Number.isFinite));
    const near = hTop > 0 && h(id) <= hTop * 0.35;
    const mode = b.nodes[id].kind === 'state' && (near || i >= settings().searchBudget / 2) ? 'bridge' : 'expand';
    log(`★ ${mode === 'bridge' ? 'bridging' : 'expanding'} “${b.nodes[id].label}” (f = ${fmt(r.g.get(id) + h(id))})`);
    const added = await expandNode(id, mode);
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
  f.elements.detail.value = settings().detail;
  f.elements.routes.value = settings().routes;
  $('#newGoalDlg').returnValue = '';
  $('#newGoalDlg').showModal();
}

$('#examples').innerHTML = EXAMPLES.map(([g], i) => `<button type="button" class="chipbtn" data-ex="${i}">${esc(g)}</button>`).join('');
$('#examples').addEventListener('click', (e) => {
  const i = e.target.closest('[data-ex]')?.dataset.ex;
  if (i == null) return;
  const f = $('#newGoalForm');
  [f.elements.goal.value, f.elements.context.value] = EXAMPLES[i];
});

$('#newGoalDlg').addEventListener('close', async () => {
  if ($('#newGoalDlg').returnValue !== 'ok') return;
  const f = new FormData($('#newGoalForm'));
  const val = (k) => String(f.get(k) || '').trim();
  const goal = val('goal');
  if (!goal) return;
  const b = createBoard({
    goal, context: val('context'), constraints: val('constraints'), timeframe: val('timeframe'), budget: val('budget'),
    detail: val('detail') || settings().detail, routes: val('routes') || settings().routes,
  });
  data.boards[b.id] = b;
  data.currentId = b.id;
  sel = null;
  persist();
  refresh();
  canvas.fit(false);
  if (f.get('dream')) {
    const added = await dream(request('dream'), {}, 'dreaming a map…', b.startId);
    if (added) await afterDream(b);
  }
});

function switchBoard(id) {
  data.currentId = id;
  sel = null;
  canvas.setLinkMode(null);
  persist({ touch: false });
  refresh();
  canvas.fit(false);
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

function readSettingsForm(prefix = '') {
  for (const el of $('#settingsForm').elements) {
    if (!el.name || !el.name.startsWith(prefix) || (el.type === 'radio' && !el.checked)) continue;
    let v = el.type === 'checkbox' ? el.checked : el.value.trim();
    if (el.type === 'number') v = Math.max(Number(el.min) || 1, Math.min(Number(el.max) || 99, Number(v) || 1));
    setPath(settings(), el.name, v);
  }
}

$('#settingsDlg').addEventListener('close', () => {
  if ($('#settingsDlg').returnValue !== 'ok') return;
  readSettingsForm();
  persist({ touch: false });
  applyDisplay();
  refresh();
  toast('Settings saved');
});

// ---------- sync / import / export ----------
async function syncNow(quiet = false) {
  const g = settings().gist;
  if (!g.token) { if (!quiet) { toast('Add a GitHub token in Settings → Cloud sync'); if (!$('#settingsDlg').open) openSettings(); } return; }
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
    if (!g.id) {
      g.id = id;
      $('#settingsForm').elements['gist.id'].value = id;
      toast(`Created secret gist ${id} — paste this id on your other devices`);
    }
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
$('#detailPathBtn').addEventListener('click', detailPath);
$('#stopBtn').addEventListener('click', () => { stopRequested = true; });
$('#settingsBtn').addEventListener('click', openSettings);
$('#syncBtn').addEventListener('click', () => syncNow(false));
$('#syncNowBtn').addEventListener('click', () => { readSettingsForm('gist.'); persist({ touch: false }); syncNow(false); });
$('#sideToggle').addEventListener('click', () => document.body.classList.toggle('side-open'));

$('#boardDetail').addEventListener('change', (e) => { board().detail = e.target.value; persist(); });
$('#boardRoutes').addEventListener('change', (e) => { board().routes = e.target.value; persist(); });
$('#ctx').addEventListener('input', (e) => {
  const k = e.target.dataset.b;
  if (k && board()) { board()[k] = e.target.value; persist(); }
});

$('#deleteBoardBtn').addEventListener('click', () => {
  const b = board();
  if (!b || !confirm(`Delete “${b.nodes[b.goalId].label}”? This can't be undone (unless it's in a sync/export).`)) return;
  delete data.boards[b.id];
  data.deleted[b.id] = now();
  data.currentId = Object.values(data.boards).sort((x, y) => y.updated - x.updated)[0]?.id || null;
  sel = null;
  persist({ touch: false });
  refresh();
  canvas.fit(false);
});

$('#weights').addEventListener('input', (e) => {
  const k = e.target.dataset.w;
  if (!k) return;
  settings().weights[k] = Number(e.target.value);
  e.target.nextElementSibling.textContent = e.target.value;
  persist({ touch: false });
  refresh({ inspector: false });
});

$('#presets').addEventListener('click', (e) => {
  const p = PRESETS[e.target.closest('[data-preset]')?.dataset.preset];
  if (!p) return;
  settings().weights = { ...p };
  renderWeights();
  persist({ touch: false });
  refresh({ inspector: false });
});

for (const id of ['#pathList', '#nextList']) {
  $(id).addEventListener('click', (e) => {
    const done = e.target.closest('[data-done]');
    if (done) return toggleDone(done.dataset.done, true);
    const li = e.target.closest('[data-edge]');
    if (li) { select({ type: 'edge', id: li.dataset.edge }); canvas.centerOn(board().edges[li.dataset.edge].to); document.body.classList.remove('side-open'); }
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
  if (e.key === '+' || e.key === '=') canvas.zoomBy(1.25);
  if (e.key === '-') canvas.zoomBy(0.8);
});

window.addEventListener('resize', () => board() && canvas.drawMinimapSoon());

// ---------- boot ----------
if (!data.boards[data.currentId]) data.currentId = Object.keys(data.boards)[0] || null;
applyDisplay();
renderWeights();
refresh();
canvas.fit(false);
if (settings().gist.auto && settings().gist.token && settings().gist.id) syncNow(true);
