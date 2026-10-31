import sys

with open(r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update .sec-header in CSS
old_css_header = """.sec-header {
      text-align: center;
      margin-bottom: 50px;
    }"""

new_css_header = """.sec-header {
      text-align: center;
      margin-bottom: 50px;
    }

    .overcome-header-box {
      text-align: center;
      margin: 0 auto 52px;
      max-width: 820px;
      padding: 32px 36px;
      background: var(--card-bg);
      border: 1.5px solid var(--border);
      border-radius: 12px;
      box-shadow: var(--card-shadow);
      position: relative;
      will-change: transform, opacity;
      transform-origin: center center;
    }

    body[data-paper='night'] .overcome-header-box {
      background: #182234;
      border-color: rgba(245, 158, 11, 0.25);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45);
    }

    .overcome-tape-top {
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%) rotate(-0.5deg);
      width: 120px;
      height: 24px;
      background: rgba(245, 158, 11, 0.35);
      border: 1px dashed rgba(217, 119, 6, 0.5);
      border-radius: 2px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
      pointer-events: none;
    }"""

assert old_css_header in code, "old_css_header not found in generate_final_home.py"
code = code.replace(old_css_header, new_css_header)

# 2. Update HTML for .sec-header in #use-cases
old_html_sec = """    <!-- Use Cases Journey (Hanging Scrapbook Photo Cards 1 to 5) -->
    <section id="use-cases" class="use-cases-sec">
      <div class="sec-header">
        <span class="sec-tag">Tested Across High-Stakes Scenarios</span>
        <h2 class="sec-title">Engineered to Overcome Human Friction</h2>
        <p class="sec-desc">Real workflows where willpower fails and dynamic A* pathfinding keeps you moving forward.</p>
      </div>"""

new_html_sec = """    <!-- Use Cases Journey (Hanging Scrapbook Photo Cards 1 to 5) -->
    <section id="use-cases" class="use-cases-sec">
      <div class="sec-header overcome-header-box" id="overcomeHeaderBox">
        <div class="overcome-tape-top"></div>
        <span class="sec-tag">Tested Across High-Stakes Scenarios</span>
        <h2 class="sec-title">Engineered to Overcome Human Friction</h2>
        <p class="sec-desc">Real workflows where willpower fails and dynamic A* pathfinding keeps you moving forward.</p>
      </div>"""

assert old_html_sec in code, "old_html_sec not found in generate_final_home.py"
code = code.replace(old_html_sec, new_html_sec)

# 3. Update animateOnScroll in JavaScript
old_js_cards = """      // 5. Use Case Cards: 100% Solid Opacity & Internal Elements Moving on Scroll
      cards.forEach(c => {
        if (!c.el) return;
        const rect = c.el.getBoundingClientRect();
        const dist = rect.top + rect.height / 2 - winH / 2;
        const p = Math.max(0, Math.min(1, 1 - Math.abs(dist) / (winH * 0.85)));

        // Animate tilt and dock-in
        const dynamicTilt = c.baseTilt * p + (1 - p) * (c.baseTilt > 0 ? 3 : -3);
        const scale = 0.96 + 0.04 * p;
        const ty = 20 * (1 - p);

        c.el.style.transform = `translate3d(0, ${ty.toFixed(1)}px, 0) rotate(${dynamicTilt.toFixed(2)}deg) scale(${scale.toFixed(3)})`;
        // Crucial: keep cards 100% solid and readable once in view
        c.el.style.opacity = '1';

        // Internal element movements on scroll:
        const stepNum = c.el.querySelector('.uc-step-num');
        if (stepNum) {
          stepNum.style.transform = `translateX(${Math.max(0, (rect.top - winH * 0.5) * 0.04)}px)`;
        }
        const statPill = c.el.querySelector('.uc-stat-pill');
        if (statPill) {
          statPill.style.transform = `scale(${0.9 + 0.1 * p})`;
        }
        const img = c.el.querySelector('.uc-humaaan-img');
        if (img) {
          img.style.transform = `translate3d(0, ${(1 - p) * 10}px, 0)`;
        }
      });"""

new_js_cards = """      // 4.5. "Engineered to Overcome" Section Header Box: Fade In & Zoom In (from bigger size scale 1.20 to og size 1.0 in og pos)
      const overcomeBox = document.getElementById('overcomeHeaderBox');
      if (overcomeBox) {
        const obRect = overcomeBox.getBoundingClientRect();
        const startY = winH;
        const endY = winH * 0.45;
        const p = Math.max(0, Math.min(1, (startY - obRect.top) / (startY - endY)));

        // Zoom in from bigger size (1.20) down to original size (1.0) in original position
        const scale = 1.20 - 0.20 * p;
        const ty = 32 * (1 - p);
        const opacity = Math.min(1, Math.max(0, p * 1.25));

        overcomeBox.style.transform = `translate3d(0, ${ty.toFixed(1)}px, 0) scale(${scale.toFixed(3)})`;
        overcomeBox.style.opacity = `${opacity.toFixed(2)}`;
      }

      // 5. Use Case Cards: Fade In and Zoom In (from bigger size scale 1.14 to og size 1.0 in og pos)
      cards.forEach(c => {
        if (!c.el) return;
        const rect = c.el.getBoundingClientRect();
        
        // Entrance progress: 0 when entering bottom of viewport, 1.0 when settled
        const enterStart = winH * 1.05;
        const enterEnd = winH * 0.55;
        const enterProgress = Math.max(0, Math.min(1, (enterStart - rect.top) / (enterStart - enterEnd)));

        // Zoom in from bigger size (1.14) down to original size (1.0) in original position
        const zoomScale = 1.14 - 0.14 * enterProgress;
        const ty = 28 * (1 - enterProgress);
        const dynamicTilt = c.baseTilt * enterProgress + (1 - enterProgress) * (c.baseTilt > 0 ? 3 : -3);
        const opacity = Math.min(1, Math.max(0, enterProgress * 1.3));

        c.el.style.transform = `translate3d(0, ${ty.toFixed(1)}px, 0) rotate(${dynamicTilt.toFixed(2)}deg) scale(${zoomScale.toFixed(3)})`;
        c.el.style.opacity = `${opacity.toFixed(2)}`;

        // Internal element movements on scroll:
        const stepNum = c.el.querySelector('.uc-step-num');
        if (stepNum) {
          stepNum.style.transform = `translateX(${Math.max(0, (rect.top - winH * 0.5) * 0.04)}px)`;
        }
        const statPill = c.el.querySelector('.uc-stat-pill');
        if (statPill) {
          statPill.style.transform = `scale(${0.9 + 0.1 * enterProgress})`;
        }
        const img = c.el.querySelector('.uc-humaaan-img');
        if (img) {
          img.style.transform = `translate3d(0, ${(1 - enterProgress) * 10}px, 0)`;
        }
      });"""

assert old_js_cards in code, "old_js_cards not found in generate_final_home.py"
code = code.replace(old_js_cards, new_js_cards)

with open(r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched generate_final_home.py with fade-in and zoom-in for overcome section successfully!")
