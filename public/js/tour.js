// GoalStar Actionable Walkthrough Tour: high-contrast spotlight with a
// measured card placement, so the guide never clips and always points at the
// element it is talking about.
import { sound } from './sound.js';

const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

// Reliable target finder helpers across all boards and scenarios
function findTargetMilestone() {
  const stateNodes = Array.from(document.querySelectorAll('.node.k-state'));
  const undone = stateNodes.find((el) => !el.classList.contains('done'));
  if (undone) return undone;
  if (stateNodes.length > 0) return stateNodes[0];
  const nonStart = document.querySelector('.node:not(.k-start)');
  if (nonStart) return nonStart;
  return document.querySelector('.node');
}

function findTargetEdgeAndCost() {
  const labels = Array.from(document.querySelectorAll('.elabel'));
  if (!labels.length) return { labelEl: null, costEl: null, durEl: null, edgeId: null };

  // Prefer hot label (on the best path) if present
  let chosen = labels.find((l) => l.classList.contains('hot'));
  if (!chosen) {
    chosen = labels.find((l) => {
      const c = l.querySelector('.cost');
      return c && c.textContent.trim().length > 0 && c.textContent.trim() !== '0';
    }) || labels[0];
  }

  const costEl = chosen.querySelector('.cost') || chosen;
  const durEl = chosen.querySelector('.dur') || chosen.querySelector('.chk') || chosen;
  const edgeId = chosen.dataset.id;
  return { labelEl: chosen, costEl, durEl, edgeId };
}

