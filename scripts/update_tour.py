import re

tour_code = '''// GoalStar Actionable Walkthrough Tour: "How to Easily Do Stuff & Log In"
// Hand-drawn sketch aesthetic matching Caveat & Patrick Hand typography
import { sound } from './sound.js';

export class SketchTour {
  constructor() {
    this.currentStep = 0;
    this.storageKey = 'goalstar_walkthrough_completed';
    this.overlay = null;

    this.steps = [
      {
        id: 'login',
        targetSelector: '#loginBtn',
        fallbackSelector: '#userBadge',
        title: '🔑 Step 1: Log In & Carry Your Memory',
        text: 'Start here! Click <b>Log In</b> to connect your <b>Sui Wallet</b>, <b>Walrus Memory ID</b>, or jump in with a <b>One-Click Demo</b>. Unlike other tools that reset every session, GoalStar permanently remembers your habits, past bottlenecks, and stamina rules.<br><button id="tourOpenLoginBtn" class="mini-btn" style="margin-top: 8px; font-size: 14px;">Try Logging In Now ➔</button>',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(20, Math.min(window.innerWidth - cardW - 20, targetRect.left - cardW / 2)),
          top: targetRect.bottom + 16
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + cardW / 2, y: cardPos.top },
            to: { x: targetRect.left + targetRect.width / 2, y: targetRect.bottom + 2 },
            ctrl: { x: cardPos.left + cardW / 2, y: (cardPos.top + targetRect.bottom) / 2 }
          }
        ],
        onEnter: () => {
          window.clearSelect?.();
          setTimeout(() => {
            document.getElementById('tourOpenLoginBtn')?.addEventListener('click', () => {
              if (window.auth) window.auth.openLoginModal();
            });
          }, 120);
        }
      },
      {
        id: 'goal',
        targetSelector: '#boardPick',
        fallbackSelector: '#newGoalBtn',
        title: '✦ Step 2: Choose or Dream Any Goal',
        text: 'Switch between goals using the dropdown or click <b>+ New Goal</b>. Simply state where you are today and where you want to go. GoalStar dreams the milestones in between so you never face a blank canvas.',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(20, Math.min(window.innerWidth - cardW - 20, targetRect.left - 20)),
          top: targetRect.bottom + 16
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + 80, y: cardPos.top },
            to: { x: targetRect.left + 50, y: targetRect.bottom + 2 },
            ctrl: { x: cardPos.left + 60, y: (cardPos.top + targetRect.bottom) / 2 }
          }
        ],
        onEnter: () => {
          window.clearSelect?.();
        }
      },
      {
        id: 'astar',
        targetSelector: '.node[data-id="n_devops"]',
        fallbackSelector: '.node',
        title: '🧭 Step 3: Click Nodes to See Action Checklists',
        text: 'The glowing green trail is your calculated <b>lowest-friction route</b>. Click any milestone card to view its checklist, examine potential pitfalls, or check off tasks as you finish them!',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, targetRect.left - cardW - 35),
          top: Math.max(120, targetRect.top - 15)
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => {
          const paasNode = document.querySelector('.node[data-id="n_paas"]');
          const paasRect = paasNode ? paasNode.getBoundingClientRect() : null;
          const list = [
            {
              from: { x: cardPos.left + cardW, y: cardPos.top + 45 },
              to: { x: targetRect.left - 4, y: targetRect.top + targetRect.height / 2 },
              ctrl: { x: (cardPos.left + cardW + targetRect.left) / 2, y: cardPos.top + 35 },
              color: '#f59e0b'
            }
          ];
          if (paasRect) {
            list.push({
              from: { x: cardPos.left + cardW, y: cardPos.top + 85 },
              to: { x: paasRect.left - 4, y: Math.min(window.innerHeight - 140, paasRect.top + 25) },
              ctrl: { x: (cardPos.left + cardW + paasRect.left) / 2, y: cardPos.top + 70 },
              color: '#10b981',
              marker: 'sketch-arrowhead-green'
            });
          }
          return list;
        },
        onEnter: () => {
          window.clearSelect?.();
        }
      },
      {
        id: 'weights',
        targetSelector: '#weights',
        fallbackSelector: '#presets',
        title: '🎚️ Step 4: Drag Sliders to Reroute Instantly',
        text: 'Feeling exhausted? Turn up <b>Effort</b>. Low on budget? Increase <b>Money</b>. GoalStar instantly recalculates and physically routes your green path around heavy roadblocks!',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, targetRect.right + 25),
          top: Math.max(100, Math.min(window.innerHeight - 240, targetRect.top - 20))
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left, y: cardPos.top + 50 },
            to: { x: targetRect.right + 4, y: targetRect.top + 30 },
            ctrl: { x: (cardPos.left + targetRect.right) / 2 - 15, y: cardPos.top + 40 }
          }
        ],
        onEnter: () => {
          const side = document.querySelector('.side');
          const wBox = document.getElementById('weights');
          if (side && wBox) {
            side.scrollTo({ top: wBox.offsetTop - 120, behavior: 'smooth' });
          }
        }
      },
      {
        id: 'escalation',
        targetSelector: '#lastTuesdayBanner',
        title: '⚡ Step 5: Log Blockers & 48h Watchdog',
        text: 'Hit a wall? Click <b>+ Log Progress</b> to note your friction. If any milestone sits untouched for <b>48 hours</b>, the watchdog automatically decomposes it into simple <b>15-minute micro-actions</b>.',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, Math.min(window.innerWidth - cardW - 20, targetRect.left + 15)),
          top: targetRect.bottom + 16
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + 120, y: cardPos.top },
            to: { x: targetRect.left + 120, y: targetRect.bottom + 2 },
            ctrl: { x: cardPos.left + 90, y: (cardPos.top + targetRect.bottom) / 2 }
          }
        ],
        onEnter: () => {
          window.clearSelect?.();
          document.querySelector('.side')?.scrollTo({ top: 0, behavior: 'smooth' });
        }
      },
      {
        id: 'sui',
        targetSelector: '[data-act="sui-stamp"]',
        fallbackSelector: '#inspector',
        title: '📜 Step 6: Stamp Verifiable Proof on Sui',
        text: 'When you finish a major deliverable, click <b>Stamp on Sui Mainnet</b>. Powered by Tatum RPC, you get permanent cryptographic proof of your milestone that you can share with anyone!',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, targetRect.left - cardW - 35),
          top: Math.max(110, Math.min(window.innerHeight - 240, targetRect.top - 50))
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + cardW, y: cardPos.top + 65 },
            to: { x: targetRect.left - 6, y: targetRect.top + targetRect.height / 2 },
            ctrl: { x: (cardPos.left + cardW + targetRect.left) / 2, y: cardPos.top + 55 }
          }
        ],
        onEnter: () => {
          window.selectNode?.('n_arch');
        }
      }
    ];

    this.handleResize = () => {
      if (this.overlay) this.render();
    };
  }

  init() {
    const bindBtn = (id) => {
      const btn = document.getElementById(id);
      if (btn) btn.addEventListener('click', () => this.start(true));
    };

    bindBtn('tourBtn');
    bindBtn('sideTourBtn');

    window.addEventListener('resize', this.handleResize);

    if (!localStorage.getItem(this.storageKey)) {
      setTimeout(() => this.start(false), 1200);
    }
  }

  start(force = false) {
    if (!force && localStorage.getItem(this.storageKey)) return;
    sound.play('pop');
    this.currentStep = 0;
    this.render();
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
    window.clearSelect?.();
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

    setTimeout(() => this.renderDom(step), 80);
  }

  renderDom(step) {
    if (!this.overlay) {
      this.overlay = document.createElement('div');
      this.overlay.className = 'sketch-tour-overlay';
      document.body.appendChild(this.overlay);
    }

    const cardW = 320;
    const cardH = 185;

    let targetEl = document.querySelector(step.targetSelector);
    if (!targetEl && step.fallbackSelector) {
      targetEl = document.querySelector(step.fallbackSelector);
    }

    let targetRect = targetEl ? targetEl.getBoundingClientRect() : {
      left: window.innerWidth / 2 - 120,
      top: 80,
      width: 240,
      height: 80,
      right: window.innerWidth / 2 + 120,
      bottom: 160
    };

    let cardPos = step.cardPos
      ? step.cardPos(targetRect, cardW, cardH)
      : { left: window.innerWidth / 2 - cardW / 2, top: window.innerHeight / 2 - cardH / 2 };

    cardPos.left = Math.max(15, Math.min(window.innerWidth - cardW - 15, cardPos.left));
    cardPos.top = Math.max(15, Math.min(window.innerHeight - cardH - 15, cardPos.top));

    const pad = 6;
    const spotX = Math.max(0, targetRect.left - pad);
    const spotY = Math.max(0, targetRect.top - pad);
    const spotW = Math.max(30, targetRect.width + pad * 2);
    const spotH = Math.max(30, targetRect.height + pad * 2);

    const arrows = step.arrows ? step.arrows(targetRect, cardPos, cardW, cardH) : [];
    let arrowsMarkup = '';
    for (const a of arrows) {
      const color = a.color || '#f59e0b';
      const markerId = a.marker || 'sketch-arrowhead';
      arrowsMarkup += `
        <path d="M ${a.from.x} ${a.from.y} Q ${a.ctrl.x} ${a.ctrl.y} ${a.to.x} ${a.to.y}" 
              fill="none" stroke="${color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"
              marker-end="url(#${markerId})" filter="drop-shadow(1px 1px 0 rgba(0,0,0,0.25))"/>
      `;
    }

    const isFirst = this.currentStep === 0;
    const isLast = this.currentStep === this.steps.length - 1;

    this.overlay.innerHTML = `
      <svg class="sketch-tour-svg" viewBox="0 0 ${window.innerWidth} ${window.innerHeight}">
        <defs>
          <mask id="sketch-mask">
            <rect width="100%" height="100%" fill="white" />
            <rect x="${spotX}" y="${spotY}" width="${spotW}" height="${spotH}" rx="8" ry="8" fill="black" />
          </mask>
          <marker id="sketch-arrowhead" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
            <path d="M 1 1 L 8 5 L 1 9 Z" fill="#f59e0b" stroke="#854d0e" stroke-width="1.2" />
          </marker>
          <marker id="sketch-arrowhead-green" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
            <path d="M 1 1 L 8 5 L 1 9 Z" fill="#10b981" stroke="#065f46" stroke-width="1.2" />
          </marker>
        </defs>
        <rect width="100%" height="100%" fill="rgba(24, 22, 18, 0.48)" mask="url(#sketch-mask)" />
        <rect x="${spotX}" y="${spotY}" width="${spotW}" height="${spotH}" rx="8" ry="8"
              fill="rgba(245, 158, 11, 0.04)" stroke="#f59e0b" stroke-width="2" stroke-dasharray="6 4" />
        ${arrowsMarkup}
      </svg>

      <div class="sketch-card-container" style="left: ${cardPos.left}px; top: ${cardPos.top}px;">
        <div class="sketch-card">
          <div class="sketch-pin">📌</div>
          <div class="sketch-head">
            <span class="sketch-badge">Guide (${this.currentStep + 1}/${this.steps.length})</span>
            <button class="sketch-close" id="tourCloseBtn" title="Close guide">&times;</button>
          </div>
          <h2 class="sketch-title">${step.title}</h2>
          <div class="sketch-text">${step.text}</div>
          <div class="sketch-foot">
            <button class="sketch-link" id="tourSkipBtn">Skip</button>
            <div class="sketch-nav">
              ${!isFirst ? '<button class="sketch-btn secondary" id="tourPrevBtn">Back</button>' : ''}
              <button class="sketch-btn primary" id="tourNextBtn">${isLast ? 'Done! 🚀' : 'Next ➔'}</button>
            </div>
          </div>
        </div>
      </div>
    `;

    document.getElementById('tourNextBtn')?.addEventListener('click', () => this.next());
    document.getElementById('tourPrevBtn')?.addEventListener('click', () => this.prev());
    document.getElementById('tourCloseBtn')?.addEventListener('click', () => this.close());
    document.getElementById('tourSkipBtn')?.addEventListener('click', () => this.close());
  }
}

export const tour = new SketchTour();
if (typeof window !== 'undefined') {
  window.tour = tour;
  window.replayTour = () => tour.start(true);
  window.addEventListener('DOMContentLoaded', () => tour.init());
}
'''

with open(r'C:\Users\hmmm\goalstar-recall\js\tour.js', 'w', encoding='utf-8') as f:
    f.write(tour_code)

print('Updated js/tour.js successfully')
