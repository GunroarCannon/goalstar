// The lined-paper canvas: HTML index cards for states, SVG ink for actions.
import { edgeCost } from './astar.js';

export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const trunc = (s, n) => (s.length > n ? s.slice(0, n - 1) + '…' : s);
const tilt = (id) => {
  let h = 0;
  for (const c of id) h = (h * 31 + c.charCodeAt(0)) | 0;
  return ((h % 100) / 100) * 1.6;
};
const fmt = (v) => (v == null || !Number.isFinite(v) ? '?' : Math.round(v * 10) / 10);

export class Canvas {
  constructor(root, handlers) {
    this.root = root;
    this.h = handlers;
    this.view = { x: 40, y: 40, k: 1 };
    this.sizes = {};
    this.linkFrom = null;
    this.board = null;
    this.o = {};
    root.innerHTML = `
      <div class="world">
        <svg class="edges" aria-hidden="true">
          <defs>
            <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#3a3f58"/></marker>
            <marker id="arrHot" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9a6a00"/></marker>
            <marker id="arrSel" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#3557c5"/></marker>
          </defs>
          <g class="hl-g"></g><g class="edge-g"></g>
        </svg>
        <div class="labels"></div>
        <div class="nodes"></div>
      </div>
      <div class="hint">double-click paper: new state · drag: pan · scroll: zoom</div>`;
    this.world = root.querySelector('.world');
    this.hlG = root.querySelector('.hl-g');
    this.edgeG = root.querySelector('.edge-g');
    this.labelsEl = root.querySelector('.labels');
    this.nodesEl = root.querySelector('.nodes');
    this.bind();
    this.applyView();
  }

  applyView() {
    const { x, y, k } = this.view;
    this.world.style.transform = `translate(${x}px, ${y}px) scale(${k})`;
    this.root.style.setProperty('--gap', `${28 * k}px`);
    this.root.style.setProperty('--oy', `${y}px`);
  }

  toWorld(cx, cy) {
    const r = this.root.getBoundingClientRect();
    return { x: (cx - r.left - this.view.x) / this.view.k, y: (cy - r.top - this.view.y) / this.view.k };
  }

