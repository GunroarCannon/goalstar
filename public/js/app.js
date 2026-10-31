import { walrusMemory } from './walrus-memory.js';

import { tatumSui } from './tatum-sui.js';

import { WorkflowWatchdog } from './watchdog.js';

import { loadData, saveData, createBoard, applyDream, deleteNode, uid, now, DETAIL_STATES } from './model.js';

import { astar, edgeCost, nextActions, heuristic, estimateMissingH, timeToDays, fmtDays } from './astar.js';

import { tidy, placeNew, COL } from './layout.js';

import { Canvas, esc, costColor, durationText, stepsDone } from './render.js';

import { generate } from './dreamers/index.js';

import * as gist from './sync.js';

import { sound } from './sound.js';

import { theme } from './theme.js';

import { auth } from './auth.js';

import { initTooltips, askConfirm } from './tooltip.js';

import { initAgentChat } from './chat.js';



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

const watchdog = new WorkflowWatchdog(walrusMemory);

const frictionFn = (lbl) => walrusMemory.getFrictionPenalty(lbl);

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

  window.toast = toast;

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

  $('#status').innerHTML = on ? `<span class="spin">*</span> ${esc(label)}` : '';

  for (const id of ['#dreamBtn', '#searchBtn', '#newGoalBtn', '#detailPathBtn']) $(id).disabled = on;

  for (const b of document.querySelectorAll('.inspector .dream')) b.disabled = on;

}



// ---------- canvas ----------

const canvas = new Canvas($('#canvas'), {

  onSelect: (s) => select(s),

  onBackgroundClick: () => {

    if (canvas.linkFrom) { canvas.setLinkMode(null); updateLinkBanner(null); updateLinkBanner(null); toast('Connect cancelled'); }

    select(null);

  },

  onBackgroundDblClick: (x, y) => addState(x, y),

  onNodeMoved: () => persist(),

  onEdgeMoved: () => persist(),

  onToggleDone: (id) => toggleDone(id),
  onAttachChild: (id) => attachChild(id),
  onLinkBackgroundClick: (fromId, x, y) => attachChild(fromId, x, y),

  onLink: (from, to) => link(from, to),

  onTidy: () => { if (board()) { tidy(board()); persist(); refresh(); canvas.fit(); } },

});



export const FONT_MAP = {
  hand: "'Patrick Hand', 'Segoe Print', cursive",
  sans: "'Space Grotesk', system-ui, -apple-system, sans-serif",
  marker: "'Caveat', cursive",
  mono: "'Courier Prime', monospace",
  serif: "'Playfair Display', Georgia, serif",
  typewriter: "'Special Elite', monospace",
  system: "system-ui, -apple-system, sans-serif"
};

function applyDisplay() {

  const d = settings().display;

  // The preset is the source of truth: palette + component skin live together.

  theme.applyTheme(theme.currentPreset || 'notebook');

  d.paper = document.body.dataset.paper || d.paper;

  canvas.setMotion(d.motion);
  const fontChoice = d.font || 'hand';
  const selectedFont = FONT_MAP[fontChoice] || FONT_MAP.hand;
  document.documentElement.style.setProperty('--hand', selectedFont);
  document.documentElement.style.setProperty('--map-font', selectedFont);
  const glow = !!d.arrowGlow;
  document.body.classList.toggle('arrow-glow', glow);
  try { localStorage.setItem('goalstar_arrow_glow', glow ? 'true' : 'false'); } catch (e) {}

}



function refresh({ inspector = true } = {}) {

  const b = board();

  $('#empty').hidden = !!b;

  document.body.classList.toggle('no-board', !b);

  renderBoardPick();

  if (!b) { $('#inspector').hidden = true; return; }



  const w = settings().weights;

  const r = astar(b, w, { frictionFn });

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



  const stateNodes = Object.values(b.nodes).filter(n => n.kind === 'state');

  const doneStates = stateNodes.filter(n => n.done).length;

  const allEdges = Object.values(b.edges);

  const totalSteps = allEdges.reduce((sum, e) => sum + (e.steps?.length || 0), 0);

  const doneSteps = allEdges.reduce((sum, e) => sum + (e.steps?.filter(s => s.done).length || 0), 0);



  let pct = 0;

  if (goalDone) {

    pct = 100;

  } else if (stateNodes.length > 0) {

    const stateRatio = doneStates / stateNodes.length;

    const stepRatio = totalSteps > 0 ? (doneSteps / totalSteps) : stateRatio;

    const pathRatio = r.found && full.found && full.cost > 0 ? Math.max(0, Math.min(1, 1 - r.cost / full.cost)) : 0;

    pct = Math.round((stateRatio * 0.4 + stepRatio * 0.35 + pathRatio * 0.25) * 100);

    pct = Math.max(0, Math.min(99, pct));

  } else {

    pct = r.found && full.found && full.cost > 0 ? Math.round(Math.max(0, Math.min(1, 1 - r.cost / full.cost)) * 100) : 0;

  }

  if (!r.found && !goalDone && doneStates === 0 && doneSteps === 0) pct = 0;



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

    list.innerHTML = '<li class="win">Goal achieved!</li>';

    $('#pathTotal').textContent = '';

    $('#detailPathBtn').hidden = true;

    return;

  }

  if (!r.found) {

    list.innerHTML = `<li class="muted">No path to the goal yet. Try <b>Dream map</b> or <b>Search</b>, or select a state and link it onward.</li>`;

    $('#pathTotal').textContent = '';

    $('#detailPathBtn').hidden = true;

    return;

  }

  $('#detailPathBtn').hidden = false;

  list.innerHTML = r.edges.map((eid) => {

    const e = b.edges[eid], to = b.nodes[e.to], c = edgeCost(e, w), sd = stepsDone(e);

    return `<li data-edge="${eid}" class="${sel?.id === eid ? 'sel' : ''}">

      <div class="step" title="${esc(e.note || e.label)}">${esc(e.label)}</div>

      <div class="sub">→ ${esc(to.label)}</div>

      <div class="chips"><span class="cost" style="--c:${costColor(c)}">${fmt(c)}</span><span class="chip">${esc(durationText(e))}</span>${sd ? `<span class="chip"> ${sd}</span>` : ''}</div>

    </li>`;

  }).join('');

  $('#pathTotal').textContent = `${r.edges.length} step${r.edges.length === 1 ? '' : 's'} · total cost ${fmt(r.cost)} · A* explored ${r.explored.length} states`;

}



function renderNext(b, w) {

  const items = nextActions(b, w).slice(0, 6);

  const onPath = new Set(lastPath?.edges || []);

  $('#nextList').innerHTML = items.length

    ? items.map(({ e, c }) => `<li data-edge="${e.id}" class="${onPath.has(e.id) ? 'best' : ''}">

        <button class="tick-sm" data-done="${e.to}" title="I did this" aria-label="I did this"><svg viewBox="0 0 12 12" width="10" height="10" aria-hidden="true"><path d="M2 6.2 L4.8 9 L10 3.2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>

        <div><div class="step">${onPath.has(e.id) ? '<span class="star-i">*</span> ' : ''}${esc(e.label)}</div>

        <div class="chips"><span class="cost" style="--c:${costColor(c)}">${fmt(c)}</span><span class="chip">${esc(durationText(e))}</span></div></div>

      </li>`).join('')

    : '<li class="muted">Nothing available from where you are. Dream or add states.</li>';

}



