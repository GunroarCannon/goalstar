// The paper canvas: HTML index cards for states, SVG ink for actions.
// Elements are keyed by id and positions are tweened, so new states fly out of
// their parent, Tidy glides, new actions draw themselves in, and the camera eases.
import { edgeCost, timeToDays, fmtDays } from './astar.js';
import { CARD_W } from './layout.js';

export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const tilt = (id) => {
  let h = 0;
  for (const c of id) h = (h * 31 + c.charCodeAt(0)) | 0;
  return ((h % 100) / 100) * 1.4;
};
const fmt = (v) => (v == null || !Number.isFinite(v) ? '?' : Math.round(v * 10) / 10);
const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);
const NS = 'http://www.w3.org/2000/svg';
const LABEL_W = 170;

// 0 (cheap) → green, 5 → amber, 10 (expensive) → red.
export const costColor = (c) => `hsl(${Math.round(150 - clamp(c, 0, 10) * 14)} 60% 36%)`;
export const durationText = (e) => e.duration || `≈ ${fmtDays(timeToDays(e.cost?.time))}`;
export const stepsDone = (e) => (e.steps?.length ? `${e.steps.filter((s) => s.done).length}/${e.steps.length}` : '');

export class Canvas {
  constructor(root, handlers) {
    this.root = root;
    this.h = handlers;
    this.view = { x: 40, y: 40, k: 1 };
    this.disp = new Map();      // id → displayed {x, y} (tweens toward the node's real x, y)
    this.nodeEls = new Map();
    this.edgeEls = new Map();
    this.entering = new Set();  // node ids still popping in
    this.drawing = new Set();   // edge ids still drawing in
    this.sizes = {};
    this.lsizes = {};
    this.linkFrom = null;
    this.board = null;
    this.o = {};
    this.motion = !matchMedia('(prefers-reduced-motion: reduce)').matches;
    root.innerHTML = `
      <div class="world">
        <svg class="edges" aria-hidden="true">
          <defs>
            <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 L2.5,5 z" class="m-ink"/></marker>
            <marker id="arrHot" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 L2.5,5 z" class="m-hot"/></marker>
            <marker id="arrSel" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 L2.5,5 z" class="m-sel"/></marker>
          </defs>
          <g class="hl-g"></g><g class="edge-g"></g><g class="flow-g"></g>
        </svg>
        <div class="labels"></div>
        <div class="nodes"></div>
        <div class="fx"></div>
      </div>
      <canvas class="minimap" title="Map overview — click or drag to move"></canvas>
      <div class="zoombar" role="toolbar" aria-label="View">
        <button data-z="out" title="Zoom out (−)">−</button>
        <button data-z="reset" class="pct" title="Reset to 100%">100%</button>
        <button data-z="in" title="Zoom in (+)">+</button>
        <span class="zsep"></span>
        <button data-z="fit" title="Fit map to screen (F)">Fit</button>
        <button data-z="tidy" title="Auto-arrange the map">Tidy</button>
      </div>
      <div class="hint">double-click paper: new state · drag: pan · scroll / pinch: zoom</div>`;
    this.world = root.querySelector('.world');
    this.hlG = root.querySelector('.hl-g');
    this.edgeG = root.querySelector('.edge-g');
    this.flowG = root.querySelector('.flow-g');
    this.labelsEl = root.querySelector('.labels');
    this.nodesEl = root.querySelector('.nodes');
    this.fxEl = root.querySelector('.fx');
    this.mini = root.querySelector('.minimap');
    this.pctEl = root.querySelector('.pct');
    this.tick = this.tick.bind(this);
    this.bind();
    this.applyView();
  }

  // ---------- camera ----------
  applyView() {
    const { x, y, k } = this.view;
    this.world.style.transform = `translate(${x}px, ${y}px) scale(${k})`;
    this.root.style.setProperty('--gap', `${28 * k}px`);
    this.root.style.setProperty('--ox', `${x}px`);
    this.root.style.setProperty('--oy', `${y}px`);
    this.pctEl.textContent = `${Math.round(k * 100)}%`;
    this.drawMinimapSoon();
  }

