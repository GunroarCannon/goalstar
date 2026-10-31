import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

gen_path = r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py'
with open(gen_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update .traveling-arrow CSS
css_pattern = r'(\.traveling-arrow\s*\{[^}]*\})'
m = re.search(css_pattern, text)
if m:
    print("Found traveling-arrow CSS block")
    new_arrow_css = """.traveling-arrow {
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
      border-radius: 9px;
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
    text = text[:m.start()] + new_arrow_css + text[m.end():]
else:
    print("Warning: traveling-arrow CSS block not found")

# 2. Update ink svg
ink_pattern = r'<svg class="ink-swash-svg" id="inkSwashSvg"[^>]*>[\s\S]*?</svg>'
m_ink = re.search(ink_pattern, text)
if m_ink:
    print("Found ink-swash-svg HTML block")
    new_ink_svg = """<svg class="ink-swash-svg" id="inkSwashSvg" viewBox="0 0 340 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
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
    text = text[:m_ink.start()] + new_ink_svg + text[m_ink.end():]
else:
    print("Warning: ink-swash-svg HTML block not found")

# 3. Add Destination Terminal underneath Card 5
card5_pattern = r'(<button class="album-btn primary-tape launch-btn" id="card5LaunchBtn">Launch GoalStar Now</button>\s*</div>\s*</div>\s*</article>\s*</div>)'
m_card5 = re.search(card5_pattern, text)
if m_card5:
    print("Found Card 5 footer block")
    terminal_html = """</div>

        <!-- Centered Destination Terminal (Middle X Position Underneath Last Card) -->
        <div class="journey-terminal" id="journeyTerminal">
          <div class="terminal-circle-target" id="terminalCircleTarget">
            <div class="terminal-core-circle"></div>
          </div>
          <span class="terminal-badge">Goal Reached · Mainnet Verified</span>
          <p class="terminal-sub">Dynamic A* Path Concluded</p>
        </div>"""
    # Replace closing </div> of uc-grid with closing + terminal
    text = text[:m_card5.end()] + terminal_html + text[m_card5.end()+6:]
else:
    print("Warning: Card 5 footer block not found")

# 4. Add theme selector to landing-nav in home.html
nav_pattern = r'(<a href="javascript:void\(0\)" id="navLaunchApp">Open App</a>\s*</nav>)'
m_nav = re.search(nav_pattern, text)
if m_nav:
    print("Found landing-nav block")
    new_nav = """<a href="javascript:void(0)" id="navLaunchApp">Open App</a>
      <select id="themeSelect" class="theme-select engraved-select" style="margin-left:8px;" title="Choose Theme Aesthetic">
        <option value="notebook">Notebook</option>
        <option value="night">Chalkboard</option>
        <option value="blueprint">Blueprint</option>
        <option value="monograph">Monograph</option>
      </select>
    </nav>"""
    text = text[:m_nav.start()] + new_nav + text[m_nav.end():]

# 5. Update buildConnectorPath
build_pattern = r'function buildConnectorPath\(\)\s*\{[\s\S]*?totalPathLength = svgPath\.getTotalLength\(\);\s*\}'
m_build = re.search(build_pattern, text)
if m_build:
    print("Found buildConnectorPath function")
    new_build = """function buildConnectorPath() {
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
    text = text[:m_build.start()] + new_build + text[m_build.end():]

# 6. Update animateOnScroll for ink underline
ink_anim_pattern = r'if \(inkSwashSvg\) \{[\s\S]*?inkSwashSvg\.style\.transform = `scaleX\(\$\{swashProgress\}\)`;\s*\}'
m_ink_anim = re.search(ink_anim_pattern, text)
if m_ink_anim:
    print("Found ink animation block in animateOnScroll")
    new_ink_anim = """if (inkSwashSvg) {
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
    text = text[:m_ink_anim.start()] + new_ink_anim + text[m_ink_anim.end():]

# 7. Update arrow logic in animateOnScroll
arrow_anim_pattern = r'const pt = svgPath\.getPointAtLength\(currentLen\);[\s\S]*?targetRing\.style\.opacity = progress >= 0\.95 \? \'1\' : \'0\';\s*\}'
m_arrow_anim = re.search(arrow_anim_pattern, text)
if m_arrow_anim:
    print("Found arrow animation loop in animateOnScroll")
    new_arrow_anim = """const pt = svgPath.getPointAtLength(currentLen);
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
    text = text[:m_arrow_anim.start()] + new_arrow_anim + text[m_arrow_anim.end():]

with open(gen_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: generate_final_home.py patched successfully!")