export class SketchTour {
  constructor() {
    this.currentStep = 0;
    this.storageKey = 'goalstar_walkthrough_completed';
    this.overlay = null;

    this.steps = [
      {
        id: 'goal-picker',
        title: 'Goals menu',
        text: 'Switch between active goals or view the current target outcome.',
        onEnter: () => { window.clearSelect?.(); },
        targetSelector: () => document.getElementById('goalPickerBtn') || document.getElementById('boardPick')
      },
      {
        id: 'goal-head',
        title: 'Destination & progress',
        text: 'Your target outcome and real-time progress, calculated from achieved milestones and ticked steps.',
        onEnter: () => { document.body.classList.add('side-open'); window.clearSelect?.(); },
        targetSelector: () => document.querySelector('.goal-head')
      },
      {
        id: 'detail-routes',
        title: 'Granularity & routes',
        text: 'Tune <b>Detail</b> for milestone depth and <b>Routes</b> to compare multiple parallel strategies.',
        onEnter: () => { document.body.classList.add('side-open'); window.clearSelect?.(); },
        targetSelector: () => document.querySelector('.goal-opts')
      },
      {
        id: 'dream-button',
        title: 'Dream the map',
        text: 'Click <b>Dream</b> to automatically generate intermediate milestones and connecting actions.',
        onEnter: () => { window.clearSelect?.(); },
        targetSelector: () => document.getElementById('dreamBtn')
      },
      {
        id: 'search-button',
        title: 'Search optimal route',
        text: 'Runs A* pathfinding across all branches to isolate the lowest-friction route to your goal.',
        onEnter: () => { window.clearSelect?.(); },
        targetSelector: () => document.getElementById('searchBtn')
      },
      {
        id: 'best-path',
        title: 'Winning A* path',
        text: 'The optimal sequence from Start to Goal. Each step displays friction cost and estimated timeline.',
        onEnter: () => {
          document.body.classList.add('side-open');
          document.getElementById('bestPathSection')?.scrollIntoView?.({ behavior: 'auto', block: 'nearest' });
        },
        targetSelector: () => document.getElementById('bestPathSection')
      },
      {
        id: 'node-card',
        title: 'Milestone cards',
        text: 'Milestones represent real-world conditions achieved. Bars fill as preceding checklist tasks complete.',
        onEnter: () => {
          window.clearSelect?.();
          const node = findTargetMilestone();
          if (node?.dataset?.id && window.canvas) window.canvas.centerOn(node.dataset.id, false);
        },
        targetSelector: () => findTargetMilestone()
      },
      {
        id: 'action-cost',
        title: 'Action connectors',
        text: 'Connectors link milestones with friction costs, realistic durations, and sub-task checklists.',
        onEnter: () => {
          window.clearSelect?.();
          const { edgeId } = findTargetEdgeAndCost();
          if (edgeId && window.canvas) window.canvas.centerOnEdge(edgeId, false);
        },
        targetSelector: () => findTargetEdgeAndCost().labelEl || findTargetEdgeAndCost().costEl
      },
      {
        id: 'action-checklist',
        title: 'Action checklists',
        text: 'Manage granular execution steps. Checking off items dynamically advances milestone progress.',
        onEnter: () => {
          if (window.selectFirstEdge) window.selectFirstEdge();
          const ins = document.getElementById('inspector');
          if (ins) {
            ins.hidden = false;
            ins.querySelector('.checklist')?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
          }
        },
        targetSelector: () => document.querySelector('#inspector .checklist') || document.querySelector('#inspector')
      },
      {
        id: 'inspector-notes',
        title: 'Notes & resources',
        text: 'Keep links, documents, contacts, and context attached directly to each milestone and action.',
        onEnter: () => {
          if (window.selectFirstEdge) window.selectFirstEdge();
          const ins = document.getElementById('inspector');
          if (ins) {
            ins.hidden = false;
            ins.querySelector('textarea[data-f="note"]')?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
          }
        },
        targetSelector: () => document.querySelector('#inspector textarea[data-f="note"]') || document.querySelector('#inspector')
      },
      {
        id: 'inspector-actions',
        title: 'Detail, break down, decompose',
        text: 'Refine actions with checklists, split big steps, or decompose milestones stalled over 48 hours.',
        onEnter: () => {
          if (window.selectFirstEdge) window.selectFirstEdge();
          const ins = document.getElementById('inspector');
          if (ins) {
            ins.hidden = false;
            ins.querySelector('.btns')?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
          }
        },
        targetSelector: () => document.querySelector('#inspector .btns') || document.querySelector('#inspector')
      },
      {
        id: 'road-blocked',
        title: 'Handle real-world blockers',
        text: 'Mark obstacles <b>Out of reach</b> or <b>Very expensive</b>; A* reroutes around them immediately.',
        onEnter: () => {
          window.clearSelect?.();
          const node = findTargetMilestone();
          if (node?.dataset?.id) {
            window.selectNode?.(node.dataset.id);
            window.canvas?.centerOn(node.dataset.id, false);
          }
        },
        targetSelector: () => document.querySelector('#inspector .block-box') || document.querySelector('#inspector')
      },
      {
        id: 'weights',
        title: 'Personal priority sliders',
        text: 'Re-weight Time, Money, Effort, and Risk. Sliders dynamically recalculate the winning path.',
        onEnter: () => {
          window.clearSelect?.();
          document.body.classList.add('side-open');
          document.getElementById('weights')?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
        },
        targetSelector: () => document.getElementById('weights') || document.querySelector('#presets')?.parentElement
      },
      {
        id: 'walrus-banner',
        title: 'Walrus habit memory',
        text: 'Recalls historical blockers from Walrus on Mainnet, applying friction penalties to matching routes.',
        onEnter: () => {
          window.clearSelect?.();
          document.body.classList.add('side-open');
          const b = document.getElementById('lastTuesdayBanner');
          if (b && b.hidden) {
            b.hidden = false;
            b.dataset.tourTemp = 'true';
          }
          b?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
        },
        targetSelector: () => (document.getElementById('lastTuesdayBanner')?.offsetParent ? document.getElementById('lastTuesdayBanner') : null) || document.querySelector('.telemetry-box') || document.querySelector('.telemetry-pill')
      },
      {
        id: 'walrus-memory',
        title: 'Decentralized telemetry',
        text: 'Live status of Walrus storage. Log blockers and stamina notes from browser or CLI.',
        onEnter: () => {
          document.body.classList.add('side-open');
          document.querySelector('.telemetry-box')?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
        },
        targetSelector: () => document.querySelector('.telemetry-box') || document.querySelector('.telemetry-pill') || document.querySelector('.side')
      },
      {
        id: 'sui-inspector',
        title: 'Onchain Sui verification',
        text: 'Seal a finished milestone as a Walrus certificate anchored to a live Sui checkpoint. Anyone can re-check it against the chain.',
        onEnter: () => {
          if (window.selectFirstStateNode) window.selectFirstStateNode();
          const ins = document.getElementById('inspector');
          if (ins) {
            ins.hidden = false;
            (ins.querySelector('.sui-box') || ins.querySelector('.ins-head'))?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
          }
        },
        targetSelector: () => document.querySelector('.sui-box') || document.querySelector('[data-act="sui-stamp"]') || document.querySelector('#inspector')
      },
      {
        id: 'themes',
        title: 'Theme switcher',
        text: 'Toggle dark or light mode instantly with the 3D switch, or open Settings to choose palettes like Chalkboard, Blueprint, or Notebook.',
        onEnter: () => { window.clearSelect?.(); },
        targetSelector: () => (document.getElementById('themeSelect')?.offsetParent ? document.getElementById('themeSelect') : null) || document.getElementById('themeSwitch') || document.getElementById('settingsBtn')
      }
    ];

    this.handleResize = () => {
      if (this.overlay) this.renderDom(this.steps[this.currentStep]);
    };
  }