  setView(target, animate = true) {
    cancelAnimationFrame(this.viewRaf);
    if (!animate || !this.motion) { this.view = target; this.applyView(); return; }
    const from = { ...this.view }, t0 = performance.now(), ms = 480;
    const step = (t) => {
      const p = ease(Math.min(1, (t - t0) / ms));
      this.view = { x: from.x + (target.x - from.x) * p, y: from.y + (target.y - from.y) * p, k: from.k + (target.k - from.k) * p };
      this.applyView();
      if (p < 1) this.viewRaf = requestAnimationFrame(step);
    };
    this.viewRaf = requestAnimationFrame(step);
  }

  zoomAt(k, mx, my, animate = false) {
    k = clamp(k, 0.2, 2.5);
    const k0 = this.view.k;
    this.setView({ k, x: mx - ((mx - this.view.x) * k) / k0, y: my - ((my - this.view.y) * k) / k0 }, animate);
  }

  zoomBy(f) {
    this.zoomAt(this.view.k * f, this.root.clientWidth / 2, this.root.clientHeight / 2, true);
  }

  toWorld(cx, cy) {
    const r = this.root.getBoundingClientRect();
    return { x: (cx - r.left - this.view.x) / this.view.k, y: (cy - r.top - this.view.y) / this.view.k };
  }

