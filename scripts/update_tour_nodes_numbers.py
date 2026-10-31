import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update css/style.css
css_path = r'C:\Users\hmmm\goalstar-recall\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Ensure .node has z-index: 10
css = css.replace(
    '.node {\n  position: absolute;\n  width: 230px;',
    '.node {\n  position: absolute;\n  z-index: 10;\n  width: 230px;'
)

# Ensure .elabel has solid panel background and z-index 5
old_elabel = """.elabel {
  position: absolute;
  transform: translate(-50%, -50%);
  width: max-content;
  max-width: 170px;
  font-family: var(--hand);
  font-size: 14.5px;
  line-height: 1.14;
  color: var(--ink-soft);
  background: var(--label-bg);
  border: 1px solid transparent;
  padding: 3px 8px 4px;
  border-radius: 9px;
  text-align: center;
  cursor: pointer;
  user-select: none;
  transition: background 0.15s, box-shadow 0.15s, border-color 0.15s;
}"""

new_elabel = """.elabel {
  position: absolute;
  transform: translate(-50%, -50%);
  width: max-content;
  max-width: 170px;
  font-family: var(--hand);
  font-size: 14.5px;
  line-height: 1.14;
  color: var(--ink-soft);
  background: var(--panel);
  border: 1px solid var(--border);
  padding: 3px 8px 4px;
  border-radius: 9px;
  text-align: center;
  cursor: pointer;
  user-select: none;
  z-index: 5;
  box-shadow: 0 1px 4px var(--shadow);
  transition: background 0.15s, box-shadow 0.15s, border-color 0.15s;
}"""

if old_elabel in css:
    css = css.replace(old_elabel, new_elabel)
    print("SUCCESS: Updated .elabel CSS!")
else:
    print("Note: replacing elabel background via regex...")
    css = re.sub(r'background:\s*var\(--label-bg\);', 'background: var(--panel); border: 1px solid var(--border); z-index: 5; box-shadow: 0 1px 4px var(--shadow);', css)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated css/style.css!")

# 2. Update js/app.js to expose window.selectFirstStateNode
app_path = r'C:\Users\hmmm\goalstar-recall\js\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    app_text = f.read()

target_select = "window.selectNode = (id) => select({ type: 'node', id });"
replacement_select = """window.selectNode = (id) => select({ type: 'node', id });
window.selectFirstStateNode = () => {
  const b = board();
  if (!b) return null;
  const stateNode = Object.values(b.nodes).find(n => n.kind === 'state') || Object.values(b.nodes)[0];
  if (stateNode) {
    select({ type: 'node', id: stateNode.id });
    return stateNode.id;
  }
  return null;
};"""

if target_select in app_text and 'window.selectFirstStateNode' not in app_text:
    app_text = app_text.replace(target_select, replacement_select)
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(app_text)
    print("SUCCESS: Added window.selectFirstStateNode to js/app.js!")

# 3. Completely overhaul js/tour.js to point to actual nodes & numbers and prevent (0,0) fallback
tour_path = r'C:\Users\hmmm\goalstar-recall\js\tour.js'
with open(tour_path, 'r', encoding='utf-8') as f:
    tour_text = f.read()