  bind() {
    const root = this.root;

    root.addEventListener('pointerdown', (e) => {
      if (e.target.closest('.node, .elabel') || e.button !== 0) return;
      const sx = e.clientX, sy = e.clientY, ox = this.view.x, oy = this.view.y;
      let moved = false;
      root.setPointerCapture(e.pointerId);
      root.classList.add('panning');
      const move = (ev) => {
        const dx = ev.clientX - sx, dy = ev.clientY - sy;
        if (Math.abs(dx) + Math.abs(dy) > 3) moved = true;
        this.view.x = ox + dx;
        this.view.y = oy + dy;
        this.applyView();
      };
      const up = () => {
        root.removeEventListener('pointermove', move);
        root.removeEventListener('pointerup', up);
        root.classList.remove('panning');
        if (!moved) this.h.onBackgroundClick();
      };
      root.addEventListener('pointermove', move);
      root.addEventListener('pointerup', up);
    });

    root.addEventListener('wheel', (e) => {
      e.preventDefault();
      const r = root.getBoundingClientRect();
      const mx = e.clientX - r.left, my = e.clientY - r.top;
      const k0 = this.view.k;
      const k = Math.min(2.5, Math.max(0.2, k0 * Math.exp(-e.deltaY * 0.0015)));
      this.view.x = mx - ((mx - this.view.x) * k) / k0;
      this.view.y = my - ((my - this.view.y) * k) / k0;
      this.view.k = k;
      this.applyView();
    }, { passive: false });

    root.addEventListener('dblclick', (e) => {
      if (e.target.closest('.node, .elabel')) return;
      const p = this.toWorld(e.clientX, e.clientY);
      this.h.onBackgroundDblClick(p.x, p.y);
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
        moved = true;
        n.x = nx + dx;
        n.y = ny + dy;
        el.style.left = `${n.x}px`;
        el.style.top = `${n.y}px`;
        this.drawEdges();
      };
      const up = () => {
        el.removeEventListener('pointermove', move);
        el.removeEventListener('pointerup', up);
        if (moved) this.h.onNodeMoved(id);
        else this.h.onSelect({ type: 'node', id });
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
  }

  setLinkMode(fromId) {
    this.linkFrom = fromId;
    this.root.classList.toggle('linking', !!fromId);
  }

  // o: { path: {nodes:Set, edges:Set}, g: Map, sel, weights, pulse }
  render(board, o = {}) {
    this.board = board;
    this.o = o;
    const sel = o.sel || {};
    this.nodesEl.innerHTML = Object.values(board.nodes).map((n) => {
      const cls = [
        `k-${n.kind}`,
        n.done && n.kind !== 'start' ? 'done' : '',
        o.path?.nodes.has(n.id) ? 'hot' : '',
        sel.type === 'node' && sel.id === n.id ? 'sel' : '',
        o.pulse === n.id ? 'pulse' : '',
        o.g && !o.g.has(n.id) && n.kind !== 'goal' ? 'unreached' : '',
      ].join(' ');
      const kindTag = n.kind === 'goal' ? '★ goal' : n.kind === 'start' ? '● you are here' : '';
      const g = o.g?.get(n.id);
      const meta = n.kind === 'start' ? '' : `h ${fmt(n.id === board.goalId ? 0 : n.h)}${g != null && g > 0 ? ` · g ${fmt(g)}` : ''}`;
      return `<div class="node ${cls}" data-id="${n.id}" style="left:${n.x}px;top:${n.y}px;--tilt:${tilt(n.id)}deg" title="${esc(n.note)}">
        ${n.kind === 'start' ? '' : `<button class="tick" title="${n.done ? 'Achieved — click to undo' : 'Mark as achieved'}">${n.done ? '✓' : ''}</button>`}
        ${kindTag ? `<div class="nk">${kindTag}</div>` : ''}
        <div class="nl">${esc(n.label)}</div>
        ${meta ? `<div class="nm">${meta}</div>` : ''}
      </div>`;
    }).join('');
    for (const el of this.nodesEl.children) this.sizes[el.dataset.id] = { w: el.offsetWidth, h: el.offsetHeight };
    this.drawEdges();
  }

  drawEdges() {
    const { board, o } = this;
    if (!board) return;
    const sel = o.sel || {};
    let hl = '', ink = '', labels = '';
    for (const e of Object.values(board.edges)) {
      const a = board.nodes[e.from], b = board.nodes[e.to];
      if (!a || !b) continue;
      const sa = this.sizes[a.id] || { w: 210, h: 70 }, sb = this.sizes[b.id] || { w: 210, h: 70 };
      const x1 = a.x + sa.w, y1 = a.y + sa.h / 2, x2 = b.x - 4, y2 = b.y + sb.h / 2;
      const dx = Math.max(60, Math.abs(x2 - x1) / 2);
      const c1x = x1 + dx, c2x = x2 - dx;
      const d = `M${x1},${y1} C${c1x},${y1} ${c2x},${y2} ${x2},${y2}`;
      const mx = (x1 + 3 * c1x + 3 * c2x + x2) / 8, my = (y1 + y2) / 2;
      const hot = o.path?.edges.has(e.id);
      const isSel = sel.type === 'edge' && sel.id === e.id;
      const cls = `${hot ? 'hot' : ''} ${isSel ? 'sel' : ''}`;
      if (hot) hl += `<path class="hl" d="${d}"/>`;
      ink += `<path class="edge ${cls}" d="${d}" marker-end="url(#${isSel ? 'arrSel' : hot ? 'arrHot' : 'arr'})"/>`;
      labels += `<div class="elabel ${cls}" data-id="${e.id}" style="left:${mx}px;top:${my}px" title="${esc(e.label)}">${esc(trunc(e.label, 56))} <span class="cost">${fmt(edgeCost(e, o.weights))}</span></div>`;
    }
    this.hlG.innerHTML = hl;
    this.edgeG.innerHTML = ink;
    this.labelsEl.innerHTML = labels;
  }

  fit() {
    const ns = Object.values(this.board?.nodes || {});
    if (!ns.length) return;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const n of ns) {
      const s = this.sizes[n.id] || { w: 210, h: 70 };
      x0 = Math.min(x0, n.x); y0 = Math.min(y0, n.y);
      x1 = Math.max(x1, n.x + s.w); y1 = Math.max(y1, n.y + s.h);
    }
    const W = this.root.clientWidth, H = this.root.clientHeight, pad = 70;
    const kFit = Math.min((W - pad * 2) / (x1 - x0), (H - pad * 2) / (y1 - y0));
    const k = Math.min(1.3, Math.max(0.6, kFit)); // never shrink cards below readable size
    const x = kFit >= 0.6 ? (W - (x1 - x0) * k) / 2 - x0 * k : pad - x0 * k; // too big: anchor at the start
    this.view = { k, x, y: (H - (y1 - y0) * k) / 2 - y0 * k };
    this.applyView();
  }

  centerOn(id) {
    const n = this.board?.nodes[id];
    if (!n) return;
    const s = this.sizes[id] || { w: 210, h: 70 };
    const W = this.root.clientWidth, H = this.root.clientHeight;
    this.view.x = W / 2 - (n.x + s.w / 2) * this.view.k;
    this.view.y = H / 2 - (n.y + s.h / 2) * this.view.k;
    this.applyView();
  }
}