function renderWeights() {

  const w = settings().weights;

  $('#weights').innerHTML = KEYS.map((k) => `

    <label><span><i class="dot seg-${k}"></i>${KEY_NAMES[k]}</span><input type="range" min="0" max="3" step="0.5" value="${w[k]}" data-w="${k}" title="How much ${KEY_NAMES[k].toLowerCase()} should count when A* prices every action (0 = ignore)"><output>${w[k]}</output></label>`).join('');

}



function renderPresets() {

  const w = settings().weights;

  $('#presets').innerHTML = Object.entries(PRESETS).map(([name, p]) =>

    `<button class="chipbtn ${KEYS.every((k) => p[k] === w[k]) ? 'on' : ''}" data-preset="${name}" title="Re-price the whole map to favour ${name.toLowerCase()} routes">${name}</button>`).join('');

}



// ---------- inspector ----------

let lastClickedNodeId = null;



function select(s) {

  if (s && s.type === 'node') {

    lastClickedNodeId = s.id;

    if (window.agentChat && window.agentChat.isOpen && window.agentChat.isOpen()) {

      window.agentChat.close();

    }

  }

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

      <div class="ins-head">

        <span class="kind k-${n.kind}">${n.kind === 'goal' ? 'Goal' : n.kind === 'start' ? ' Where you are' : 'State'}</span>

        <div style="display:flex; align-items:center; gap:8px;">

          <button class="ins-guide-btn" data-act="ins-guide" title="Show guide for this inspector" style="font-family:'Space Grotesk',sans-serif; font-size:12px; font-weight:700; padding:2px 8px; border-radius:6px; border:1px solid var(--accent); background:var(--panel-2); color:var(--accent); cursor:pointer;"><span style="color:var(--accent); font-weight:800;">?</span> Guide</button>

          <button class="icon close" data-act="close" title="Close (Esc)">×</button>

        </div>

      </div>

      <label>State <textarea data-f="label" rows="2">${esc(n.label)}</textarea></label>

      <label>Notes & Resources <span class="muted small">(links, attachments, contacts)</span> <textarea data-f="note" rows="3" placeholder="Details, links, numbers…">${esc(n.note)}</textarea></label>

      <div style="margin-top:-4px; margin-bottom:8px;"><button type="button" class="mini-add-link-btn" data-act="add-link-template" title="Insert a markdown link into Notes for a document, form, contact or website" style="font-size:11px; padding:2px 8px; border-radius:4px; border:1px dashed var(--ink); background:transparent; cursor:pointer; color:var(--ink);">+ Add link to Notes</button></div>

      ${n.kind === 'goal' || n.kind === 'start' ? '' : `

        <div class="grid2">

          <label>h (cost left) <input type="number" step="0.5" min="0" data-f="h" value="${n.h ?? ''}"></label>

          <label class="row ach"><input type="checkbox" data-f="done" ${n.done ? 'checked' : ''}> Achieved</label>

        </div>`}

      <div class="muted small">${g != null ? `g (cost so far) ${fmt(g)}` : 'not reachable from where you are yet'}</div>

      <div class="btns">

        ${n.kind === 'goal' ? '' : `<button class="dream primary" data-act="expand" ${busy ? 'disabled' : ''}>* Dream next states</button>`}

        ${n.kind === 'goal' ? '' : '<button data-act="link" title="Draw an action connector to another milestone">Connect to Milestone →</button>'}

        ${n.kind === 'goal' ? '' : '<button data-act="child" class="primary engraved-btn" style="margin-bottom:6px; width:100%; font-weight:700;" title="Create a new milestone connected directly to this one">+ Attach Next Milestone</button>'}

        <button data-act="center" title="Bring this milestone back to the middle of the canvas">Center</button>

        ${n.kind === 'state' ? '<button data-act="delete" class="danger" title="Delete this milestone and every action attached to it">Delete</button>' : ''}

      </div>

      ${ins.length ? `<h4>Leads here (${ins.length})</h4><ul class="rel">${ins.map((e) => edgeRow(b, e, 'in')).join('')}</ul>` : ''}

      ${outs.length ? `<h4>From here (${outs.length})</h4><ul class="rel">${outs.map((e) => edgeRow(b, e, 'out')).join('')}</ul>` : ''}

      ${n.kind === 'state' ? `

      <div class="block-box ${n.blocked ? 'on' : ''}">

        <div class="block-head">

          <b>Route control</b>

          <span class="block-state ${n.blocked ? n.blocked.level : ''}">${n.blocked ? (n.blocked.level === 'impossible' ? 'Out of reach' : 'Very expensive') : 'Open'}</span>

        </div>

        <div class="muted small">Facts change: a refusal, a closed program, no money, no time. Mark this milestone so A* stops routing through it.</div>

        <input data-f="blockReason" placeholder="Why? e.g. visa refused, cohort closed, need $8k" value="${esc(n.blockReason || '')}">

        <div class="row gap">

          <button data-act="block-expensive" title="Keep it on the map but make every route through it cost 2.5× more">Very expensive</button>

          <button data-act="block-impossible" class="danger" title="Drop it from every route without deleting the card">Out of reach</button>

          ${n.blocked ? '<button data-act="unblock">Reopen route</button>' : ''}

        </div>

      </div>

      <div class="sui-box">

        <div style="font-family:'Space Grotesk',sans-serif; font-size:13px; font-weight:700; color:var(--ink); display:flex; align-items:center; justify-content:space-between;">

          <span>Cryptographic Proof</span>

          <span style="font-size:10px; font-weight:700; text-transform:uppercase; color:#0284c7; background:rgba(2,132,199,0.1); border:1px solid rgba(2,132,199,0.3); padding:1px 6px; border-radius:4px;">Sui Mainnet</span>

        </div>

        <div style="font-size:11.5px; color:var(--muted); line-height:1.4; margin:5px 0 8px;">

          Verifiable Milestone Proof: Cryptographically anchored to Sui Mainnet via Tatum RPC gateway with immutable verification.

        </div>

        <button class="sui-stamp-btn" data-act="sui-stamp" data-nodeid="${n.id}" style="width:100%;">${n.done ? 'Stamp Verified Milestone on Sui (Tatum)' : 'Stamp Milestone Proof on Sui (Tatum)'}</button>

      </div>` : ''}

      ${!n.done && n.kind === 'state' ? `<button class="mini-btn" style="width: 100%; margin-top: 10px; background: #6366f1;" data-act="auto-decompose" data-nodeid="${n.id}"> Apply Learned Escalation: Decompose</button>` : ''}`;

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

      <label>Notes & Resources <span class="muted small">(how, where, who, links)</span> <textarea data-f="note" rows="3" placeholder="How, where, who, links…">${esc(e.note)}</textarea></label>

      <div style="margin-top:-4px; margin-bottom:8px;"><button type="button" class="mini-add-link-btn" data-act="add-link-template" title="Insert a markdown link into Notes for a document, form, contact or website" style="font-size:11px; padding:2px 8px; border-radius:4px; border:1px dashed var(--ink); background:transparent; cursor:pointer; color:var(--ink);">+ Add link to Notes</button></div>

      <div class="checklist">

        <h4>Checklist ${steps.length ? `<span class="muted">${stepsDone(e)}</span>` : ''}</h4>

        ${steps.map((s, i) => `<div class="ck ${s.done ? 'on' : ''}"><input type="checkbox" data-step="${i}" ${s.done ? 'checked' : ''} aria-label="done"><textarea class="ck-t" data-steptext="${i}" rows="1">${esc(s.text)}</textarea><button class="icon ck-x" data-act="delstep" data-i="${i}" title="Remove">×</button></div>`).join('')}

        <input class="ck-add" placeholder="+ add a step, press Enter">

        ${allDone ? '<button data-act="done" class="ok-btn">All steps done — mark reached</button>' : ''}

      </div>

      <label>Duration <input data-f="duration" value="${esc(e.duration || '')}" placeholder="${esc(durationText({ cost: e.cost }))} (from the time rating)"></label>

      ${slider('time', 'week≈3 · month≈5 · 6 mo≈7 · years=10')}

      ${slider('money', 'month of income≈5')}

      ${slider('effort', '')}

      ${slider('risk', 'chance it fails')}

      <div class="muted small">cost with your weights: <b id="edgeCostOut">${fmt(edgeCost(e, w))}</b>${e.by ? ` · dreamed by ${esc(e.by)}` : ''}</div>

      <div class="btns">

        <button class="dream primary" data-act="detail" ${busy ? 'disabled' : ''} title="Ask the dreamer for a checklist, duration and specifics">Add detail</button>

        <button class="dream" data-act="breakdown" ${busy ? 'disabled' : ''} title="Replace this action with a chain of smaller ones">* Break down</button>

        <button data-act="done" title="Mark the milestone this action leads to as reached">I did this</button>

        <button data-act="delete" class="danger" title="Remove this action connector only">Delete</button>

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

  else if (t.dataset.f === 'blockReason') obj.blockReason = t.value;

  if (t.dataset.f === 'note') rememberNote(obj, t.value);

  else if (t.dataset.f === 'h') obj.h = t.value === '' ? null : Math.max(0, Number(t.value));

  else if (t.dataset.f === 'done') { obj.done = t.checked; full = true; if (t.checked) canvas.burst(obj.id, 14); }

  else if (t.dataset.step != null) {

    const sIdx = Number(t.dataset.step);

    if (obj.steps && obj.steps[sIdx]) {

      obj.steps[sIdx].done = t.checked;

      full = true;

      if (t.checked) sound.play('pop');

      const toNode = b.nodes[obj.to];

      if (toNode) {

        const allDone = obj.steps.length > 0 && obj.steps.every(s => s.done);

        if (allDone && !toNode.done) {

          toNode.done = true;

          canvas.burst(toNode.id, 16);

          sound.play('ding');

        } else if (!allDone && toNode.done) {

          toNode.done = false;

        }

      }

    }

  }

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

    if (act === 'add-link-template') {

      const ta = $('#inspector textarea[data-f="note"]');

      const target = sel.type === 'node' ? b.nodes[sel.id] : b.edges[sel.id];

      if (ta && target) {

        const label = 'Resource name';

        const insert = `[${label}](https://example.com)`;

        const cur = ta.value.trim();

        ta.value = cur ? `${cur}\n${insert}` : insert;

        target.note = ta.value;

        persist();

        refresh({ inspector: false });

        // Put the cursor on the placeholder so the next keystroke replaces it.

        const at = ta.value.lastIndexOf(label);

        ta.focus();

        if (at >= 0) ta.setSelectionRange(at, at + label.length);

        toast('Link template inserted in Notes — replace “Resource name” and the URL');

      }

      return;

    }

  if (sel.type === 'node') {

    const id = sel.id;

    if (act === 'expand') { await expandNode(id); refresh(); }

    if (act === 'link') { canvas.setLinkMode(id); updateLinkBanner(id); toast('Click destination milestone to connect'); }

    if (act === 'child' || act === 'attach-child') { attachChild(id); return; }
    if (false && act === 'child') {

      const n = b.nodes[id];

      const c = addState(n.x + COL, n.y + 40, { select: false });

      link(id, c);

      // Link the new child milestone forward to downstream target or GOAL to avoid creating a dead-end leaf node

      const parentOuts = Object.values(b.edges).filter((e) => e.from === id && e.to !== c);

      const targetId = parentOuts.length > 0 ? parentOuts[0].to : b.goalId;

      if (targetId && targetId !== c && !Object.values(b.edges).some((e) => e.from === c && e.to === targetId)) {

        link(c, targetId);

      }

    }

    if (act === 'center') canvas.centerOn(id);

    if (act === 'block-impossible' || act === 'block-expensive') {

      const level = act === 'block-impossible' ? 'impossible' : 'expensive';

      b.nodes[id].blocked = { level, reason: String(b.nodes[id].blockReason || '').slice(0, 140), at: now() };

      persist(); refresh();

      toast(level === 'impossible' ? 'Marked out of reach — A* routes around it now' : 'Priced it up: every route through it costs 2.5× more');

    }

    if (act === 'unblock') { delete b.nodes[id].blocked; persist(); refresh(); toast('Route reopened'); }

    if (act === 'ins-guide') {

      sound.play('pop');

      if (window.tour && typeof window.tour.goToStepId === 'function') {

        window.tour.goToStepId('action-checklist');

      } else if (window.tour && typeof window.tour.start === 'function') {

        window.tour.start(true);

      }

    }

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


function attachChild(id, atX, atY) {
  const b = board();
  if (!b || !b.nodes[id]) return null;
  const n = b.nodes[id];
  const COL = 240;
  const x = atX != null ? atX : n.x + COL;
  const y = atY != null ? atY : n.y + 30;
  const c = addState(x, y, { select: true });
  if (c) {
    link(id, c);
    const parentOuts = Object.values(b.edges).filter((e) => e.from === id && e.to !== c);
    const targetId = parentOuts.length > 0 ? parentOuts[0].to : b.goalId;
    if (targetId && targetId !== c && !Object.values(b.edges).some((e) => e.from === c && e.to === targetId)) {
      link(c, targetId);
    }
    persist();
    refresh();
    toast('Attached connected milestone');
  }
  return c;
}

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

  canvas.setLinkMode(null); updateLinkBanner(null);

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

    toast(n.kind === 'goal' ? 'Goal achieved!' : `Done ${n.label}`);

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

    const added = applyDream(b, result, { ...ctx, by }) || { nodes: [], edges: [], updated: false };

    estimateMissingH(b, settings().weights);

    placeNew(b, added.nodes || []);

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

  if (Object.keys(b.edges).length) {

    const ok = await askConfirm({

      title: 'Dream a fresh map?',

      message: 'Existing states are kept; matching ones are merged with the new route.',

      confirmText: 'Dream it',

    });

    if (!ok) return;

  }

  const added = await dream(request('dream'), {}, 'dreaming a map…', b.startId);

  if (added) await afterDream(b);

}



