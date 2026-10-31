import re

home_path = r'C:\Users\hmmm\goalstar-recall\home.html'

with open(home_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add ink blotch accents to the use-case section header
old_uc_head = r'<div class="uc-header">[\s\S]*?<h2>Real Human Scenarios: Rerouting Around Friction</h2>[\s\S]*?<p class="uc-sub">[\s\S]*?</p>\s*</div>'

new_uc_head = '''<div class="uc-header" style="position: relative;">
        <!-- Organic Ink Blotch & Splatters Background Accent -->
        <svg class="ink-blotch-bg" viewBox="0 0 500 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M 50 60 C 80 20, 160 30, 240 25 C 320 20, 420 15, 460 55 C 480 75, 450 100, 380 105 C 300 110, 180 105, 110 100 C 60 95, 30 85, 50 60 Z" fill="#2a2d3e" opacity="0.04" />
          <!-- Ink Droplet Splatters -->
          <circle cx="475" cy="40" r="4" fill="#2a2d3e" opacity="0.25" />
          <circle cx="485" cy="52" r="2.5" fill="#2a2d3e" opacity="0.18" />
          <circle cx="465" cy="28" r="1.8" fill="#2a2d3e" opacity="0.2" />
          <circle cx="35" cy="75" r="3.2" fill="#2a2d3e" opacity="0.2" />
          <circle cx="25" cy="85" r="2" fill="#2a2d3e" opacity="0.15" />
        </svg>

        <div class="ink-stamp-badge">
          <img src="assets/ink/Droplet.svg" alt="Ink Droplet" width="16" height="16" class="ink-icon-stamp" />
          <span>REAL-LIFE SCENARIOS // WALRUS PORTABLE MEMORY</span>
        </div>
        <h2>Real Human Scenarios: Rerouting Around Friction</h2>
        <p class="uc-sub">
          Scroll down as the A* path dynamically adapts across five distinct real-world hurdles.
        </p>
      </div>'''

content = re.sub(old_uc_head, new_uc_head, content)

# Add Thinker toggle and ink seal inside sculpture card
old_tagline = r'<div class="sculpture-tagline">"The mind reroutes where friction permits\."</div>\s*</div>'

new_tagline = '''<div class="sculpture-tagline">"The mind reroutes where friction permits."</div>
          
          <!-- Mode Switch: Papercut Silhouette <-> Thinker Statue -->
          <div class="sculpture-switch-row">
            <button id="toggleThinkerBtn" class="mini-ink-btn" title="Toggle between Anatomical Papercut and Classical Thinker Statue">
              <span id="thinkerBtnIcon">🗿</span> <span id="thinkerBtnTxt">Show Thinker Statue</span>
            </button>
            <span class="ink-seal-label">INK BLOT NO. 42</span>
          </div>

          <!-- Optional Classical Thinker Overlay -->
          <div id="thinkerOverlay" class="thinker-overlay" hidden>
            <img src="assets/ink/thinker.png" alt="The Thinker" class="thinker-statue-img" width="180" height="250" loading="lazy" />
            <div class="thinker-quote">Contemplative intelligence.</div>
          </div>
        </div>'''

content = re.sub(old_tagline, new_tagline, content)

# Add CSS for ink stamp badge, ink-blotch-bg, and thinker overlay
style_addition = '''
    /* Ink Blotch & Stamp Accents */
    .ink-blotch-bg {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 100%;
      max-width: 650px;
      height: 120px;
      pointer-events: none;
      z-index: 0;
    }
    .ink-stamp-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(42, 45, 62, 0.06);
      border: 1px solid rgba(42, 45, 62, 0.2);
      border-radius: 4px;
      padding: 3px 10px;
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.8px;
      color: var(--ink-soft);
      margin-bottom: 8px;
    }
    body[data-paper='night'] .ink-stamp-badge {
      background: rgba(245, 158, 11, 0.1);
      border-color: rgba(245, 158, 11, 0.3);
      color: #f59e0b;
    }
    .ink-icon-stamp {
      filter: drop-shadow(1px 1px 0 rgba(0,0,0,0.2));
    }
    body[data-paper='night'] .ink-icon-stamp {
      filter: invert(1) brightness(1.5);
    }
    .sculpture-switch-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px dashed var(--line);
    }
    .mini-ink-btn {
      background: var(--paper-warm);
      border: 1.5px solid var(--ink);
      border-radius: 4px;
      padding: 4px 10px;
      font-family: 'Patrick Hand', cursive;
      font-size: 14px;
      font-weight: bold;
      color: var(--ink);
      cursor: pointer;
      box-shadow: 2px 2px 0 var(--ink);
      transition: all 0.15s ease;
    }
    .mini-ink-btn:hover {
      transform: translateY(-1px);
      box-shadow: 3px 3px 0 var(--ink);
      background: #fef3c7;
    }
    .mini-ink-btn:active {
      transform: translateY(1px);
      box-shadow: 1px 1px 0 var(--ink);
    }
    body[data-paper='night'] .mini-ink-btn {
      background: rgba(30, 41, 59, 0.9);
      color: #f8fafc;
      border-color: #f59e0b;
      box-shadow: 2px 2px 0 #f59e0b;
    }
    .ink-seal-label {
      font-family: 'Space Grotesk', monospace;
      font-size: 10px;
      font-weight: 800;
      color: var(--ink-soft);
      letter-spacing: 1px;
    }
    .thinker-overlay {
      position: absolute;
      top: 45px;
      left: 20px;
      right: 20px;
      bottom: 45px;
      background: var(--panel);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      z-index: 10;
      animation: fadeIn 0.25s ease;
    }
    .thinker-statue-img {
      max-height: 200px;
      width: auto;
      object-fit: contain;
      filter: drop-shadow(0 8px 16px rgba(0,0,0,0.25));
    }
    .thinker-quote {
      font-family: 'Caveat', cursive;
      font-size: 16px;
      color: var(--ink);
      margin-top: 6px;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.96); }
      to { opacity: 1; transform: scale(1); }
    }
  </style>'''

content = content.replace('</style>', style_addition)

# Add JS handler for thinker toggle in home.html
js_addition = '''
    // Thinker Statue Toggle
    const toggleThinkerBtn = document.getElementById('toggleThinkerBtn');
    const thinkerOverlay = document.getElementById('thinkerOverlay');
    const sculptureSvgWrap = document.querySelector('.sculpture-svg-wrap');
    let showingThinker = false;

    if (toggleThinkerBtn && thinkerOverlay) {
      toggleThinkerBtn.addEventListener('click', () => {
        showingThinker = !showingThinker;
        if (showingThinker) {
          thinkerOverlay.hidden = false;
          sculptureSvgWrap.style.opacity = '0.15';
          document.getElementById('thinkerBtnIcon').textContent = '👤';
          document.getElementById('thinkerBtnTxt').textContent = 'Show Papercut Mind';
        } else {
          thinkerOverlay.hidden = true;
          sculptureSvgWrap.style.opacity = '1';
          document.getElementById('thinkerBtnIcon').textContent = '🗿';
          document.getElementById('thinkerBtnTxt').textContent = 'Show Thinker Statue';
        }
        if (window.sound) window.sound.play('click');
      });
    }
  </script>'''

content = content.replace('</script>\n</body>', js_addition + '\n</body>')

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Added ink blotch accents, Thinker statue toggle, and droplet stamp!')