  // ---------- input ----------
  bind() {
    const root = this.root;
    const pts = new Map(); // active pointers on the paper, for pan + pinch
    let pan = null, pinch = null;

    root.addEventListener('pointerdown', (e) => {
      if (e.target.closest('.node, .elabel, .zoombar, .minimap') || (e.pointerType === 'mouse' && e.button !== 0)) return;
      cancelAnimationFrame(this.viewRaf);
      root.setPointerCapture(e.pointerId);
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pts.size === 1) {
        pan = { sx: e.clientX, sy: e.clientY, ox: this.view.x, oy: this.view.y, moved: false };
        root.classList.add('panning');
      } else if (pts.size === 2) {
        const [a, b] = [...pts.values()];
        pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), k: this.view.k };
        pan = null;
      }
    });
    root.addEventListener('pointermove', (e) => {
      if (!pts.has(e.pointerId)) return;
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pinch && pts.size === 2) {
        const [a, b] = [...pts.values()];
        const r = root.getBoundingClientRect();
        this.zoomAt(pinch.k * (Math.hypot(a.x - b.x, a.y - b.y) / pinch.d), (a.x + b.x) / 2 - r.left, (a.y + b.y) / 2 - r.top);
      } else if (pan) {
        const dx = e.clientX - pan.sx, dy = e.clientY - pan.sy;
        if (Math.abs(dx) + Math.abs(dy) > 3) pan.moved = true;
        this.view.x = pan.ox + dx;
        this.view.y = pan.oy + dy;
        this.applyView();
      }
    });
    const up = (e) => {
      if (!pts.has(e.pointerId)) return;
      pts.delete(e.pointerId);
      if (pts.size < 2) pinch = null;
      if (!pts.size) {
        root.classList.remove('panning');
        if (pan && !pan.moved && e.type === 'pointerup') this.h.onBackgroundClick();
        pan = null;
      }
    };
    root.addEventListener('pointerup', up);
    root.addEventListener('pointercancel', up);

    root.addEventListener('wheel', (e) => {
      if (e.target.closest('.minimap')) return;
      e.preventDefault();
      cancelAnimationFrame(this.viewRaf);
      const r = root.getBoundingClientRect();
      this.zoomAt(this.view.k * Math.exp(-e.deltaY * 0.0015), e.clientX - r.left, e.clientY - r.top);
    }, { passive: false });

    root.addEventListener('dblclick', (e) => {
      if (e.target.closest('.node, .elabel, .zoombar, .minimap')) return;
      const p = this.toWorld(e.clientX, e.clientY);
      this.h.onBackgroundDblClick(p.x - CARD_W / 2, p.y - 30);
    });

    root.querySelector('.zoombar').addEventListener('click', (e) => {
      const z = e.target.closest('[data-z]')?.dataset.z;
      if (z === 'in') this.zoomBy(1.25);
      if (z === 'out') this.zoomBy(0.8);
      if (z === 'reset') this.zoomAt(1, root.clientWidth / 2, root.clientHeight / 2, true);
      if (z === 'fit') this.fit();
      if (z === 'tidy') this.h.onTidy();
    });

    this.nodesEl.addEventListener('pointerdown', (e) => {
      const el = e.target.closest('.node');
      if (!el || e.button !== 0) return;
      e.stopPropagation();
      const id = el.dataset.id;
      if (e.target.closest('.tick')) { this.h.onToggleDone(id); return; }
      if (this.linkFrom) { this.h.onLink(this.linkFrom, id); return; }
      const n = this.board.nodes[id];
      const sx = e.clientX, sy = e.clientY, nx = n.x, ny = n.y;
      let moved = false;
      el.setPointerCapture(e.pointerId);
      const move = (ev) => {
        const dx = (ev.clientX - sx) / this.view.k, dy = (ev.clientY - sy) / this.view.k;
        if (!moved && Math.abs(dx) + Math.abs(dy) < 4 / this.view.k) return;
        if (!moved) el.classList.add('dragging');
        moved = true;
        n.x = nx + dx;
        n.y = ny + dy;
        this.disp.set(id, { x: n.x, y: n.y });
        el.style.left = `${n.x}px`;
        el.style.top = `${n.y}px`;
        this.drawEdges();
      };
      const up = () => {
        el.removeEventListener('pointermove', move);
        el.removeEventListener('pointerup', up);
        el.classList.remove('dragging');
        if (moved) { this.h.onNodeMoved(id); this.drawMinimapSoon(); } else this.h.onSelect({ type: 'node', id });
      };
      el.addEventListener('pointermove', move);
      el.addEventListener('pointerup', up);
    });

    this.labelsEl.addEventListener('pointerdown', (e) => {
      const el = e.target.closest('.elabel');
      if (!el) return;
      e.stopPropagation();
      this.h.onSelect({ type: 'edge', id: el.dataset.id });
    });

    // Minimap: click or drag to move the camera there.
    const goMini = (e) => {
      const m = this.miniMap;
      if (!m) return;
      const r = this.mini.getBoundingClientRect();
      const wx = (e.clientX - r.left - m.ox) / m.s, wy = (e.clientY - r.top - m.oy) / m.s;
      const { k } = this.view;
      this.view = { k, x: root.clientWidth / 2 - wx * k, y: root.clientHeight / 2 - wy * k };
      this.applyView();
    };
    this.mini.addEventListener('pointerdown', (e) => {
      e.stopPropagation();
      cancelAnimationFrame(this.viewRaf);
      this.mini.setPointerCapture(e.pointerId);
      goMini(e);
      const mv = (ev) => goMini(ev);
      const end = () => { this.mini.removeEventListener('pointermove', mv); this.mini.removeEventListener('pointerup', end); };
      this.mini.addEventListener('pointermove', mv);
      this.mini.addEventListener('pointerup', end);
    });
  }

  setLinkMode(fromId) {
    this.linkFrom = fromId;
    this.root.classList.toggle('linking', !!fromId);
  }

  setMotion(on) {
    this.motion = on && !matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.root.classList.toggle('still', !this.motion);
  }

  // ---------- drawing ----------
  // o: { path: {nodes:Set, edges:Set}, g: Map, sel, weights, pulse, display: {notes, numbers, minimap} }
  render(board, o = {}) {
    const fresh = this.board?.id !== board.id;
    if (fresh) {
      this.nodesEl.innerHTML = this.labelsEl.innerHTML = this.hlG.innerHTML = this.edgeG.innerHTML = this.flowG.innerHTML = '';
      this.nodeEls.clear(); this.edgeEls.clear(); this.disp.clear(); this.entering.clear(); this.drawing.clear();
      this.flowKey = '';
    }
    this.board = board;
    this.o = o;
    const sel = o.sel || {};
    const show = o.display || {};
    const animate = this.motion && !fresh;
    this.mini.hidden = show.minimap === false;

    const hs = Object.values(board.nodes).map((n) => n.h).filter((h) => Number.isFinite(h));
    const hMax = Math.max(1, ...hs);

    // States
    let born = 0;
    for (const n of Object.values(board.nodes)) {
      let el = this.nodeEls.get(n.id);
      if (!el) {
        el = document.createElement('div');
        el.dataset.id = n.id;
        this.nodesEl.append(el);
        this.nodeEls.set(n.id, el);
        if (animate) {
          this.entering.add(n.id);
          el.style.animationDelay = `${Math.min(born++ * 60, 420)}ms`; // big maps still land within ~1s
          el.addEventListener('animationend', () => { this.entering.delete(n.id); el.classList.remove('enter'); el.style.animationDelay = ''; }, { once: true });
        }
      }
      if (!this.disp.has(n.id)) {
        // Spawn at the parent's position so it flies out; otherwise appear in place.
        const parent = animate && Object.values(board.edges).find((e) => e.to === n.id && this.disp.has(e.from));
        const p = parent ? this.disp.get(parent.from) : n;
        this.disp.set(n.id, { x: p.x, y: p.y });
      }
      el.className = [
        'node', `k-${n.kind}`,
        n.done && n.kind !== 'start' ? 'done' : '',
        o.path?.nodes.has(n.id) ? 'hot' : '',
        sel.type === 'node' && sel.id === n.id ? 'sel' : '',
        o.pulse === n.id ? 'pulse' : '',
        o.g && !o.g.has(n.id) && n.kind !== 'goal' ? 'unreached' : '',
        this.entering.has(n.id) ? 'enter' : '',
      ].join(' ');
      el.style.setProperty('--tilt', `${tilt(n.id)}deg`);
      el.title = n.note || '';
      el.innerHTML = this.cardHtml(n, o, show, hMax);
    }
    for (const [id, el] of this.nodeEls) if (!board.nodes[id]) { el.remove(); this.nodeEls.delete(id); this.disp.delete(id); }
    for (const [id, el] of this.nodeEls) this.sizes[id] = { w: el.offsetWidth, h: el.offsetHeight };

    // Actions
    let drawn = 0;
    for (const e of Object.values(board.edges)) {
      let r = this.edgeEls.get(e.id);
      if (!r) {
        r = { hl: document.createElementNS(NS, 'path'), ink: document.createElementNS(NS, 'path'), label: document.createElement('div') };
        r.hl.setAttribute('class', 'hl');
        r.ink.id = `p-${e.id}`;
        r.ink.setAttribute('pathLength', '1');
        r.label.dataset.id = e.id;
        r.label.className = 'elabel'; // styled before it's measured
        this.hlG.append(r.hl);
        this.edgeG.append(r.ink);
        this.labelsEl.append(r.label);
        this.edgeEls.set(e.id, r);
        if (animate) {
          this.drawing.add(e.id);
          const delay = `${120 + Math.min(drawn++ * 50, 450)}ms`;
          r.ink.style.animationDelay = r.label.style.animationDelay = delay;
          r.ink.addEventListener('animationend', () => { this.drawing.delete(e.id); r.ink.style.animationDelay = r.label.style.animationDelay = ''; this.drawEdges(); }, { once: true });
        }
      }
      const c = edgeCost(e, o.weights);
      const done = stepsDone(e);
      r.label.title = `${e.label}${e.note ? '\n\n' + e.note : ''}`;
      r.label.innerHTML = `<div class="el-t">${esc(e.label)}</div>
        <div class="el-m"><span class="cost" style="--c:${costColor(c)}" title="cost with your weights">${fmt(c)}</span><span class="dur">${esc(durationText(e))}</span>${done ? `<span class="chk">☑ ${done}</span>` : ''}</div>`;
    }
    for (const [id, r] of this.edgeEls) if (!board.edges[id]) { r.hl.remove(); r.ink.remove(); r.label.remove(); this.edgeEls.delete(id); this.drawing.delete(id); }
    for (const [id, r] of this.edgeEls) this.lsizes[id] = { w: r.label.offsetWidth, h: r.label.offsetHeight };

    this.kick();
  }

  cardHtml(n, o, show, hMax) {
    const kindTag = n.kind === 'goal' ? '★ goal' : n.kind === 'start' ? '● you are here' : '';
    const g = o.g?.get(n.id);
    const h = n.kind === 'goal' ? 0 : n.h;
    const near = n.kind === 'start' ? 0 : n.kind === 'goal' || n.done ? 1 : Number.isFinite(h) ? 1 - h / hMax : null;
    const nums = show.numbers !== false && n.kind !== 'start'
      ? `<span>h ${fmt(h)}</span>${g != null && g > 0 ? `<span>g ${fmt(g)}</span>` : ''}` : '';
    return `
      ${n.kind === 'start' ? '' : `<button class="tick" title="${n.done ? 'Achieved — click to undo' : 'Mark as achieved'}">${n.done ? '✓' : ''}</button>`}
      ${kindTag ? `<div class="nk">${kindTag}</div>` : ''}
      <div class="nl">${esc(n.label)}</div>
      ${show.notes !== false && n.note && n.kind !== 'start' ? `<div class="nn">${esc(n.note)}</div>` : ''}
      ${nums || near != null ? `<div class="nm">${nums}${near != null && n.kind === 'state' ? `<span class="near" title="closeness to the goal"><i style="width:${Math.round(near * 100)}%"></i></span>` : ''}</div>` : ''}`;
  }

  kick() {
    if (!this.raf) this.raf = requestAnimationFrame(this.tick);
  }

  // One animation frame: ease displayed positions toward real ones, then redraw ink.
  tick() {
    this.raf = null;
    if (!this.board) return;
    const a = this.motion ? 0.2 : 1;
    let moving = false;
    for (const [id, el] of this.nodeEls) {
      const n = this.board.nodes[id], d = this.disp.get(id);
      if (!n || !d) continue;
      const dx = n.x - d.x, dy = n.y - d.y;
      if (Math.abs(dx) > 0.5 || Math.abs(dy) > 0.5) { d.x += dx * a; d.y += dy * a; moving = true; } else { d.x = n.x; d.y = n.y; }
      el.style.left = `${d.x}px`;
      el.style.top = `${d.y}px`;
    }
    this.drawEdges();
    if (moving) this.kick();
    else this.drawMinimapSoon();
  }

  drawEdges() {
    const { board, o } = this;
    if (!board) return;
    const sel = o.sel || {};
    const hot = [];
    const labels = [];
    for (const e of Object.values(board.edges)) {
      const r = this.edgeEls.get(e.id);
      const a = this.disp.get(e.from), b = this.disp.get(e.to);
      if (!r || !a || !b) continue;
      const sa = this.sizes[e.from] || { w: CARD_W, h: 80 }, sb = this.sizes[e.to] || { w: CARD_W, h: 80 };
      const x1 = a.x + sa.w, y1 = a.y + sa.h / 2, x2 = b.x - 5, y2 = b.y + sb.h / 2;
      const dx = Math.max(70, Math.abs(x2 - x1) / 2);
      const c1x = x1 + dx, c2x = x2 - dx;
      const d = `M${x1},${y1} C${c1x},${y1} ${c2x},${y2} ${x2},${y2}`;
      const isHot = o.path?.edges.has(e.id);
      const isSel = sel.type === 'edge' && sel.id === e.id;
      const cls = `${isHot ? 'hot' : ''} ${isSel ? 'sel' : ''} ${this.drawing.has(e.id) ? 'draw' : ''}`;
      r.ink.setAttribute('d', d);
      r.ink.setAttribute('class', `edge ${cls}`);
      if (this.drawing.has(e.id)) r.ink.removeAttribute('marker-end');
      else r.ink.setAttribute('marker-end', `url(#${isSel ? 'arrSel' : isHot ? 'arrHot' : 'arr'})`);
      r.hl.setAttribute('d', isHot ? d : '');
      r.label.className = `elabel ${cls}`;
      if (isHot) hot.push(e.id);

      // Label: mid-curve for neighbouring columns; for long jumps, in the first
      // gutter after the source so it never lands on a card in between.
      const bez = (t) => {
        const u = 1 - t;
        return { x: u * u * u * x1 + 3 * u * u * t * c1x + 3 * u * t * t * c2x + t * t * t * x2, y: u * u * u * y1 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t * t * t * y2 };
      };
      let p = bez(0.5);
      if (x2 - x1 > 260) {
        const tx = x1 + 95;
        let best = 0.5, bd = Infinity;
        for (let t = 0; t <= 0.5; t += 0.02) { const q = bez(t); if (Math.abs(q.x - tx) < bd) { bd = Math.abs(q.x - tx); best = t; } }
        p = bez(best);
      }
      const s = this.lsizes[e.id] || { w: LABEL_W, h: 40 };
      labels.push({ r, x: p.x, y: p.y, w: s.w, h: s.h });
    }

    // Nudge overlapping labels apart vertically.
    labels.sort((p, q) => p.y - q.y);
    for (let i = 0; i < labels.length; i++) {
      for (let j = 0; j < i; j++) {
        const A = labels[j], B = labels[i];
        if (Math.abs(A.x - B.x) < (A.w + B.w) / 2 + 4 && Math.abs(A.y - B.y) < (A.h + B.h) / 2 + 3) B.y = A.y + (A.h + B.h) / 2 + 3;
      }
    }
    for (const l of labels) { l.r.label.style.left = `${l.x}px`; l.r.label.style.top = `${l.y}px`; }

    // Ink flowing along the best path.
    const key = hot.join(',');
    if (key !== this.flowKey) {
      this.flowKey = key;
      const order = o.path ? [...o.path.edges] : [];
      this.flowG.innerHTML = order.filter((id) => this.edgeEls.has(id)).map((id, i) => `
        <circle r="4.5" class="flow"><animateMotion dur="1.6s" begin="${(i * 0.22).toFixed(2)}s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="linear"><mpath href="#p-${id}"/></animateMotion></circle>`).join('');
    }
  }

  // ---------- effects ----------
  // A shimmering placeholder card next to the state being dreamed about.
  setDreaming(id) {
    this.fxEl.querySelector('.ghost')?.remove();
    if (!id || !this.board?.nodes[id]) return;
    const d = this.disp.get(id) || this.board.nodes[id];
    const s = this.sizes[id] || { w: CARD_W, h: 80 };
    const g = document.createElement('div');
    g.className = 'ghost';
    g.style.left = `${d.x + s.w + 120}px`;
    g.style.top = `${d.y + s.h / 2 - 34}px`;
    g.innerHTML = '<span class="spin">✦</span> dreaming<span class="dots"><i>.</i><i>.</i><i>.</i></span>';
    this.fxEl.append(g);
  }

  // Stars burst out of a card (goal reached, step achieved).
  burst(id, count = 26) {
    if (!this.motion) return;
    const d = this.disp.get(id), s = this.sizes[id];
    if (!d || !s) return;
    const glyphs = ['★', '✦', '✧', '•'];
    for (let i = 0; i < count; i++) {
      const p = document.createElement('span');
      p.className = 'spark';
      p.textContent = glyphs[i % glyphs.length];
      const ang = (i / count) * Math.PI * 2 + Math.random() * 0.4, dist = 70 + Math.random() * 90;
      p.style.left = `${d.x + s.w / 2}px`;
      p.style.top = `${d.y + s.h / 2}px`;
      p.style.setProperty('--dx', `${Math.cos(ang) * dist}px`);
      p.style.setProperty('--dy', `${Math.sin(ang) * dist}px`);
      p.style.setProperty('--r', `${Math.random() * 360}deg`);
      p.style.setProperty('--hue', `${35 + Math.random() * 25}`);
      this.fxEl.append(p);
      setTimeout(() => p.remove(), 1300);
    }
  }

  // Briefly light up the states A* looked at, in the order it looked.
  scan(ids) {
    if (!this.motion) return;
    ids.forEach((id, i) => {
      const el = this.nodeEls.get(id);
      if (!el) return;
      setTimeout(() => { el.classList.remove('scan'); void el.offsetWidth; el.classList.add('scan'); }, i * 60);
      setTimeout(() => el.classList.remove('scan'), i * 60 + 700);
    });
  }

  // ---------- minimap ----------
  drawMinimapSoon() {
    if (this.miniRaf) return;
    this.miniRaf = requestAnimationFrame(() => { this.miniRaf = null; this.drawMinimap(); });
  }

  drawMinimap() {
    const cv = this.mini, b = this.board;
    if (!b || cv.hidden || !cv.offsetWidth) return;
    const W = cv.offsetWidth, H = cv.offsetHeight, dpr = devicePixelRatio || 1;
    if (cv.width !== W * dpr) { cv.width = W * dpr; cv.height = H * dpr; }
    const ctx = cv.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const ns = Object.values(b.nodes);
    if (!ns.length) return;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const n of ns) {
      const s = this.sizes[n.id] || { w: CARD_W, h: 80 };
      x0 = Math.min(x0, n.x); y0 = Math.min(y0, n.y); x1 = Math.max(x1, n.x + s.w); y1 = Math.max(y1, n.y + s.h);
    }
    const pad = 8, sc = Math.min((W - pad * 2) / (x1 - x0 || 1), (H - pad * 2) / (y1 - y0 || 1));
    const ox = pad - x0 * sc + (W - pad * 2 - (x1 - x0) * sc) / 2, oy = pad - y0 * sc + (H - pad * 2 - (y1 - y0) * sc) / 2;
    this.miniMap = { s: sc, ox, oy };
    const css = getComputedStyle(this.root);
    const v = (name) => css.getPropertyValue(name).trim();
    const X = (x) => ox + x * sc, Y = (y) => oy + y * sc;
    const hot = this.o.path?.edges || new Set();
    for (const e of Object.values(b.edges)) {
      const a = b.nodes[e.from], c = b.nodes[e.to];
      if (!a || !c) continue;
      const sa = this.sizes[a.id] || { w: CARD_W, h: 80 }, sc2 = this.sizes[c.id] || { w: CARD_W, h: 80 };
      ctx.strokeStyle = hot.has(e.id) ? v('--gold') : v('--mini-ink');
      ctx.lineWidth = hot.has(e.id) ? 2.5 : 1;
      ctx.beginPath();
      ctx.moveTo(X(a.x + sa.w), Y(a.y + sa.h / 2));
      ctx.lineTo(X(c.x), Y(c.y + sc2.h / 2));
      ctx.stroke();
    }
    for (const n of ns) {
      const s = this.sizes[n.id] || { w: CARD_W, h: 80 };
      ctx.fillStyle = n.kind === 'goal' ? v('--gold') : n.kind === 'start' ? v('--green') : n.done ? v('--done-mini') : v('--mini-card');
      ctx.fillRect(X(n.x), Y(n.y), Math.max(3, s.w * sc), Math.max(2, s.h * sc));
    }
    const { x, y, k } = this.view, R = this.root;
    ctx.strokeStyle = v('--accent');
    ctx.lineWidth = 1.5;
    ctx.strokeRect(X(-x / k), Y(-y / k), (R.clientWidth / k) * sc, (R.clientHeight / k) * sc);
  }

  // ---------- framing ----------
  bounds() {
    const ns = Object.values(this.board?.nodes || {});
    if (!ns.length) return null;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const n of ns) {
      const s = this.sizes[n.id] || { w: CARD_W, h: 80 };
      x0 = Math.min(x0, n.x); y0 = Math.min(y0, n.y);
      x1 = Math.max(x1, n.x + s.w); y1 = Math.max(y1, n.y + s.h);
    }
    return { x0, y0, x1, y1 };
  }

  fit(animate = true) {
    const bb = this.bounds();
    if (!bb) return;
    const W = this.root.clientWidth, H = this.root.clientHeight, pad = W < 600 ? 24 : 70;
    const kFit = Math.min((W - pad * 2) / (bb.x1 - bb.x0), (H - pad * 2) / (bb.y1 - bb.y0));
    const kMin = W < 600 ? 0.7 : 0.85; // never shrink cards below readable size; the minimap shows the rest
    const k = clamp(kFit, kMin, 1.15);
    const start = this.board.nodes[this.board.startId];
    const ss = this.sizes[start.id] || { w: CARD_W, h: 80 };
    // Too wide: anchor at the start. Too tall: centre on the start's row.
    const x = (bb.x1 - bb.x0) * k <= W - pad * 2 ? (W - (bb.x1 - bb.x0) * k) / 2 - bb.x0 * k : pad - bb.x0 * k;
    const y = (bb.y1 - bb.y0) * k <= H - pad * 2 ? (H - (bb.y1 - bb.y0) * k) / 2 - bb.y0 * k : H / 2 - (start.y + ss.h / 2) * k;
    this.setView({ k, x, y }, animate);
  }

  centerOn(id, animate = true) {
    const n = this.board?.nodes[id];
    if (!n) return;
    const s = this.sizes[id] || { w: CARD_W, h: 80 };
    const W = this.root.clientWidth, H = this.root.clientHeight, k = this.view.k;
    this.setView({ k, x: W / 2 - (n.x + s.w / 2) * k, y: H / 2 - (n.y + s.h / 2) * k }, animate);
  }
}