// Lay out a fresh map; if the dreamer left a gap before the goal, let Search fill it.

async function afterDream(b) {

  tidy(b);

  persist();

  refresh();

  canvas.fit();

  const r = astar(b, settings().weights, { frictionFn });

  if (r.found) setTimeout(() => canvas.scan(r.explored), 500);

  else {

    log('map doesn’t reach the goal yet — running Search');

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

  if (!todo.length) { toast('Every step on the path already has a checklist — use Add detail on one to redo it'); return; }

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

    const r = astar(b, w, { frictionFn });

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

    log(`* ${mode === 'bridge' ? 'bridging' : 'expanding'} “${b.nodes[id].label}” (f = ${fmt(r.g.get(id) + h(id))})`);

    const added = await expandNode(id, mode);

    pulseId = null;

    refresh();

    if (!added) break;

  }

  pulseId = null;

  $('#stopBtn').hidden = true;

  const r = astar(b, w, { frictionFn });

  refresh();

  if (r.found) { toast(`Path found: ${r.edges.length} steps, cost ${fmt(r.cost)}`); canvas.fit(); }

  else if (stopRequested) toast('Search stopped');

  else toast('No path yet — run Search again or raise the budget in Settings');

}



// ---------- boards ----------

function updateNewGoalRouteHint() {

  const f = $('#newGoalForm');

  const d = f.elements.detail?.value;

  const hintEl = $('#newGoalRouteHint');

  if (!hintEl) return;

  if (d === 'detailed' || d === 'deep') {

    hintEl.textContent = '★ Detailed mode: explores 4–6 parallel routes from START to GOAL.';

  } else if (f.elements.routes?.value === 'one') {

    hintEl.textContent = 'Single direct path with no alternatives.';

  } else {

    hintEl.textContent = 'Balanced multi-path planning with 3–4 comparison branches.';

  }

}