# Replace steps definition
new_tour_steps = """this.steps = [
      {
        id: 'node-card',
        targetSelector: () => document.querySelector('.node:not(.k-start)') || document.querySelector('.node'),
        title: 'Step 1: Milestone Card & Checkbox',
        text: 'Each card is a milestone. Click the circle to mark it done, or click the card to inspect.',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, targetRect.left - cardW - 35),
          top: Math.max(90, targetRect.top - 20)
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + cardW, y: cardPos.top + 45 },
            to: { x: targetRect.left - 4, y: targetRect.top + targetRect.height / 2 },
            ctrl: { x: (cardPos.left + cardW + targetRect.left) / 2, y: cardPos.top + 35 },
            color: '#10b981'
          }
        ],
        onEnter: () => {
          window.clearSelect?.();
        }
      },
      {
        id: 'heuristic-num',
        targetSelector: () => {
          const n = document.querySelector('.node:not(.k-start)') || document.querySelector('.node');
          return n ? (n.querySelector('.nm span:first-child') || n.querySelector('.nm') || n) : null;
        },
        title: 'Step 2: Heuristic Friction (h)',
        text: 'The "h" number (e.g. h 8.5) is the estimated remaining friction from this state to your final goal.',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, targetRect.left - cardW - 30),
          top: Math.max(90, targetRect.bottom + 12)
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + cardW - 20, y: cardPos.top },
            to: { x: targetRect.left + targetRect.width / 2, y: targetRect.bottom + 2 },
            ctrl: { x: cardPos.left + cardW - 20, y: (cardPos.top + targetRect.bottom) / 2 },
            color: '#f59e0b'
          }
        ],
        onEnter: () => {
          window.clearSelect?.();
        }
      },
      {
        id: 'action-cost',
        targetSelector: () => document.querySelector('.elabel.hot .cost') || document.querySelector('.elabel .cost') || document.querySelector('.elabel'),
        title: 'Step 3: Action Cost (g score)',
        text: 'The number on the connector (e.g. 1.5, 2.4) is the friction score combining Time, Money, Effort, and Risk.',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, Math.min(window.innerWidth - cardW - 20, targetRect.left - cardW / 2)),
          top: Math.max(90, targetRect.bottom + 18)
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + cardW / 2, y: cardPos.top },
            to: { x: targetRect.left + targetRect.width / 2, y: targetRect.bottom + 2 },
            ctrl: { x: cardPos.left + cardW / 2, y: (cardPos.top + targetRect.bottom) / 2 },
            color: '#10b981'
          }
        ],
        onEnter: () => {
          window.clearSelect?.();
        }
      },
      {
        id: 'action-tasks',
        targetSelector: () => document.querySelector('.elabel.hot .dur') || document.querySelector('.elabel .dur') || document.querySelector('.elabel'),
        title: 'Step 4: Timeline & Checklist (0/3)',
        text: 'Shows estimated calendar time and completed checklist progress (e.g. ≈ 3 days, 0/3 tasks finished).',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, Math.min(window.innerWidth - cardW - 20, targetRect.left - cardW / 2)),
          top: Math.max(90, targetRect.bottom + 18)
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + cardW / 2, y: cardPos.top },
            to: { x: targetRect.left + targetRect.width / 2, y: targetRect.bottom + 2 },
            ctrl: { x: cardPos.left + cardW / 2, y: (cardPos.top + targetRect.bottom) / 2 },
            color: '#f59e0b'
          }
        ],
        onEnter: () => {
          window.clearSelect?.();
        }
      },
      {
        id: 'weights-profile',
        targetSelector: () => document.querySelector('#profile:not([hidden])') || document.querySelector('#weights') || document.querySelector('.side'),
        title: 'Step 5: 4-D Friction Breakdown',
        text: 'The 4 colored bars break down friction into Time, Money, Effort, and Risk across your journey.',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, targetRect.right + 25),
          top: Math.max(100, Math.min(window.innerHeight - 240, targetRect.top - 10))
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left, y: cardPos.top + 45 },
            to: { x: targetRect.right + 4, y: targetRect.top + 25 },
            ctrl: { x: (cardPos.left + targetRect.right) / 2 - 10, y: cardPos.top + 35 },
            color: '#10b981'
          }
        ],
        onEnter: () => {
          const side = document.querySelector('.side');
          const prof = document.getElementById('profile');
          if (side && prof) {
            side.scrollTo({ top: prof.offsetTop - 100, behavior: 'smooth' });
          }
        }
      },
      {
        id: 'sui-inspector',
        targetSelector: () => document.querySelector('[data-act="sui-stamp"]') || document.querySelector('.inspector') || document.querySelector('aside.side-panel'),
        title: 'Step 6: Inspector & Verifiable Proof',
        text: 'Take notes, check off steps, or click "Stamp on Sui" for immutable blockchain proof.',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(340, targetRect.left - cardW - 35),
          top: Math.max(110, Math.min(window.innerHeight - 240, targetRect.top - 30))
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + cardW, y: cardPos.top + 55 },
            to: { x: targetRect.left - 6, y: targetRect.top + Math.min(100, targetRect.height / 2) },
            ctrl: { x: (cardPos.left + cardW + targetRect.left) / 2, y: cardPos.top + 45 },
            color: '#10b981'
          }
        ],
        onEnter: () => {
          if (window.selectFirstStateNode) {
            window.selectFirstStateNode();
          }
        }
      }
    ];"""

tour_text = re.sub(r'this\.steps\s*=\s*\[[\s\S]*?\];\s*this\.handleResize', new_tour_steps + '\n\n    this.handleResize', tour_text)

# Also update renderDom in tour.js to strictly prevent (0,0) fallback!
old_render_dom_rect_pattern = r'let targetEl = document\.querySelector\(step\.targetSelector\);[\s\S]*?let targetRect = targetEl \? targetEl\.getBoundingClientRect\(\) : \{[\s\S]*?\};'

new_render_dom_rect = """let targetEl = null;
    if (typeof step.targetSelector === 'function') {
      try { targetEl = step.targetSelector(); } catch(e) {}
    } else if (step.targetSelector) {
      targetEl = document.querySelector(step.targetSelector);
    }
    if (!targetEl && step.fallbackSelector) {
      try {
        targetEl = typeof step.fallbackSelector === 'function' ? step.fallbackSelector() : document.querySelector(step.fallbackSelector);
      } catch(e) {}
    }

    const isValidRect = (r) => r && (r.width > 4 || r.height > 4) && (r.right > 20 || r.bottom > 20) && (r.left > 10 || r.top > 10);
    let tr = targetEl ? targetEl.getBoundingClientRect() : null;

    let targetRect = (tr && isValidRect(tr)) ? tr : {
      left: Math.max(340, window.innerWidth / 2 - 120),
      top: 140,
      width: 240,
      height: 80,
      right: Math.max(580, window.innerWidth / 2 + 120),
      bottom: 220
    };"""

m = re.search(old_render_dom_rect_pattern, tour_text)
if m:
    tour_text = tour_text[:m.start()] + new_render_dom_rect + tour_text[m.end():]
    print("SUCCESS: Replaced targetRect resolution in tour.js!")
else:
    print("Warning: old_render_dom_rect_pattern not found via regex, checking manual replacement...")

with open(tour_path, 'w', encoding='utf-8') as f:
    f.write(tour_text)

print("Updated js/tour.js!")
