import sys

with open(r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS in generate_final_home.py
old_css_arrow = """    .traveling-arrow {
      position: absolute;
      width: 26px;
      height: 26px;
      z-index: 20;
      pointer-events: none;
      transform: translate(-50%, -50%);
      filter: drop-shadow(0 2px 5px rgba(5, 150, 105, 0.5));
      transition: none; /* strictly direct frame-by-frame synchronization */
    }"""

new_css_arrow = """    .traveling-arrow {
      position: absolute;
      width: 26px;
      height: 26px;
      z-index: 20;
      pointer-events: none;
      transform: translate(-50%, -50%);
      filter: drop-shadow(0 2px 5px rgba(5, 150, 105, 0.5));
      display: flex;
      align-items: center;
      justify-content: center;
      transition: border-radius 0.25s ease, background 0.25s ease, box-shadow 0.25s ease;
    }

    .traveling-arrow.is-circle {
      border-radius: 50% !important;
      background: #059669 !important;
      box-shadow: 0 0 20px rgba(5, 150, 105, 0.9), 0 0 0 5px rgba(5, 150, 105, 0.25);
    }

    .traveling-arrow.is-circle svg {
      opacity: 0 !important;
      display: none !important;
    }

    /* Bottom Terminal Destination (Middle X Position Underneath Card 5) */
    .journey-terminal {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin: 48px auto 24px;
      text-align: center;
      position: relative;
      z-index: 10;
    }

    .terminal-circle-target {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      border: 2.5px solid #059669;
      background: rgba(5, 150, 105, 0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.4s ease, background 0.4s ease;
      box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.4);
    }

    .terminal-circle-target.arrived {
      transform: scale(1.18);
      background: #059669;
      box-shadow: 0 0 24px rgba(5, 150, 105, 0.6), 0 0 0 8px rgba(5, 150, 105, 0.18);
    }

    .terminal-core-circle {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #059669;
      transition: all 0.3s ease;
    }

    .terminal-circle-target.arrived .terminal-core-circle {
      background: #ffffff;
      transform: scale(0.8);
    }

    .terminal-badge {
      font-family: 'Space Grotesk', monospace;
      font-size: 13px;
      font-weight: 800;
      color: var(--accent);
      letter-spacing: 0.8px;
      text-transform: uppercase;
      margin-top: 14px;
      padding: 4px 12px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 99px;
      box-shadow: 0 2px 6px var(--card-shadow);
    }

    .terminal-sub {
      font-size: 12px;
      color: var(--ink-soft);
      margin: 4px 0 0;
    }

    /* Ink Underline Calligraphy & Bleed */
    .ink-droplet {
      transform-origin: center center;
      transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    }"""

assert old_css_arrow in text, "old_css_arrow not found in generate_final_home.py"
text = text.replace(old_css_arrow, new_css_arrow)

# 2. Update Hero ink underline in HTML
old_ink_html = """            <svg class="ink-swash-svg" id="inkSwashSvg" viewBox="0 0 310 28" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M 6 18 C 35 15, 75 22, 120 21 C 170 20, 220 12, 268 9 C 274 8.5, 278 11, 274 13 C 240 21, 190 25, 135 25 C 80 25, 30 22, 6 18 Z" fill="#d97706" />
              <path d="M 18 19 C 70 23, 140 24, 210 18 C 245 15, 270 11, 277 9" stroke="#b45309" stroke-width="2.5" stroke-linecap="round" />
            </svg>"""

new_ink_html = """            <svg class="ink-swash-svg" id="inkSwashSvg" viewBox="0 0 340 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <defs>
                <filter id="inkBleedFilter" x="-15%" y="-15%" width="130%" height="130%">
                  <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise" />
                  <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.5" xChannelSelector="R" yChannelSelector="G" />
                </filter>
              </defs>
              <path id="heroInkCalligraphyPath" filter="url(#inkBleedFilter)"
                d="M 8 20 C 45 16, 95 24, 150 22 C 210 20, 265 14, 320 10 C 330 9, 335 12, 330 15 C 290 23, 220 27, 160 27 C 100 27, 40 24, 8 20 Z" fill="#d97706" />
              <path id="heroInkStrokePath" filter="url(#inkBleedFilter)"
                d="M 12 18 C 65 24, 145 25, 230 18 C 275 14, 310 11, 328 10"
                stroke="#b45309" stroke-width="3" stroke-linecap="round" fill="none" />
              <circle class="ink-droplet" id="inkDrop1" cx="332" cy="12" r="3.2" fill="#d97706" />
              <circle class="ink-droplet" id="inkDrop2" cx="324" cy="24" r="2.2" fill="#b45309" />
              <circle class="ink-droplet" id="inkDrop3" cx="16" cy="26" r="2.5" fill="#d97706" />
            </svg>"""

assert old_ink_html in text, "old_ink_html not found in generate_final_home.py"
text = text.replace(old_ink_html, new_ink_html)

# 3. Add Destination Terminal underneath Card 5
old_card5_end = """            <div class="uc-card-footer">
              <span class="uc-stat-pill">100% Finish Rate · Injury Prevented</span>
              <div class="card5-target-wrap">
                <div class="card5-target-ring" id="card5TargetRing"></div>
                <button class="album-btn primary-tape launch-btn" id="card5LaunchBtn">Launch GoalStar Now</button>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>"""

new_card5_end = """            <div class="uc-card-footer">
              <span class="uc-stat-pill">100% Finish Rate · Injury Prevented</span>
              <div class="card5-target-wrap">
                <div class="card5-target-ring" id="card5TargetRing"></div>
                <button class="album-btn primary-tape launch-btn" id="card5LaunchBtn">Launch GoalStar Now</button>
              </div>
            </div>
          </article>
        </div>

        <!-- Centered Destination Terminal (Middle X Position Underneath Last Card) -->
        <div class="journey-terminal" id="journeyTerminal">
          <div class="terminal-circle-target" id="terminalCircleTarget">
            <div class="terminal-core-circle"></div>
          </div>
          <span class="terminal-badge">Goal Reached · Mainnet Verified</span>
          <p class="terminal-sub">Dynamic A* Path Concluded</p>
        </div>
      </div>
    </section>"""

assert old_card5_end in text, "old_card5_end not found in generate_final_home.py"
text = text.replace(old_card5_end, new_card5_end)

# 4. Add theme selector to landing-nav in home.html
old_landing_nav = """      <a href="#simulator">A* Simulator</a>
      <a href="#use-cases">Use Cases</a>
      <a href="javascript:void(0)" id="navTourBtn">Walkthrough</a>
      <a href="javascript:void(0)" id="navLaunchApp">Open App</a>
    </nav>"""

new_landing_nav = """      <a href="#simulator">A* Simulator</a>
      <a href="#use-cases">Use Cases</a>
      <a href="javascript:void(0)" id="navTourBtn">Walkthrough</a>
      <a href="javascript:void(0)" id="navLaunchApp">Open App</a>
      <select id="themeSelect" class="theme-select engraved-select" style="margin-left:8px;" title="Choose Theme Aesthetic">
        <option value="notebook">Notebook</option>
        <option value="night">Chalkboard</option>
        <option value="blueprint">Blueprint</option>
        <option value="monograph">Monograph</option>
      </select>
    </nav>"""

assert old_landing_nav in text, "old_landing_nav not found in generate_final_home.py"
text = text.replace(old_landing_nav, new_landing_nav)

# 5. Update buildConnectorPath & animateOnScroll
old_build_func = """    function buildConnectorPath() {
      const track = document.getElementById('journeyTrack');
      if (!track || !svgPath || bays.length < 2 || window.innerWidth < 640) return;
      const tr = track.getBoundingClientRect();
      const svg = document.getElementById('journeySvgTrack');
      if (!svg) return;

      // Set SVG viewBox and dimensions matching track exactly 1:1
      svg.setAttribute('viewBox', `0 0 ${tr.width} ${tr.height}`);
      svg.setAttribute('width', `${tr.width}`);
      svg.setAttribute('height', `${tr.height}`);

      const c1 = document.getElementById('card1').getBoundingClientRect();
      const c2 = document.getElementById('card2').getBoundingClientRect();
      const c3 = document.getElementById('card3').getBoundingClientRect();
      const c4 = document.getElementById('card4').getBoundingClientRect();
      const c5 = document.getElementById('card5').getBoundingClientRect();
      const endBtn = document.getElementById('card5LaunchBtn') || document.getElementById('card5');
      const er = endBtn.getBoundingClientRect();

      // Precision anchor points on each card
      const p1 = { x: c1.left - tr.left + 50, y: c1.top - tr.top + 30 };
      const p2 = { x: c2.right - tr.left - 50, y: c2.top - tr.top + 30 };
      const p3 = { x: c3.left - tr.left + 50, y: c3.top - tr.top + 30 };
      const p4 = { x: c4.right - tr.left - 50, y: c4.top - tr.top + 30 };
      // End point terminates EXACTLY on card 5 launch button
      const pEnd = { x: er.left - tr.left + er.width / 2, y: er.top - tr.top + er.height / 2 };

      const d = `M ${p1.x} ${p1.y} ` +
                `C ${p1.x + 80} ${(p1.y + p2.y) / 2}, ${p2.x - 80} ${(p1.y + p2.y) / 2}, ${p2.x} ${p2.y} ` +
                `C ${p2.x - 80} ${(p2.y + p3.y) / 2}, ${p3.x + 80} ${(p2.y + p3.y) / 2}, ${p3.x} ${p3.y} ` +
                `C ${p3.x + 80} ${(p3.y + p4.y) / 2}, ${p4.x - 80} ${(p3.y + p4.y) / 2}, ${p4.x} ${p4.y} ` +
                `C ${p4.x - 80} ${(p4.y + pEnd.y) / 2}, ${pEnd.x} ${(p4.y + pEnd.y) / 2 - 20}, ${pEnd.x} ${pEnd.y}`;

      svgPath.setAttribute('d', d);
      if (activePath) activePath.setAttribute('d', d);
      totalPathLength = svgPath.getTotalLength();
    }"""

new_build_func = """    function buildConnectorPath() {
      const track = document.getElementById('journeyTrack');
      if (!track || !svgPath || bays.length < 2 || window.innerWidth < 640) return;
      const tr = track.getBoundingClientRect();
      const svg = document.getElementById('journeySvgTrack');
      if (!svg) return;

      // Set SVG viewBox and dimensions matching track exactly 1:1
      svg.setAttribute('viewBox', `0 0 ${tr.width} ${tr.height}`);
      svg.setAttribute('width', `${tr.width}`);
      svg.setAttribute('height', `${tr.height}`);

      const c1 = document.getElementById('card1').getBoundingClientRect();
      const c2 = document.getElementById('card2').getBoundingClientRect();
      const c3 = document.getElementById('card3').getBoundingClientRect();
      const c4 = document.getElementById('card4').getBoundingClientRect();
      const c5 = document.getElementById('card5').getBoundingClientRect();
      
      const termEl = document.getElementById('terminalCircleTarget');
      const ter = termEl ? termEl.getBoundingClientRect() : { left: tr.left + tr.width/2 - 24, top: tr.top + tr.height - 60, width: 48, height: 48 };

      // Anchor points on cards
      const p1 = { x: c1.left - tr.left + 50, y: c1.top - tr.top + 30 };
      const p2 = { x: c2.right - tr.left - 50, y: c2.top - tr.top + 30 };
      const p3 = { x: c3.left - tr.left + 50, y: c3.top - tr.top + 30 };
      const p4 = { x: c4.right - tr.left - 50, y: c4.top - tr.top + 30 };
      const p5 = { x: c5.right - tr.left - 80, y: c5.top - tr.top + 40 };

      // EXACT TERMINATION: Middle X position of the page, underneath last card
      const pEnd = { x: tr.width / 2, y: ter.top - tr.top + ter.height / 2 };

      const d = `M ${p1.x} ${p1.y} ` +
                `C ${p1.x + 80} ${(p1.y + p2.y) / 2}, ${p2.x - 80} ${(p1.y + p2.y) / 2}, ${p2.x} ${p2.y} ` +
                `C ${p2.x - 80} ${(p2.y + p3.y) / 2}, ${p3.x + 80} ${(p2.y + p3.y) / 2}, ${p3.x} ${p3.y} ` +
                `C ${p3.x + 80} ${(p3.y + p4.y) / 2}, ${p4.x - 80} ${(p3.y + p4.y) / 2}, ${p4.x} ${p4.y} ` +
                `C ${p4.x - 80} ${(p4.y + p5.y) / 2}, ${p5.x + 80} ${(p4.y + p5.y) / 2}, ${p5.x} ${p5.y} ` +
                `C ${p5.x + 60} ${p5.y + 70}, ${pEnd.x} ${(p5.y + pEnd.y) / 2}, ${pEnd.x} ${pEnd.y}`;

      svgPath.setAttribute('d', d);
      if (activePath) activePath.setAttribute('d', d);
      totalPathLength = svgPath.getTotalLength();
    }"""

assert old_build_func in text, "old_build_func not found in generate_final_home.py"
text = text.replace(old_build_func, new_build_func)

# 6. Update animateOnScroll in JavaScript for ink underline & arrow turning to circle
old_scroll_anim = """      if (inkSwashSvg) {
        // Smoothly draw in ink line as page scrolls
        const swashProgress = Math.min(1, Math.max(0.2, (scrollY + 200) / 320));
        inkSwashSvg.style.transform = `scaleX(${swashProgress})`;
      }"""

new_scroll_anim = """      if (inkSwashSvg) {
        // Organic calligraphy ink flow and stroke dash drawing
        const inkProgress = Math.min(1, Math.max(0.05, (scrollY + 220) / 360));
        const strokePath = document.getElementById('heroInkStrokePath');
        if (strokePath) {
          const len = strokePath.getTotalLength() || 320;
          strokePath.style.strokeDasharray = `${len}`;
          strokePath.style.strokeDashoffset = `${len * (1 - inkProgress)}`;
        }
        const calligPath = document.getElementById('heroInkCalligraphyPath');
        if (calligPath) {
          calligPath.style.clipPath = `inset(0 ${(1 - inkProgress) * 100}% 0 0)`;
        }
        const drop1 = document.getElementById('inkDrop1');
        const drop2 = document.getElementById('inkDrop2');
        if (drop1) drop1.style.transform = `scale(${Math.max(0, (inkProgress - 0.65) / 0.35)})`;
        if (drop2) drop2.style.transform = `scale(${Math.max(0, (inkProgress - 0.8) / 0.2)})`;
      }"""

assert old_scroll_anim in text, "old_scroll_anim not found in generate_final_home.py"
text = text.replace(old_scroll_anim, new_scroll_anim)

# 7. Update arrow logic in animateOnScroll
old_arrow_loop = """          const pt = svgPath.getPointAtLength(currentLen);
          travelingArrow.style.left = `${pt.x}px`;
          travelingArrow.style.top = `${pt.y}px`;

          // Tangent alignment
          if (progress >= 0.98) {
            travelingArrow.style.transform = `translate(-50%, -50%) rotate(180deg)`;
          } else {
            const pBefore = svgPath.getPointAtLength(Math.max(0, currentLen - 2));
            const pAfter = svgPath.getPointAtLength(Math.min(pathLen, currentLen + 2));
            const angle = Math.atan2(pAfter.y - pBefore.y, pAfter.x - pBefore.x) * (180 / Math.PI);
            travelingArrow.style.transform = `translate(-50%, -50%) rotate(${angle + 90}deg)`;
          }

          // Highlight target arrival ring at Card 5
          const targetRing = document.getElementById('card5TargetRing');
          if (targetRing) {
            targetRing.style.opacity = progress >= 0.95 ? '1' : '0';
          }"""

new_arrow_loop = """          const pt = svgPath.getPointAtLength(currentLen);
          travelingArrow.style.left = `${pt.x}px`;
          travelingArrow.style.top = `${pt.y}px`;

          const terminalTarget = document.getElementById('terminalCircleTarget');

          // TURN INTO A CIRCLE IN THE MIDDLE X POSITION AT THE BOTTOM
          if (progress >= 0.94) {
            travelingArrow.classList.add('is-circle');
            travelingArrow.style.transform = `translate(-50%, -50%) scale(1.15)`;
            if (terminalTarget) terminalTarget.classList.add('arrived');
          } else {
            travelingArrow.classList.remove('is-circle');
            if (terminalTarget) terminalTarget.classList.remove('arrived');
            const pBefore = svgPath.getPointAtLength(Math.max(0, currentLen - 2));
            const pAfter = svgPath.getPointAtLength(Math.min(pathLen, currentLen + 2));
            const angle = Math.atan2(pAfter.y - pBefore.y, pAfter.x - pBefore.x) * (180 / Math.PI);
            travelingArrow.style.transform = `translate(-50%, -50%) rotate(${angle + 90}deg)`;
          }

          const targetRing = document.getElementById('card5TargetRing');
          if (targetRing) {
            targetRing.style.opacity = progress >= 0.85 ? '1' : '0';
          }"""

assert old_arrow_loop in text, "old_arrow_loop not found in generate_final_home.py"
text = text.replace(old_arrow_loop, new_arrow_loop)

with open(r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated generate_final_home.py with arrow turning into center circle and authentic ink calligraphy!")