function openNewGoal() {

  const f = $('#newGoalForm');

  f.reset();

  f.elements.detail.value = settings().detail;

  f.elements.routes.value = settings().routes;

  if (f.elements.detail.value === 'detailed' || f.elements.detail.value === 'deep') {

    f.elements.routes.value = 'many';

  }

  updateNewGoalRouteHint();

  $('#newGoalDlg').returnValue = '';

  $('#newGoalDlg').showModal();

}



$('#newGoalForm')?.addEventListener('change', (e) => {

  const f = $('#newGoalForm');

  if (e.target.name === 'detail') {

    if (e.target.value === 'detailed' || e.target.value === 'deep') {

      f.elements.routes.value = 'many';

    }

  }

  updateNewGoalRouteHint();

});



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

  canvas.setLinkMode(null); updateLinkBanner(null);

  persist({ touch: false });

  refresh();

  canvas.fit(false);

}



// ---------- settings ----------

const getPath = (obj, path) => path.split('.').reduce((o, k) => o?.[k], obj);

const setPath = (obj, path, v) => {
  const ks = path.split('.');
  const last = ks.pop();
  const target = ks.reduce((o, k) => {
    if (!o[k] || typeof o[k] !== 'object') o[k] = {};
    return o[k];
  }, obj);
  target[last] = v;
};

// Synchronize font pills UI
function syncFontPickerUI() {
  const currentVal = getPath(settings(), 'display.font') || 'hand';

  document.querySelectorAll('.font-pill-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.font === currentVal);
  });
}

function openSettings() {

  const f = $('#settingsForm');

  for (const el of f.elements) {

    if (!el.name) continue;

    const v = getPath(settings(), el.name);

    if (el.type === 'radio') el.checked = v === el.value;

    else if (el.type === 'checkbox') el.checked = !!v;

    else el.value = v ?? '';

  }

  const themePick = $('#settingsTheme');

  if (themePick) themePick.value = theme.currentPreset;

  syncFontPickerUI();

  showPane();

  $('#settingsDlg').returnValue = '';

  $('#settingsDlg').showModal();

}



function showPane() {

  const v = $('#settingsForm').elements.dreamer.value;

  for (const p of document.querySelectorAll('.pane')) p.hidden = p.dataset.pane !== v;

}

$('#dreamerSeg').addEventListener('change', showPane);

$('#settingsTheme')?.addEventListener('change', (e) => {
  theme.setPreset(e.target.value);
});

document.querySelectorAll('.font-pill-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    sound.play('click');
    const fVal = btn.dataset.font;
    syncFontPickerUI();
    setPath(settings(), 'display.font', fVal);
    persist({ touch: false });
    applyDisplay();
    refresh();
  });
});

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

// Tapping outside settings dialog closes and saves settings
let settingsMouseDownOutside = false;
const settingsDlg = $('#settingsDlg');
if (settingsDlg) {
  settingsDlg.addEventListener('mousedown', (e) => {
    const rect = settingsDlg.getBoundingClientRect();
    settingsMouseDownOutside = (
      e.clientX < rect.left || e.clientX > rect.right ||
      e.clientY < rect.top || e.clientY > rect.bottom
    );
  });

  settingsDlg.addEventListener('touchstart', (e) => {
    if (!e.touches || !e.touches[0]) return;
    const t = e.touches[0];
    const rect = settingsDlg.getBoundingClientRect();
    settingsMouseDownOutside = (
      t.clientX < rect.left || t.clientX > rect.right ||
      t.clientY < rect.top || t.clientY > rect.bottom
    );
  }, { passive: true });

  const closeAndSaveSettings = () => {
    if (settingsDlg.open) {
      sound.play('click');
      settingsDlg.returnValue = 'ok';
      settingsDlg.close('ok');
    }
  };

  settingsDlg.addEventListener('click', (e) => {
    const rect = settingsDlg.getBoundingClientRect();
    const isOutside = (
      e.clientX < rect.left || e.clientX > rect.right ||
      e.clientY < rect.top || e.clientY > rect.bottom
    );
    if (isOutside && settingsMouseDownOutside) {
      closeAndSaveSettings();
    }
    settingsMouseDownOutside = false;
  });

  settingsDlg.addEventListener('touchend', (e) => {
    if (e.changedTouches && e.changedTouches[0] && settingsMouseDownOutside) {
      const t = e.changedTouches[0];
      const rect = settingsDlg.getBoundingClientRect();
      const isOutside = (
        t.clientX < rect.left || t.clientX > rect.right ||
        t.clientY < rect.top || t.clientY > rect.bottom
      );
      if (isOutside) {
        closeAndSaveSettings();
      }
    }
    settingsMouseDownOutside = false;
  });
}



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

    else if (!quiet) toast('Synced');

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



$('#boardDetail').addEventListener('change', (e) => {

  const b = board();

  b.detail = e.target.value;

  if (e.target.value === 'detailed' || e.target.value === 'deep') {

    b.routes = 'many';

    $('#boardRoutes').value = 'many';

    toast('Detailed mode: exploring 4–6 alternative paths to the goal');

  }

  persist();

  refresh({ inspector: false });

});

$('#boardRoutes').addEventListener('change', (e) => { board().routes = e.target.value; persist(); });

