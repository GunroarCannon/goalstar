import re

home_path = r'C:\Users\hmmm\goalstar-recall\home.html'

with open(home_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Background Humaaans Layer (Bigger, animated on scroll)
bg_humaaans_html = '''  <!-- Background Parallax Humaaans Layer (Animated on Scroll) -->
  <div class="bg-humaaans-layer" id="bgHumaaansLayer" aria-hidden="true">
    <div class="bg-humaaan-item" id="bgHumaaan1" style="top: 140px; right: 2%;">
      <img src="assets/humaaans/webp/hu_sit_8.webp" alt="" class="bg-humaaan-img" />
    </div>
    <div class="bg-humaaan-item" id="bgHumaaan2" style="top: 900px; left: 1%;">
      <img src="assets/humaaans/webp/hu_stand_10.webp" alt="" class="bg-humaaan-img" />
    </div>
    <div class="bg-humaaan-item" id="bgHumaaan3" style="top: 1700px; right: 1%;">
      <img src="assets/humaaans/webp/hu_sit_3.webp" alt="" class="bg-humaaan-img" />
    </div>
    <div class="bg-humaaan-item" id="bgHumaaan4" style="top: 2500px; left: 2%;">
      <img src="assets/humaaans/webp/hu_stand_4.webp" alt="" class="bg-humaaan-img" />
    </div>
    <div class="bg-humaaan-item" id="bgHumaaan5" style="top: 3200px; right: 2%;">
      <img src="assets/humaaans/webp/hu_stand_14.webp" alt="" class="bg-humaaan-img" />
    </div>
  </div>
'''

if 'bg-humaaans-layer' not in content:
    content = content.replace('<body class="landing-body">', '<body class="landing-body">\n' + bg_humaaans_html)

# 2. Replace Hero Section: Remove that face completely! Replace with clean Hanging Photo Album Card!
# Also remove the cluttered hero-humaaan-badge
old_hero_pattern = r'<section class="hero-sec">[\s\S]*?</section>\s*<!-- Live Route Simulator'

new_hero_html = '''<section class="hero-sec">
      <div class="hero-left">
        <div class="hero-badge">🧠 WALRUS MAINNET MEMORY · TATUM SUI RPC</div>
        <h1 class="hero-title">
          A* Pathfinding for Life Goals, Backed by 
          <span class="ink-hl-wrap">
            <span class="ink-hl-text">Portable Memory</span>
            <svg class="ink-swash-svg" viewBox="0 0 310 28" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M 6 18 C 35 15, 75 22, 120 21 C 170 20, 220 12, 268 9 C 274 8.5, 278 11, 274 13 C 240 21, 190 25, 135 25 C 80 25, 30 22, 6 18 Z" fill="#d97706" />
              <path d="M 18 19 C 70 23, 140 24, 210 18 C 245 15, 270 11, 277 9" stroke="#b45309" stroke-width="2.5" stroke-linecap="round" opacity="0.6" />
              <circle cx="284" cy="6" r="2.2" fill="#d97706" opacity="0.8" />
              <circle cx="290" cy="12" r="1.5" fill="#d97706" opacity="0.6" />
              <circle cx="276" cy="4" r="1.1" fill="#d97706" opacity="0.5" />
              <circle cx="3" cy="19" r="1.5" fill="#d97706" opacity="0.5" />
            </svg>
          </span>
        </h1>
        <p class="hero-desc">
          Goals fail when friction builds up. GoalStar calculates your lowest-cost path forward, learns your real-world stamina, and reroutes around roadblocks.
        </p>

        <div class="hero-cta-row">
          <button id="heroLaunchBtn" class="album-btn primary-tape" style="font-size: 18px !important; padding: 12px 28px !important;">🚀 Open Interactive Planner</button>
          <a href="#simulator" class="album-btn secondary-tape" style="font-size: 15px; text-decoration: none;">⚡ Try A* In Browser</a>
        </div>
      </div>

      <div class="hero-right">
        <!-- Photo Album Hanging Photo (No Face! Clean Humaaan & Constellation) -->
        <div class="hanging-photo-card" id="heroPhoto">
          <!-- Twine Clothesline & Wooden Clothespin -->
          <div class="photo-pin-top">
            <svg class="clothespin-svg" width="32" height="42" viewBox="0 0 32 42" fill="none">
              <!-- Twine line across top -->
              <line x1="-50" y1="8" x2="80" y2="8" stroke="#8b5e3c" stroke-width="2.5" stroke-dasharray="2 2" />
              <!-- Wooden Clip Body -->
              <rect x="11" y="2" width="10" height="30" rx="3" fill="#d4a373" stroke="#2a2d3e" stroke-width="1.8" />
              <rect x="13" y="14" width="6" height="6" rx="1.5" fill="#9c6644" />
              <line x1="16" y1="2" x2="16" y2="12" stroke="#2a2d3e" stroke-width="1.2" />
              <line x1="16" y1="22" x2="16" y2="32" stroke="#2a2d3e" stroke-width="1.2" />
            </svg>
          </div>

          <!-- Polaroid Photo Image Frame -->
          <div class="polaroid-frame">
            <div class="polaroid-inner-art">
              <img src="assets/humaaans/webp/hu_stand_24.webp" alt="Life Goal Dreamer" class="polaroid-humaaan-hero" loading="lazy">
              <!-- Glowing A* Graph Constellation -->
              <svg class="photo-constellation-svg" viewBox="0 0 240 180" aria-hidden="true">
                <line x1="40" y1="130" x2="110" y2="70" stroke="#10b981" stroke-width="2.5" stroke-dasharray="3 3" />
                <line x1="110" y1="70" x2="185" y2="40" stroke="#10b981" stroke-width="3" />
                <circle cx="40" cy="130" r="7" fill="#10b981" stroke="#2a2d3e" stroke-width="2" />
                <circle cx="110" cy="70" r="8" fill="#10b981" stroke="#2a2d3e" stroke-width="2" />
                <polygon points="185,26 190,38 203,39 193,48 196,61 185,54 174,61 177,48 167,39 180,38" fill="#f59e0b" stroke="#2a2d3e" stroke-width="2" />
              </svg>
            </div>
            <!-- Polaroid Handwritten Chin -->
            <div class="polaroid-chin">
              <span class="polaroid-handwriting">"The shortest path between where you are and where you want to be."</span>
              <span class="polaroid-date">OCT 2026 // SUI &amp; WALRUS</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Live Route Simulator'''

content = re.sub(old_hero_pattern, new_hero_html, content)

# 3. Add Photo Album Styles (Replace heavy 3D buttons & panels with photo album / hanging photo styles)
photo_album_css = '''
    /* ========================================================
       PHOTO ALBUM & HANGING PHOTOS AESTHETIC (FRONTEND-DESIGN)
       ======================================================== */

    /* Background Parallax Humaaans */
    .bg-humaaans-layer {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      pointer-events: none;
      z-index: 0;
    }
    .bg-humaaan-item {
      position: absolute;
      will-change: transform, opacity;
      transition: transform 0.1s linear, opacity 0.2s ease;
      opacity: 0.25;
      filter: grayscale(15%) drop-shadow(0 15px 25px rgba(0,0,0,0.06));
    }
    body[data-paper='night'] .bg-humaaan-item {
      opacity: 0.16;
      filter: brightness(0.85) drop-shadow(0 15px 30px rgba(0,0,0,0.4));
    }
    .bg-humaaan-img {
      height: 380px;
      width: auto;
      object-fit: contain;
    }
    @media (max-width: 1000px) {
      .bg-humaaan-item { display: none; }
    }

    /* Hanging Polaroid Photo Card (Hero) */
    .hanging-photo-card {
      position: relative;
      background: #ffffff;
      border: 1px solid rgba(42, 45, 62, 0.15);
      border-radius: 4px;
      padding: 14px 14px 20px;
      box-shadow: 
        0 14px 28px rgba(0, 0, 0, 0.12),
        0 3px 8px rgba(0, 0, 0, 0.06),
        0 0 1px rgba(0, 0, 0, 0.1);
      transform: rotate(-1.5deg);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      max-width: 360px;
      margin: 20px auto 0;
      z-index: 2;
    }
    .hanging-photo-card:hover {
      transform: rotate(0deg) translateY(-4px) scale(1.02);
      box-shadow: 0 20px 38px rgba(0, 0, 0, 0.16), 0 5px 12px rgba(0, 0, 0, 0.08);
    }
    body[data-paper='night'] .hanging-photo-card {
      background: #1e293b;
      border-color: rgba(245, 158, 11, 0.3);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6);
    }

    .photo-pin-top {
      position: absolute;
      top: -24px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 5;
    }

    .polaroid-frame {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .polaroid-inner-art {
      position: relative;
      background: #f8f6f0;
      border: 1.5px solid rgba(42, 45, 62, 0.2);
      border-radius: 2px;
      height: 240px;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      overflow: hidden;
      background-image: radial-gradient(rgba(42, 45, 62, 0.08) 1px, transparent 1px);
      background-size: 16px 16px;
    }
    body[data-paper='night'] .polaroid-inner-art {
      background: #0f172a;
      border-color: rgba(245, 158, 11, 0.2);
      background-image: radial-gradient(rgba(245, 158, 11, 0.1) 1px, transparent 1px);
    }
    .polaroid-humaaan-hero {
      height: 210px;
      width: auto;
      object-fit: contain;
      z-index: 2;
      filter: drop-shadow(2px 4px 8px rgba(0,0,0,0.12));
    }
    .photo-constellation-svg {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
      pointer-events: none;
    }
    .polaroid-chin {
      display: flex;
      flex-direction: column;
      gap: 4px;
      padding: 4px 6px 0;
      text-align: center;
    }
    .polaroid-handwriting {
      font-family: 'Caveat', cursive;
      font-size: 18px;
      line-height: 1.25;
      color: var(--ink);
      font-weight: bold;
    }
    .polaroid-date {
      font-family: 'Space Grotesk', monospace;
      font-size: 10px;
      font-weight: 800;
      color: var(--ink-soft);
      letter-spacing: 1px;
    }

    /* Washi Tape and Pinned Photo Album Cards */
    .uc-card {
      background: #ffffff !important;
      border: 1.5px solid rgba(42, 45, 62, 0.18) !important;
      border-radius: 3px !important;
      padding: 20px 24px !important;
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08), 0 2px 6px rgba(0, 0, 0, 0.04) !important;
      position: relative;
      transform: rotate(-0.8deg);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card-bay:nth-child(even) .uc-card {
      transform: rotate(1deg);
    }
    .uc-card:hover {
      transform: rotate(0deg) translateY(-4px) !important;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.14) !important;
    }
    body[data-paper='night'] .uc-card {
      background: #1e293b !important;
      border-color: rgba(245, 158, 11, 0.3) !important;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5) !important;
    }

    /* Washi Tape Strip at top of card */
    .uc-card::before {
      content: '';
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%) rotate(-1deg);
      width: 90px;
      height: 24px;
      background: rgba(245, 222, 179, 0.85);
      border-left: 2px dashed rgba(42, 45, 62, 0.15);
      border-right: 2px dashed rgba(42, 45, 62, 0.15);
      box-shadow: 0 2px 5px rgba(0,0,0,0.08);
      z-index: 10;
    }
    body[data-paper='night'] .uc-card::before {
      background: rgba(245, 158, 11, 0.3);
      border-color: rgba(255, 255, 255, 0.2);
    }

    /* Photo Album Tape-Style Buttons (Flat & Tactile, No 3D bevels) */
    .album-btn, .tape-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-family: 'Space Grotesk', system-ui, sans-serif;
      font-weight: 700;
      border-radius: 4px;
      cursor: pointer;
      user-select: none;
      text-decoration: none;
      transition: all 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
      box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
      border: 1.5px solid var(--ink);
    }
    .album-btn.primary-tape {
      background: #f59e0b;
      color: #111827;
      border-color: #111827;
    }
    .album-btn.primary-tape:hover {
      background: #fbbf24;
      transform: translateY(-2px) rotate(-0.5deg);
      box-shadow: 0 6px 14px rgba(245, 158, 11, 0.28);
    }
    .album-btn.primary-tape:active {
      transform: translateY(1px);
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
    }
    .album-btn.secondary-tape {
      background: #ffffff;
      color: var(--ink);
      padding: 10px 20px;
    }
    .album-btn.secondary-tape:hover {
      background: #f8fafc;
      transform: translateY(-2px) rotate(0.5deg);
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.12);
    }
    .album-btn.secondary-tape:active {
      transform: translateY(1px);
    }
    body[data-paper='night'] .album-btn.secondary-tape {
      background: #0f172a;
      color: #f8fafc;
      border-color: #f59e0b;
    }
    
    /* Clean up scenario buttons to match album tape tags */
    .scenario-launch-btn {
      background: #fef3c7 !important;
      color: #78350f !important;
      border: 1.5px solid #b45309 !important;
      box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
      border-radius: 4px !important;
      padding: 6px 14px !important;
      font-weight: 700 !important;
      transform: none !important;
    }
    .scenario-launch-btn:hover {
      background: #fde68a !important;
      transform: translateY(-2px) rotate(-0.5deg) !important;
      box-shadow: 0 4px 10px rgba(180, 83, 9, 0.2) !important;
    }
    body[data-paper='night'] .scenario-launch-btn {
      background: rgba(245, 158, 11, 0.15) !important;
      color: #fde68a !important;
      border-color: #f59e0b !important;
    }
'''

content = content.replace('/* Specific Landing Page Styles', photo_album_css + '\n    /* Specific Landing Page Styles')

# 4. Scroll Animation Engine for Background Humaaans
humaaans_scroll_script = '''
    // Scroll-Driven Animation Engine for Background Humaaans
    // Tweens scale, rotation, translateY, and opacity as the user scrolls
    const bgHumaaans = [
      { id: 'bgHumaaan1', baseTop: 140, speed: 0.18, minScale: 0.9, maxScale: 1.15, rotRange: 4 },
      { id: 'bgHumaaan2', baseTop: 900, speed: -0.15, minScale: 0.85, maxScale: 1.1, rotRange: -5 },
      { id: 'bgHumaaan3', baseTop: 1700, speed: 0.16, minScale: 0.9, maxScale: 1.12, rotRange: 4 },
      { id: 'bgHumaaan4', baseTop: 2500, speed: -0.14, minScale: 0.85, maxScale: 1.1, rotRange: -4 },
      { id: 'bgHumaaan5', baseTop: 3200, speed: 0.2, minScale: 0.88, maxScale: 1.15, rotRange: 5 }
    ];

    let ticking = false;
    function updateHumaaansParallax() {
      const scrollY = window.pageYOffset || document.documentElement.scrollTop;
      const vh = window.innerHeight;

      bgHumaaans.forEach(h => {
        const el = document.getElementById(h.id);
        if (!el) return;

        // Calculate position relative to viewport
        const itemCenter = h.baseTop + 190;
        const distFromCenter = (itemCenter - scrollY) - (vh / 2);
        const normDist = distFromCenter / (vh * 0.8);
        const clampedNorm = Math.max(-1, Math.min(1, normDist));

        // Visibility & Opacity Envelope (peak near center)
        const inViewFactor = 1 - Math.abs(clampedNorm);
        const opacity = Math.max(0.08, inViewFactor * 0.38);

        // Zoom / Scale Tween
        const scale = h.minScale + inViewFactor * (h.maxScale - h.minScale);

        // Rotation & Parallax Tween
        const rot = clampedNorm * h.rotRange;
        const translateY = distFromCenter * h.speed;

        el.style.opacity = opacity.toFixed(2);
        el.style.transform = `translate3d(0, ${translateY.toFixed(1)}px, 0) scale(${scale.toFixed(3)}) rotate(${rot.toFixed(1)}deg)`;
      });

      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(updateHumaaansParallax);
        ticking = true;
      }
    }, { passive: true });

    // Initial positioning
    setTimeout(updateHumaaansParallax, 100);
'''

content = content.replace('// Quick Home Walkthrough Modal', humaaans_scroll_script + '\n    // Quick Home Walkthrough Modal')

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('[OK] Updated home.html with Photo Album aesthetic and scroll-animated background Humaaans!')