  init() {
    const bindBtn = (id) => {
      const btn = document.getElementById(id);
      if (btn) {
        btn.addEventListener('click', () => {
          window.stopTourBounce?.();
          this.start(true);
        });
      }
    };

    bindBtn('tourBtn');
    bindBtn('sideTourBtn');

    window.addEventListener('resize', this.handleResize);
  }

  start(force = false) {
    if (!force && localStorage.getItem(this.storageKey)) return;
    window.stopTourBounce?.();
    sound.play('pop');
    this.currentStep = 0;
    this.render();
  }

  goToStep(stepIndex) {
    window.stopTourBounce?.();
    sound.play('pop');
    this.currentStep = clamp(stepIndex, 0, this.steps.length - 1);
    this.render();
  }

  goToStepId(id) {
    const i = this.steps.findIndex((s) => s.id === id);
    if (i >= 0) this.goToStep(i);
  }

  next() {
    sound.play('whoosh');
    if (this.currentStep < this.steps.length - 1) {
      this.currentStep++;
      this.render();
    } else {
      this.close();
    }
  }

  prev() {
    sound.play('whoosh');
    if (this.currentStep > 0) {
      this.currentStep--;
      this.render();
    }
  }

  close() {
    sound.play('click');
    localStorage.setItem(this.storageKey, 'true');
    window.stopTourBounce?.();
    window.clearSelect?.();
    const b = document.getElementById('lastTuesdayBanner');
    if (b?.dataset?.tourTemp) {
      b.hidden = true;
      delete b.dataset.tourTemp;
    }
    if (this.overlay) {
      this.overlay.remove();
      this.overlay = null;
    }
  }

  render() {
    const step = this.steps[this.currentStep];
    if (step.onEnter) {
      try { step.onEnter(); } catch (e) { console.warn('onEnter failed', e); }
    }
    // Wait a short settle so the panel opens and the canvas finishes its camera
    // move before we measure the target.
    clearTimeout(this.renderTimer);
    this.renderTimer = setTimeout(() => this.renderDom(step), 90);
  }

  targetRect(step, spotPad) {
    let el = null;
    if (typeof step.targetSelector === 'function') {
      try { el = step.targetSelector(); } catch (e) { el = null; }
    } else if (step.targetSelector) {
      el = document.querySelector(step.targetSelector);
    }
    if (!el) return null;

    el.scrollIntoView?.({ behavior: 'auto', block: 'nearest', inline: 'nearest' });
    const r = el.getBoundingClientRect();
    const valid = (rect) => rect && (rect.width > 4 || rect.height > 4) && rect.right > 4 && rect.bottom > 4;
    if (!valid(r)) return null;

    return {
      el,
      x: clamp(r.left - spotPad, 6, window.innerWidth - 24),
      y: clamp(r.top - spotPad, 4, window.innerHeight - 24),
      w: clamp(r.width + spotPad * 2, 26, window.innerWidth - 12),
      h: clamp(r.height + spotPad * 2, 22, window.innerHeight - 8),
      raw: r
    };
  }