$('#ctx').addEventListener('input', (e) => {

  const k = e.target.dataset.b;

  if (k && board()) { board()[k] = e.target.value; persist(); }

});



$('#deleteBoardBtn').addEventListener('click', async () => {

  const b = board();

  if (!b) return;

  const ok = await askConfirm({

    title: 'Delete this goal?',

    message: `“${b.nodes[b.goalId].label}” and its map will be removed. This cannot be undone unless it is in a sync or export.`,

    confirmText: 'Delete goal',

    danger: true,

  });

  if (!ok) return;

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

  if (e.target.closest?.('input, textarea, select, dialog')) return;

  const b = board();

  if (e.key === 'Escape') { canvas.setLinkMode(null); updateLinkBanner(null); select(null); }

  if ((e.key === 'Delete' || e.key === 'Backspace') && sel && b) {

    if (sel.type === 'node' && deleteNode(b, sel.id)) { sel = null; persist(); refresh(); }

    else if (sel.type === 'edge') { delete b.edges[sel.id]; sel = null; persist(); refresh(); }

  }

  if (e.key === 'f') canvas.fit();

  if (e.key === '+' || e.key === '=') canvas.zoomBy(1.25);

  if (e.key === '-') canvas.zoomBy(0.8);

});



window.addEventListener('resize', () => board() && canvas.drawMinimapSoon());

window.canvas = canvas;

window.centerNode = (id, anim) => canvas.centerOn(id, anim);

window.centerEdge = (id, anim) => canvas.centerOnEdge(id, anim);

window.selectNode = (id) => select({ type: 'node', id });

window.selectFirstStateNode = () => {

  const b = board();

  if (!b) return null;

  const stateNode = Object.values(b.nodes).find(n => n.kind === 'state') || Object.values(b.nodes)[0];

  if (stateNode) {

    select({ type: 'node', id: stateNode.id });

    return stateNode.id;

  }

  return null;

};

window.clearSelect = () => select(null);



function stopTourBounce() {

  try {

    localStorage.setItem('goalstar_tour_clicked', 'true');
    localStorage.setItem('goalstar_guide_clicked', 'true');

  } catch (e) {}

  document.querySelectorAll('.tour-bounce-btn').forEach(btn => btn.classList.remove('tour-bounce-btn'));

}

window.stopTourBounce = stopTourBounce;

if (localStorage.getItem('goalstar_tour_clicked') === 'true' || localStorage.getItem('goalstar_guide_clicked') === 'true' || localStorage.getItem('goalstar_walkthrough_completed') === 'true') {

  stopTourBounce();

}





// ---------- Walrus Memory & Tatum Sui Wiring ----------

async function updateWalrusTelemetry() {

  const [stats, memories] = await Promise.all([

    walrusMemory.checkStatus(),

    walrusMemory.recall(),

  ]);

  const countBadge = $('#walrusCountBadge');

  if (countBadge) {

    countBadge.textContent = stats.enabled

      ? `Mainnet · ${memories.length} memories`

      : `Local pending · ${memories.length}`;

  }



  const insight = watchdog.generateLastTuesdayInsight();

  const textEl = $('#tuesdayText');

  const ruleEl = $('#tuesdayRule');

  if (textEl && ruleEl) {

    const short = insight.text.length > 150 ? insight.text.slice(0, 149) + '…' : insight.text;

    textEl.textContent = insight.hasInsight ? `Remembered: ${short}` : short;

    ruleEl.textContent = insight.ruleApplied;

  }



  // Say plainly what memory is doing right now, in the panel and the banner.

  const recallLine = $('#walrusRecallLine');

  if (recallLine) {

    const newest = String(memories[0]?.text || '').trim();

    const preview = newest.length > 120 ? newest.slice(0, 119) + '…' : newest;

    recallLine.innerHTML = memories.length

      ? `<b>Remembered ${memories.length} memor${memories.length === 1 ? 'y' : 'ies'}.</b> Newest: “${esc(preview)}”. Matching steps cost more on the route.`

      : 'No memories yet. Log your progress or blockers so GoalStar learns where you usually stall.';

  }



  const banner = $('#lastTuesdayBanner');

  if (banner) {

    if (memories.length && insight.hasInsight) {

      banner.hidden = false;

      banner.classList.remove('memory-pulse');

      void banner.offsetWidth;

      banner.classList.add('memory-pulse');

      if (!window.__walrusAnnounced) {

        window.__walrusAnnounced = true;

        toast(`Walrus recalled ${memories.length} memories — matching steps cost more`);

      }

    } else {

      banner.hidden = true; // Never show fake or simulated placeholder memory!

    }

  }



  refresh({ inspector: false });

}



async function updateTatumTelemetry() {

  const sui = await tatumSui.checkStatus();

  const badge = $('#tatumRpcBadge');

  if (badge) {

    if (sui && sui.checkpoint && typeof sui.checkpoint === 'string' && !sui.checkpoint.includes('Not Found')) {

      badge.textContent = `Sui #${sui.checkpoint}`;

    } else {

      badge.textContent = 'Mainnet Active (Tatum)';

    }

  }

}



// Modal & button wiring

$('#addMemoryBtn')?.addEventListener('click', () => {

  const modal = $('#memoryModal');

  if (modal) modal.hidden = false;

});



$('#shareBoardBtn')?.addEventListener('click', shareBoard);

$('#templatesBtn')?.addEventListener('click', () => loadTemplates(true));

$('#seedMemoryBtn')?.addEventListener('click', async () => {

  const btn = $('#seedMemoryBtn');

  if (btn) {

    btn.disabled = true;

    btn.textContent = 'Seeding...';

  }

  toast('Writing 10 habit & friction memories to Walrus Mainnet...');

  const res = await walrusMemory.seedTenMemories();

  if (btn) {

    btn.disabled = false;

    btn.textContent = '10 Seeded';

  }

  await updateWalrusTelemetry();

  toast(res ? 'Successfully stored 10 memories on Walrus Mainnet!' : 'Seed queued locally', res ? 'ok' : 'info');

});

$('#closeTemplatesBtn')?.addEventListener('click', () => { const box = $('#templatesBox'); if (box) box.hidden = true; });

$('#publishTemplateBtn')?.addEventListener('click', publishTemplate);

$('#templateList')?.addEventListener('click', (e) => {

  const li = e.target.closest('[data-template]');

  if (li) importTemplate(li.dataset.template);

});



$('#cancelMemoryBtn')?.addEventListener('click', () => {

  const modal = $('#memoryModal');

  if (modal) modal.hidden = true;

});



$('#saveMemoryBtn')?.addEventListener('click', async () => {

  const input = $('#memoryInput');

  const text = (input?.value || '').trim();

  if (!text) return;



  const btn = $('#saveMemoryBtn');

  btn.textContent = 'Writing to Mainnet...';

  btn.disabled = true;



  const saved = await walrusMemory.remember(text, 'user_update');

  input.value = '';

  $('#memoryModal').hidden = true;

  btn.textContent = 'Save to Walrus Mainnet';

  btn.disabled = false;



  await updateWalrusTelemetry();

  toast(saved ? 'Memory saved to Walrus — future routes will re-price around it' : 'Saved locally — it will sync when Walrus is reachable');

});



