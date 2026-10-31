import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

tour_file = r'C:\Users\hmmm\goalstar-recall\js\tour.js'
with open(tour_file, 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'this\.steps\s*=\s*\[[\s\S]*?\];\s*this\.handleResize'

new_steps = """this.steps = [
      {
        id: 'goal',
        targetSelector: '#boardPick',
        fallbackSelector: '#newGoalBtn',
        title: 'Step 1: Your Active Goal',
        text: 'Select an active goal or create a new one to view your path.',
        cardPos: (targetRect, cardW, cardH) => ({
          left: Math.max(20, Math.min(window.innerWidth - cardW - 20, targetRect.left - 10)),
          top: targetRect.bottom + 16
        }),
        arrows: (targetRect, cardPos, cardW, cardH) => [
          {
            from: { x: cardPos.left + 80, y: cardPos.top },
            to: { x: targetRect.left + targetRect.width / 2, y: targetRect.bottom + 2 },
            ctrl: { x: cardPos.left + 80, y: (cardPos.top + targetRect.bottom) / 2 }
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
        title: 'Step 2: Lowest-Friction Path',
        text: 'The glowing green trail is your optimal A* route. Click any node to see tasks.',
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
        title: 'Step 3: 4-D Friction Sliders',
        text: 'Adjust Time, Money, Effort, or Risk to instantly reroute around obstacles.',
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
        title: 'Step 4: 48h Watchdog',
        text: 'Stuck milestones automatically break down into 15-minute micro-actions.',
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
        title: 'Step 5: Sui Blockchain Stamp',
        text: 'Stamp completed milestones on Sui Mainnet for permanent verification.',
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

    this.handleResize"""

m = re.search(pattern, text)
if m:
    text = text[:m.start()] + new_steps + text[m.end():]
    with open(tour_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Updated js/tour.js steps!")
else:
    print("ERROR: pattern not found in js/tour.js")
    sys.exit(1)