  renderDom(step) {
    const existingCard = this.overlay?.querySelector('.sketch-card-container');
    const cardScroll = existingCard ? existingCard.querySelector('.sketch-card')?.scrollTop : 0;

    if (!this.overlay) {
      this.overlay = document.createElement('div');
      this.overlay.className = 'sketch-tour-overlay';
      document.body.appendChild(this.overlay);
    }

    // Which edge of the UI is the target attached to? It changes where the card
    // should go; the sidebar and inspector are the risky ones.
    let el = null;
    try {
      el = typeof step.targetSelector === 'function' ? step.targetSelector() : document.querySelector(step.targetSelector);
    } catch (e) { el = null; }
    const headerEl = document.querySelector('.topbar');
    const sideEl = document.querySelector('.side');
    const inspectorEl = document.getElementById('inspector');
    const inHeader = !!(el && headerEl && headerEl.contains(el));
    const inSide = !!(el && sideEl && sideEl.contains(el));
    const inInspector = !!(el && inspectorEl && !inspectorEl.hidden && inspectorEl.contains(el));

    const spotPad = inHeader ? 5 : 8;
    let spot = this.targetRect(step, spotPad);

    // Target not laid out yet: fall back to the panel geometry, not the middle
    // of the screen, so the card still points somewhere sensible.
    if (!spot) {
      const panel = inInspector ? inspectorEl : inSide ? sideEl : headerEl;
      if (panel) {
        const r = panel.getBoundingClientRect();
        spot = {
          el: panel,
          x: clamp(r.left - spotPad, 6, window.innerWidth - 24),
          y: clamp(r.top - spotPad, 4, window.innerHeight - 24),
          w: clamp(r.width + spotPad * 2, 26, window.innerWidth - 12),
          h: clamp(r.height + spotPad * 2, 22, window.innerHeight - 8),
          raw: r
        };
      } else {
        spot = { el: null, x: Math.round(window.innerWidth / 2 - 110), y: Math.round(window.innerHeight / 2 - 40), w: 220, h: 80, raw: null };
      }
    }

    const isFirst = this.currentStep === 0;
    const isLast = this.currentStep === this.steps.length - 1;

    // Build the overlay shell. The card is inserted hidden at the origin so we
    // can measure its real height before choosing a corner for it.
    this.overlay.innerHTML = `
      <svg class="sketch-tour-svg" viewBox="0 0 ${window.innerWidth} ${window.innerHeight}" width="${window.innerWidth}" height="${window.innerHeight}">
        <defs>
          <mask id="sketch-mask">
            <rect width="100%" height="100%" fill="white" />
            <rect x="${spot.x}" y="${spot.y}" width="${spot.w}" height="${spot.h}" rx="10" ry="10" fill="black" />
          </mask>
          <marker id="sketch-arrowhead" markerWidth="12" markerHeight="12" refX="8" refY="6" orient="auto">
            <path d="M 1 2 L 10 6 L 1 10 Z" fill="#059669" stroke="#047857" stroke-width="1.2" />
          </marker>
        </defs>
        <rect width="100%" height="100%" fill="rgba(15, 23, 42, 0.52)" mask="url(#sketch-mask)" />
        <rect x="${spot.x}" y="${spot.y}" width="${spot.w}" height="${spot.h}" rx="10" ry="10"
              fill="rgba(5, 150, 105, 0.08)" stroke="#059669" stroke-width="2.5" stroke-dasharray="6 4" class="tour-spotlight-ring" />
        <g class="tour-arrow-layer"></g>
      </svg>

      <div class="sketch-card-container" style="visibility:hidden; left:0; top:0;">
        <div class="sketch-card">
          <div class="sketch-pin">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#d97706"><circle cx="12" cy="7" r="5"/><polygon points="12,12 12,22 10,14"/></svg>
          </div>
          <div class="sketch-head">
            <span class="sketch-badge">Guide · ${this.currentStep + 1} of ${this.steps.length}</span>
            <button class="sketch-close" id="tourCloseBtn" title="Close guide">&times;</button>
          </div>
          <h2 class="sketch-title">${step.title}</h2>
          <div class="sketch-text">${step.text}</div>
          <div class="sketch-foot">
            <button class="sketch-link" id="tourSkipBtn">Skip tour</button>
            <div class="sketch-nav">
              ${!isFirst ? '<button class="sketch-btn secondary" id="tourPrevBtn">Back</button>' : ''}
              <button class="sketch-btn primary" id="tourNextBtn">${isLast ? 'Finish tour' : 'Next step'}</button>
            </div>
          </div>
        </div>
      </div>
    `;

    const container = this.overlay.querySelector('.sketch-card-container');
    const card = this.overlay.querySelector('.sketch-card');
    const isMobile = window.innerWidth <= 600;
    const margin = isMobile ? 8 : 14;
    const maxAllowedW = Math.min(350, window.innerWidth - margin * 2);
    const cardW = isMobile ? Math.max(260, window.innerWidth - margin * 2) : maxAllowedW;
    container.style.width = `${cardW}px`;
    container.style.maxWidth = `${window.innerWidth - margin * 2}px`;

    const headH = headerEl?.offsetHeight || 52;
    const minTop = Math.min(headH + 6, Math.max(margin, Math.round(window.innerHeight * 0.15)));
    
    // Temporarily clear inline maxHeight to measure true rendered height with width applied
    card.style.maxHeight = 'none';
    const naturalH = card.offsetHeight || 220;
    const maxRoomH = Math.max(140, window.innerHeight - minTop - margin);
    const cardH = Math.min(naturalH, maxRoomH);
    const maxTop = Math.max(minTop, window.innerHeight - cardH - margin);

    const spaceBelow = window.innerHeight - (spot.y + spot.h);
    const spaceAbove = spot.y;
    const spaceLeft = spot.x;
    const spaceRight = window.innerWidth - (spot.x + spot.w);

    let left, top;

    if (isMobile) {
      left = (window.innerWidth - cardW) / 2;
      if (spot.y < window.innerHeight / 2) {
        top = spot.y + spot.h + 10;
      } else {
        top = spot.y - cardH - 10;
      }
    } else if (inHeader) {
      // Header sits across the top: card goes under the spotlight.
      left = spot.x + spot.w / 2 - cardW / 2;
      top = spot.y + spot.h + 12;
    } else if (inSide) {
      // Sidebar is a full-height column on the left: card goes over the canvas,
      // right of the sidebar if room permits, otherwise centered
      const sideRight = sideEl ? sideEl.getBoundingClientRect().right : spot.x + spot.w;
      if (window.innerWidth - sideRight >= cardW + margin * 2) {
        left = sideRight + 14;
        top = spot.y + spot.h / 2 - cardH / 2;
      } else {
        left = (window.innerWidth - cardW) / 2;
        top = spot.y > window.innerHeight / 2 ? spot.y - cardH - 12 : spot.y + spot.h + 12;
      }
    } else if (inInspector) {
      // Inspector is on the right: card goes to its left when there is room.
      const inspLeft = inspectorEl ? inspectorEl.getBoundingClientRect().left : spot.x;
      if (inspLeft >= cardW + margin * 2) {
        left = inspLeft - cardW - 14;
        top = spot.y + spot.h / 2 - cardH / 2;
      } else {
        left = (window.innerWidth - cardW) / 2;
        top = spot.y > window.innerHeight / 2 ? spot.y - cardH - 12 : spot.y + spot.h + 12;
      }
    } else if (spaceBelow >= cardH + 20) {
      left = spot.x + spot.w / 2 - cardW / 2;
      top = spot.y + spot.h + 14;
    } else if (spaceAbove >= cardH + 20) {
      left = spot.x + spot.w / 2 - cardW / 2;
      top = spot.y - cardH - 14;
    } else if (spaceRight >= cardW + 20) {
      left = spot.x + spot.w + 14;
      top = spot.y + spot.h / 2 - cardH / 2;
    } else if (spaceLeft >= cardW + 20) {
      left = spot.x - cardW - 14;
      top = spot.y + spot.h / 2 - cardH / 2;
    } else {
      left = (window.innerWidth - cardW) / 2;
      top = spot.y + spot.h / 2 - cardH / 2;
    }

    left = clamp(left, margin, Math.max(margin, window.innerWidth - cardW - margin));
    top = clamp(top, minTop, maxTop);

    // Dynamic max-height constraint so the card NEVER overflows the viewport bottom:
    const fitH = Math.max(130, window.innerHeight - top - margin);
    card.style.maxHeight = `${Math.floor(fitH)}px`;
    card.style.overflowY = 'auto';

    container.style.left = `${Math.round(left)}px`;
    container.style.top = `${Math.round(top)}px`;
    container.style.visibility = 'visible';
    if (cardScroll) card.scrollTop = cardScroll;

    // Arrow: card edge -> spotlight edge, along the line between their centres.
    this.drawArrow(spot, { left, top, w: cardW, h: cardH });

    document.getElementById('tourNextBtn')?.addEventListener('click', () => this.next());
    document.getElementById('tourPrevBtn')?.addEventListener('click', () => this.prev());
    document.getElementById('tourCloseBtn')?.addEventListener('click', () => this.close());
    document.getElementById('tourSkipBtn')?.addEventListener('click', () => this.close());
  }