// Certificate: Walrus blob (the deliverable) + Sui stamp (the proof of it).

document.addEventListener('click', async (e) => {

  const suiBtn = e.target.closest('[data-act="sui-stamp"]');

  if (suiBtn) {

    const nodeId = suiBtn.dataset.nodeid;

    const b = board();

    const node = b?.nodes[nodeId];

    if (!node) return;



    const checklist = Object.values(b.edges).filter((x) => x.to === nodeId).flatMap((x) => (x.steps || []).map((s) => s.text));

    suiBtn.textContent = 'Sealing Walrus + Sui certificate…';

    suiBtn.disabled = true;



    const res = await tatumSui.stampMilestone(node.id, node.label, { checklist, goal: b.nodes[b.goalId]?.label });

    if (res && res.onchainProof) {

      node.proof = res.onchainProof;

      persist();

      suiBtn.replaceWith(certificateCard(node, b, res.onchainProof));

      toast('Certificate sealed: deliverable on Walrus, stamp on Sui');

    } else {

      suiBtn.textContent = 'Stamp failed — try again';

      suiBtn.disabled = false;

    }

  }



  const decomposeBtn = e.target.closest('[data-act="auto-decompose"]');

  if (decomposeBtn) {

    const nodeId = decomposeBtn.dataset.nodeid;

    if (!board()?.nodes[nodeId] || busy) return;

    decomposeBtn.textContent = 'Decomposing…';

    decomposeBtn.disabled = true;

    select({ type: 'node', id: nodeId });

    await expandNode(nodeId);

    refresh();

  }

});





// ---------- Walrus: sharing, shared knowledge, certificates, notes ----------

let noteMemoryTimer = null;

function rememberNote(obj, text) {

  const value = String(text || '').trim();

  if (value.length < 3) return;

  clearTimeout(noteMemoryTimer);

  noteMemoryTimer = setTimeout(() => {

    const where = obj.label || 'an action';

    walrusMemory.remember(`NOTE on "${where}": ${value}`.slice(0, 900), 'note').catch(() => {});

  }, 1500);

}



function certificateCard(node, b, proof) {

  const el = document.createElement('div');

  el.className = 'cert-card';

  const steps = Object.values(b.edges).filter((x) => x.to === node.id)

    .flatMap((x) => (x.steps || []).filter((s) => s.done).map((s) => s.text));

  el.innerHTML = `

    <div class="cert-kicker">Certificate · Walrus + Sui</div>

    <h4>${esc(node.label)}</h4>

    <div class="cert-sub">${esc(b.nodes[b.goalId]?.label || '')} · ${new Date(proof.timestamp || Date.now()).toLocaleDateString()}</div>

    ${steps.length ? `<ul class="cert-steps">${steps.slice(0, 6).map((s) => `<li>${esc(s)}</li>`).join('')}</ul>` : ''}

    <div class="cert-meta">

      <div><span>Walrus blob</span><code>${esc(proof.walrusBlobId || '—')}</code></div>

      <div><span>Sui checkpoint</span><code>#${esc(proof.checkpoint || '—')}</code></div>

      <div><span>Proof digest</span><code>${esc(proof.proofDigest || '—')}</code></div>

    </div>

    <div class="cert-links">

      ${proof.certificateUrl ? `<a href="${esc(proof.certificateUrl)}" target="_blank" rel="noopener">Open the immutable record</a>` : ''}

      ${proof.shareLink ? `<a href="${esc(proof.shareLink)}" target="_blank" rel="noopener">Share this certificate</a>` : ''}

    </div>`;

  return el;

}



function addSharedBoard(source) {

  const copy = JSON.parse(JSON.stringify(source));

  copy.id = uid('b');

  copy.title = `${copy.title || 'Shared goal'} (shared)`;

  copy.updated = now();

  data.boards[copy.id] = copy;

  data.currentId = copy.id;

  sel = null;

  persist();

  refresh();

  canvas.fit(false);

}



async function shareBoard() {

  const b = board();

  if (!b) return toast('Open a goal first');

  const btn = $('#shareBoardBtn');

  btn.disabled = true;

  btn.textContent = 'Publishing…';

  try {

    const res = await fetch('/api/walrus/snapshot', {

      method: 'POST', headers: { 'Content-Type': 'application/json' },

      body: JSON.stringify({ board: b, label: b.nodes[b.goalId]?.label || b.title }),

    });

    const data = await res.json();

    if (!data.success) throw new Error(data.error || 'Walrus refused the snapshot');

    const link = `${location.origin}/index.html?board=walrus://${data.id}`;

    try { await navigator.clipboard.writeText(link); } catch { /* clipboard blocked */ }

    toast(`Saved on Walrus (${data.storage}) · copied · walrus://${data.id}`, 'ok');

    log(`shared board → walrus://${data.id}`);

  } catch (err) {

    toast(`Share failed: ${err.message}`, 'err');

  } finally {

    btn.disabled = false;

    btn.textContent = 'Share board';

  }

}



async function loadTemplates(show = true) {

  const box = $('#templatesBox');

  const list = $('#templateList');

  if (!box || !list) return;

  if (show) box.hidden = false;

  list.innerHTML = '<li class="muted small">Reading the public Walrus namespace…</li>';

  try {

    const res = await fetch('/api/walrus/templates');

    const data = await res.json();

    list.innerHTML = (data.templates || []).length

      ? data.templates.map((t) => `<li data-template="${esc(t.id)}">

          <b>${esc(t.title)}</b>

          <span class="muted small">${esc(t.start || '')} → ${esc(t.goal || '')}${t.author ? ` · ${esc(t.author)}` : ''}</span>

        </li>`).join('')

      : '<li class="muted small">Nothing published yet. Publish a goal so other people — and their agents — can start from your map.</li>';

  } catch (err) {

    list.innerHTML = `<li class="muted small">Could not read templates: ${esc(err.message)}</li>`;

  }

}



async function publishTemplate() {

  const b = board();

  if (!b) return toast('Open a goal first');

  const btn = $('#publishTemplateBtn');

  btn.disabled = true;

  btn.textContent = 'Publishing…';

  try {

    const res = await fetch('/api/walrus/templates', {

      method: 'POST', headers: { 'Content-Type': 'application/json' },

      body: JSON.stringify({ board: b, author: localStorage.getItem('goalstar_user') || 'anonymous', tags: b.constraints || '' }),

    });

    const data = await res.json();

    if (!data.success) throw new Error(data.error || 'Publish failed');

    toast('Published to the shared Walrus knowledge base');

    await loadTemplates(false);

  } catch (err) {

    toast(`Publish failed: ${err.message}`, 'err');

  } finally {

    btn.disabled = false;

    btn.textContent = 'Publish this goal';

  }

}



async function importTemplate(id) {

  try {

    const res = await fetch(`/api/walrus/blob/${id}`);

    const data = await res.json();

    const source = data.board || data.template?.board;

    if (!source?.nodes) throw new Error('That blob is not a goal map');

    addSharedBoard(source);

    toast(`Imported “${data.template || data.label || 'shared goal'}”`);

  } catch (err) {

    toast(`Import failed: ${err.message}`, 'err');

  }

}



function showCertificateBanner(cert, id) {

  document.getElementById('certFloat')?.remove();

  const wrap = document.createElement('div');

  wrap.id = 'certFloat';

  wrap.className = 'cert-float';

  const steps = (cert.checklist || []).filter(Boolean);

  wrap.innerHTML = `

    <button class="cert-close" aria-label="Close">&times;</button>

    <div class="cert-kicker">Verified on Walrus + Sui</div>

    <h4>${esc(cert.milestoneLabel || 'Milestone')}</h4>

    <div class="cert-sub">${esc(cert.goal || '')} · ${new Date(cert.completedAt || Date.now()).toLocaleDateString()}</div>

    ${steps.length ? `<ul class="cert-steps">${steps.slice(0, 6).map((s) => `<li>${esc(typeof s === 'string' ? s : s.text)}</li>`).join('')}</ul>` : ''}

    <div class="cert-meta">

      <div><span>Walrus blob</span><code>${esc(id)}</code></div>

      <div><span>Sui checkpoint</span><code>#${esc(cert.checkpoint || '—')}</code></div>

    </div>

    <a class="cert-link" href="/api/walrus/blob/${esc(id)}" target="_blank" rel="noopener">Open the immutable record</a>`;

  document.body.appendChild(wrap);

  wrap.querySelector('.cert-close').addEventListener('click', () => wrap.remove());

}



async function loadSharedLink() {

  const params = new URLSearchParams(location.search);

  const blobId = (v) => (v && v.startsWith('walrus://') ? v.slice(9) : null);

  const bId = blobId(params.get('board'));

  const cId = blobId(params.get('cert'));

  try {

    if (bId) {

      const data = await (await fetch(`/api/walrus/blob/${bId}`)).json();

      if (data.board?.nodes) { addSharedBoard(data.board); toast('Opened a board shared from Walrus'); }

      else toast('That share link held no board', 'err');

    }

    if (cId) {

      const data = await (await fetch(`/api/walrus/blob/${cId}`)).json();

      if (data.kind === 'certificate') showCertificateBanner(data, cId);

      else toast('That certificate link is empty', 'err');

    }

    const goalParam = params.get('goal');
    if (goalParam && !bId && !cId) {
      const b = createBoard({
        goal: goalParam,
        context: params.get('context') || 'Starting from where I am right now',
        constraints: params.get('constraints') || '',
        timeframe: params.get('timeframe') || '',
        budget: params.get('budget') || '',
        detail: settings().detail || 'normal',
        routes: settings().routes || 'some',
      });
      data.boards[b.id] = b;
      data.currentId = b.id;
      sel = null;
      persist();
      refresh();
      canvas.fit(false);
      toast(`Created plan for: "${goalParam}"`);
      setTimeout(async () => {
        try {
          const added = await dream(request('dream'), {}, 'Dreaming realistic milestones...', b.startId);
          if (added) await afterDream(b);
        } catch (err) {
          console.warn('Auto-dream failed:', err);
        }
      }, 350);
    }

  } catch (err) {

    toast(`Could not open the Walrus link: ${err.message}`, 'err');

  }

}



function updateLinkBanner(fromId) {

  let bEl = document.getElementById('linkBanner');

  if (!fromId) {

    if (bEl) bEl.hidden = true;

    return;

  }

  if (!bEl) {

    bEl = document.createElement('div');

    bEl.id = 'linkBanner';

    bEl.className = 'link-banner';

    bEl.innerHTML = `<span id="linkBannerText"></span><button id="cancelLinkBtn">Cancel</button>`;

    document.body.appendChild(bEl);

    bEl.querySelector('#cancelLinkBtn').addEventListener('click', () => {

      canvas.setLinkMode(null); updateLinkBanner(null);

      updateLinkBanner(null);

      toast('Connect cancelled');

    });

  }

  const b = board();

  const name = b?.nodes[fromId]?.label || 'Milestone';

  bEl.querySelector('#linkBannerText').textContent = `Connecting from "${name}": Click any destination milestone card (or Esc)`;

  bEl.hidden = false;

}



window.selectFirstEdge = () => {

  const b = board();

  if (!b) return;

  const firstEid = (lastPath?.edges && lastPath.edges[0]) || Object.keys(b.edges)[0];

  if (firstEid) {

    select({ type: 'edge', id: firstEid });

    if (window.canvas) window.canvas.centerOnEdge(firstEid, false);

  }

};



// ---------- planning agent chat (plain-English edits) ----------

function agentBoardContext() {

  const b = board();

  if (!b) return null;

  const targetId = (sel && sel.type === 'node') ? sel.id : (lastClickedNodeId && b.nodes[lastClickedNodeId]) ? lastClickedNodeId : null;

  const targetNode = targetId ? b.nodes[targetId] : null;

  return {

    goal: { id: b.goalId, label: b.nodes[b.goalId]?.label || b.title },

    start: { id: b.startId, label: b.nodes[b.startId]?.label || '' },

    constraints: b.constraints || '',

    timeframe: b.timeframe || '',

    budget: b.budget || '',

    targetNodeId: targetId,

    targetNodeLabel: targetNode?.label || null,

    nodes: Object.values(b.nodes).map((n) => ({ id: n.id, label: n.label, kind: n.kind, done: !!n.done })),

    edges: Object.values(b.edges).map((e) => ({

      id: e.id, label: e.label, from: e.from, to: e.to,

      fromLabel: b.nodes[e.from]?.label || '', toLabel: b.nodes[e.to]?.label || '',

      steps: (e.steps || []).map((s) => s.text),

    })),

    bestPath: lastPath?.found ? lastPath.edges : [],

  };

}



const clipText = (v, n) => String(v ?? '').trim().slice(0, n);



// Apply the agent's structured edits to the open goal. Every op is validated

// against the real map, so an unknown id is reported instead of applied.