  // Intersect the segment from rect centre toward `target` with the rect edge.
  rectEdge(rect, target) {
    const cx = rect.left + rect.w / 2;
    const cy = rect.top + rect.h / 2;
    const dx = target.x - cx;
    const dy = target.y - cy;
    if (!dx && !dy) return { x: cx, y: cy };
    const sx = dx ? (rect.w / 2) / Math.abs(dx) : Infinity;
    const sy = dy ? (rect.h / 2) / Math.abs(dy) : Infinity;
    const s = Math.min(sx, sy);
    return { x: cx + dx * s, y: cy + dy * s };
  }

  drawArrow(spot, cardBox) {
    const layer = this.overlay?.querySelector('.tour-arrow-layer');
    if (!layer) return;
    const cardRect = { left: cardBox.left, top: cardBox.top, w: cardBox.w, h: cardBox.h };
    const spotRect = { left: spot.x, top: spot.y, w: spot.w, h: spot.h };
    const sc = { x: spotRect.left + spotRect.w / 2, y: spotRect.top + spotRect.h / 2 };
    const cc = { x: cardRect.left + cardRect.w / 2, y: cardRect.top + cardRect.h / 2 };

    const from = this.rectEdge(cardRect, sc);
    const to = this.rectEdge(spotRect, cc);

    const dist = Math.hypot(to.x - from.x, to.y - from.y);
    if (dist < 10) return;

    // Gentle curve, perpendicular to the arrow, so it looks hand-drawn.
    const mx = (from.x + to.x) / 2;
    const my = (from.y + to.y) / 2;
    const nx = -(to.y - from.y) / dist;
    const ny = (to.x - from.x) / dist;
    const bend = Math.min(38, dist * 0.16);
    const ctrl = { x: mx + nx * bend, y: my + ny * bend };

    layer.innerHTML = `
      <path d="M ${from.x} ${from.y} Q ${ctrl.x} ${ctrl.y} ${to.x} ${to.y}"
            fill="none" stroke="#059669" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"
            marker-end="url(#sketch-arrowhead)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.3))"/>
      <circle cx="${from.x}" cy="${from.y}" r="3.5" fill="#059669" stroke="#047857" stroke-width="1.5"/>
    `;
  }
}

export const tour = new SketchTour();
if (typeof window !== 'undefined') {
  window.tour = tour;
  window.replayTour = () => tour.start(true);
  window.addEventListener('DOMContentLoaded', () => tour.init());
}