async function applyAgentOps(ops = []) {

  const b = board();

  if (!b) return { ok: [], fail: ['No goal is open'] };

  const ok = [], fail = [], replan = [];

  let touched = null;



  for (const op of ops.slice(0, 25)) {

    const type = op?.type;

    const node = op?.id ? b.nodes[op.id] : null;

    const edge = op?.id ? b.edges[op.id] : null;



    if (type === 'rename_state') {

      const label = clipText(op.label, 140);

      if (!node) fail.push(`No milestone with id ${op.id}`);

      else if (!label) fail.push('That rename was empty');

      else {

        node.label = label;

        if (node.kind === 'goal') b.title = label;

        touched = node.id;

        ok.push(`Renamed milestone to “${label}”`);

      }

    } else if (type === 'rename_action') {

      const label = clipText(op.label, 160);

      if (!edge) fail.push(`No action with id ${op.id}`);

      else if (!label) fail.push('That rename was empty');

      else {

        edge.label = label;

        touched = edge.to;

        ok.push(`Renamed action to “${label}”`);

      }

    } else if (type === 'set_done') {

      if (!node || node.kind === 'start') fail.push('That milestone cannot be completed');

      else {

        node.done = op.done !== false;

        touched = node.id;

        ok.push(`${node.done ? 'Marked complete' : 'Reopened'} “${node.label}”`);

      }

    } else if (type === 'remove_state') {

      if (!node) fail.push(`No milestone with id ${op.id}`);

      else if (node.kind !== 'state') fail.push('The start and the goal cannot be invalidated');

      else {

        const label = node.label;

        deleteNode(b, node.id);

        ok.push(`Invalidated “${label}” and its actions`);

      }

    } else if (type === 'remove_action') {

      if (!edge) fail.push(`No action with id ${op.id}`);

      else {

        const label = edge.label;

        delete b.edges[edge.id];

        ok.push(`Removed the action “${label}”`);

      }

    } else if (type === 'relink_action') {

      const to = b.nodes[op.to];

      if (!edge) fail.push(`No action with id ${op.id}`);

      else if (!to) fail.push(`No milestone with id ${op.to}`);

      else if (to.id === edge.from) fail.push('An action cannot point back at its own state');

      else if (Object.values(b.edges).some((x) => x.id !== edge.id && x.from === edge.from && x.to === to.id)) {

        fail.push(`“${b.nodes[edge.from]?.label}” already has an action to “${to.label}”`);

      } else {

        edge.to = to.id;

        touched = to.id;

        ok.push(`Re-routed “${edge.label}” to “${to.label}”`);

      }

    } else if (type === 'block_state') {

      if (!node || node.kind !== 'state') fail.push('Only a milestone between start and goal can be blocked');

      else {

        const level = op.level === 'expensive' ? 'expensive' : 'impossible';

        node.blocked = { level, reason: clipText(op.reason, 140), at: now() };

        touched = node.id;

        ok.push(`Marked “${node.label}” ${level === 'impossible' ? 'out of reach' : 'very expensive'}`);

      }

    } else if (type === 'replan') {

      if (!node || node.kind === 'goal') fail.push('Pick a non-goal milestone to re-plan from');

      else replan.push(node.id);

    } else if (type === 'add_branch') {

      const fromNode = b.nodes[op.fromId || op.id];

      let toNode = op.toId ? b.nodes[op.toId] : null;

      if (!toNode) toNode = b.nodes[b.goalId]; // always connect back to downstream or GOAL!

      

      if (!fromNode) {

        fail.push(`Cannot branch from unknown milestone "${op.fromId || op.id}"`);

      } else if (!toNode) {

        fail.push(`Cannot connect branches to unknown milestone "${op.toId}"`);

      } else {

        const branches = Array.isArray(op.branches) ? op.branches : [];

        if (!branches.length) {

          fail.push('No branch definitions provided');

        } else {

          const fromX = fromNode.x || 200;

          const fromY = fromNode.y || 200;

          const toX = toNode.x || (fromX + 420);

          const midX = Math.round((fromX + toX) / 2);

          const spreadY = 130;

          const startY = fromY - Math.round(((branches.length - 1) * spreadY) / 2);



          branches.forEach((br, idx) => {

            const mLabel = clipText(br.milestone || br.label || `Alternative Path ${idx + 1}`, 140);

            const mNote = clipText(br.note || '', 400);

            const inLabel = clipText(br.actionIn || `Approach via ${mLabel}`, 140);

            const outLabel = clipText(br.actionOut || `Advance to ${toNode.label}`, 140);

            const branchY = startY + idx * spreadY;



            const newNodeId = uid('n');

            b.nodes[newNodeId] = {

              id: newNodeId,

              kind: 'state',

              label: mLabel,

              note: mNote,

              x: midX,

              y: branchY,

              h: Math.max(1, (fromNode.h || 5) - 2),

              done: false,

            };



            const inEdgeId = uid('e');

            b.edges[inEdgeId] = {

              id: inEdgeId,

              from: fromNode.id,

              to: newNodeId,

              label: inLabel,

              note: '',

              cost: {

                time: br.time ?? 2,

                money: br.money ?? 1,

                effort: br.effort ?? 2,

                risk: br.risk ?? 1,

              },

              duration: br.duration || '1 week',

              steps: (br.steps || []).map(s => ({ text: String(s), done: false })),

            };



            const outEdgeId = uid('e');

            b.edges[outEdgeId] = {

              id: outEdgeId,

              from: newNodeId,

              to: toNode.id,

              label: outLabel,

              note: '',

              cost: {

                time: br.timeOut ?? 2,

                money: br.moneyOut ?? 1,

                effort: br.effortOut ?? 2,

                risk: br.riskOut ?? 1,

              },

              duration: br.durationOut || '1 week',

              steps: [],

            };



            ok.push(`Added branch "${mLabel}" connecting "${fromNode.label}" → "${toNode.label}"`);

            touched = newNodeId;

          });

        }

      }

    } else {

      fail.push(`Unsupported edit: ${type || 'unknown'}`);

    }

  }



  if (ok.length) {

    estimateMissingH(b, settings().weights);

    persist();

    refresh();

    if (touched && ok.length === 1) canvas.centerOn(touched);

  }



  for (const id of replan) if (b.nodes[id]) await expandNode(id);

  if (replan.length) refresh();



  return { ok, fail };

}



// ---------- boot ----------

window.toast = toast;

window.auth = auth;

theme.init();

initTooltips();

window.agentChat = initAgentChat({ getContext: agentBoardContext, applyOps: applyAgentOps });

sound.attachListeners();

auth.init();

if (!data.boards[data.currentId]) data.currentId = Object.keys(data.boards)[0] || null;

applyDisplay();

renderWeights();

refresh();

canvas.fit(false);

if (settings().gist.auto && settings().gist.token && settings().gist.id) syncNow(true);



updateWalrusTelemetry();

updateTatumTelemetry();

loadSharedLink();



  // UI Explainer Guide Modal handlers

  const guideDlg = document.getElementById('uiGuideDlg');

  document.getElementById('uiGuideBtn')?.addEventListener('click', () => {

    stopTourBounce();

    sound.play('pop');

    if (!sel) {

      window.selectFirstStateNode?.();

    }

    if (window.tour && typeof window.tour.start === 'function') {

      if (sel && sel.type === 'node') {

        window.tour.goToStepId?.('node-card');

      } else {

        window.tour.start(true);

      }

    } else if (guideDlg && typeof guideDlg.showModal === 'function') {

      guideDlg.showModal();

    }

  });

  document.querySelectorAll('#closeUiGuideBtn, #closeGuideDlgBtn').forEach(b => {

    b.addEventListener('click', () => {

      sound.play('click');

      if (guideDlg && typeof guideDlg.close === 'function') guideDlg.close();

      else if (guideDlg) guideDlg.removeAttribute('open');

    });

  });

  document.getElementById('launchTourFromGuideBtn')?.addEventListener('click', () => {

    stopTourBounce();

    if (guideDlg && typeof guideDlg.close === 'function') guideDlg.close();

    else if (guideDlg) guideDlg.removeAttribute('open');

    sound.play('click');

    if (window.tour && typeof window.tour.start === 'function') window.tour.start(true);

  });

  document.getElementById('tourBtn')?.addEventListener('click', () => {

    stopTourBounce();

  });

  document.getElementById('sideTourBtn')?.addEventListener('click', () => {

    stopTourBounce();

  });

