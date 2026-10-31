import sys, os

sys.stdout.reconfigure(encoding='utf-8')

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>GoalStar — A* Pathfinding for Life Goals, Backed by Portable Memory</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'><polygon points='20,4 24,14 35,15 27,22 29,33 20,27 11,33 13,22 5,15 16,14' fill='%23f59e0b'/></svg>">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Playfair+Display:ital,wght@0,600;0,800;0,900;1,600&family=Space+Grotesk:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="css/style.css">
  
  <style>
    /* ========================================================
       EDITORIAL PHOTO ALBUM THEME & SPACING (FRONTEND-DESIGN)
       ======================================================== */
    :root {
      --paper: #fbf9f4;
      --paper-warm: #f6f2e9;
      --panel: #ffffff;
      --panel-card: #ffffff;
      --ink: #1e293b;
      --ink-soft: #475569;
      --ink-muted: #64748b;
      --accent: #d97706;
      --accent-hover: #b45309;
      --green: #059669;
      --green-light: #10b981;
      --red: #dc2626;
      --washi-light: rgba(245, 222, 179, 0.88);
      --card-shadow: 0 12px 28px rgba(0, 0, 0, 0.09), 0 2px 6px rgba(0, 0, 0, 0.04);
      --card-border: 1.5px solid rgba(42, 45, 62, 0.18);
    }

    body[data-paper='night'] {
      --paper: #0b111e;
      --paper-warm: #0f172a;
      --panel: #151e2e;
      --panel-card: #182234;
      --ink: #f1f5f9;
      --ink-soft: #cbd5e1;
      --ink-muted: #94a3b8;
      --accent: #f59e0b;
      --accent-hover: #d97706;
      --green: #10b981;
      --green-light: #34d399;
      --red: #ef4444;
      --washi-light: rgba(245, 158, 11, 0.28);
      --card-shadow: 0 16px 36px rgba(0, 0, 0, 0.6), 0 3px 8px rgba(0, 0, 0, 0.4);
      --card-border: 1.5px solid rgba(245, 158, 11, 0.3);
    }

    html {
      scroll-behavior: smooth;
    }

    html:has(body.landing-body), body.landing-body {
      height: auto !important;
      min-height: 100vh !important;
      overflow-x: hidden !important;
      overflow-y: auto !important;
    }

    body.landing-body {
      margin: 0;
      padding: 0;
      background-color: var(--paper);
      color: var(--ink);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      position: relative;
      line-height: 1.55;
    }

    /* Subtle Paper Grid Texture */
    body.landing-body::before {
      content: '';
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
      opacity: 0.4;
      background-image: 
        linear-gradient(rgba(42, 45, 62, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(42, 45, 62, 0.04) 1px, transparent 1px);
      background-size: 32px 32px;
    }

    body[data-paper='night']::before {
      opacity: 0.18;
      background-image: 
        linear-gradient(rgba(245, 158, 11, 0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(245, 158, 11, 0.07) 1px, transparent 1px);
    }

    /* ----------------------------------------------------
       BACKGROUND PARALLAX HUMAAANS (5 FIGURES)
       ---------------------------------------------------- */
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
      opacity: 0.22;
      filter: grayscale(12%) drop-shadow(0 15px 25px rgba(0,0,0,0.06));
      transform-origin: center center;
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

    @media (max-width: 768px) {
      .bg-humaaan-item {
        opacity: 0.11;
      }
      .bg-humaaan-img {
        height: 230px;
      }
    }

    /* ----------------------------------------------------
       STICKY RESPONSIVE HEADER
       ---------------------------------------------------- */
    .landing-header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--panel);
      border-bottom: 2px solid var(--ink);
      box-shadow: 0 3px 0 var(--ink), 0 6px 14px rgba(0,0,0,0.08);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 24px;
      gap: 16px;
      backdrop-filter: blur(8px);
      box-sizing: border-box;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      color: var(--ink);
      flex-shrink: 0;
    }

    .brand .logo {
      width: 32px;
      height: 32px;
    }

    .brand .word {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
    }

    .brand .word b {
      color: var(--accent);
    }

    .landing-nav {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .landing-nav a {
      color: var(--ink-soft);
      text-decoration: none;
      font-size: 14px;
      font-weight: 600;
      transition: color 0.2s;
    }

    .landing-nav a:hover {
      color: var(--accent);
    }

    .landing-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    /* Engraved Pill Switches */
    .engraved-switch {
      position: relative;
      width: 102px;
      height: 34px;
      cursor: pointer;
      user-select: none;
      border-radius: 17px;
      outline: none;
      flex-shrink: 0;
    }

    .engraved-switch .switch-track {
      position: relative;
      width: 100px;
      height: 32px;
      background: #e2ded7;
      border: 1.5px solid rgba(42, 45, 62, 0.3);
      border-radius: 16px;
      box-shadow: 
        inset 0 3px 6px rgba(0,0,0,0.22),
        inset 0 1px 2px rgba(0,0,0,0.18),
        0 1px 0 rgba(255,255,255,0.7);
      box-sizing: border-box;
    }

    body[data-paper='night'] .engraved-switch .switch-track {
      background: #0f172a;
      border-color: rgba(245, 158, 11, 0.4);
      box-shadow: 
        inset 0 3px 6px rgba(0,0,0,0.65),
        inset 0 1px 3px rgba(0,0,0,0.5),
        0 1px 0 rgba(245, 158, 11, 0.15);
    }

    .engraved-switch .switch-knob {
      position: absolute;
      top: 2px;
      left: 3px;
      width: 25px;
      height: 25px;
      background: #ffffff;
      border-radius: 50%;
      border: 1px solid rgba(42, 45, 62, 0.2);
      box-shadow: 
        0 3px 6px rgba(0,0,0,0.22),
        0 1px 2px rgba(0,0,0,0.14),
        inset 0 1px 0 #ffffff;
      transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
      z-index: 3;
    }

    body[data-paper='night'] .engraved-switch .switch-knob {
      background: #334155;
      border-color: rgba(245, 158, 11, 0.4);
      box-shadow: 
        0 3px 8px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.2);
    }

    .engraved-switch.active .switch-knob {
      transform: translateX(67px);
    }

    .engraved-switch .track-label {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1px;
      color: rgba(42, 45, 62, 0.65);
      text-shadow: 0 1px 0 rgba(255,255,255,0.7);
      pointer-events: none;
      z-index: 1;
      text-align: center;
      left: 32px;
      width: 60px;
    }

    body[data-paper='night'] .engraved-switch .track-label {
      color: rgba(245, 158, 11, 0.75);
      text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }

    .engraved-switch.active .track-label {
      left: 8px;
      width: 58px;
    }

    /* Buttons: Flat Tactile Photo Album Style (No 3D Bevels) */
    .album-btn, .tape-btn {
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      font-size: 14px;
      padding: 8px 16px;
      border: 1.5px solid var(--ink);
      border-radius: 3px;
      background: #ffffff;
      color: var(--ink);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      text-decoration: none;
      box-shadow: 2px 2px 0 var(--ink);
      transition: transform 0.12s ease, box-shadow 0.12s ease, background 0.15s ease;
      position: relative;
      box-sizing: border-box;
      line-height: 1.2;
    }

    .album-btn:hover {
      transform: translate(-1px, -1px);
      box-shadow: 3px 3px 0 var(--ink);
    }

    .album-btn:active {
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0 var(--ink);
    }

    .album-btn.primary-tape {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--ink);
    }

    .album-btn.primary-tape:hover {
      background: var(--accent-hover);
    }

    .album-btn.secondary-tape {
      background: var(--paper-warm);
      color: var(--ink);
    }

    body[data-paper='night'] .album-btn {
      background: #1e293b;
      color: #f1f5f9;
      border-color: rgba(245, 158, 11, 0.4);
      box-shadow: 2px 2px 0 rgba(245, 158, 11, 0.3);
    }
    /* Interactive Tour Button Bounce Animation */
    @keyframes tourBounce {
      0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-6px); }
      60% { transform: translateY(-3px); }
    }
    .tour-bounce-btn {
      animation: tourBounce 2.2s infinite cubic-bezier(0.28, 0.84, 0.42, 1) !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }


    body[data-paper='night'] .album-btn.primary-tape {
      background: #d97706;
      color: #ffffff;
    }

    .user-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      font-weight: 600;
      padding: 4px 10px;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      border-radius: 12px;
    }

    .user-badge .indicator.live {
      width: 7px;
      height: 7px;
      background: var(--green);
      border-radius: 50%;
    }

    .logout-link {
      background: none;
      border: none;
      color: var(--ink-soft);
      font-size: 12px;
      cursor: pointer;
      text-decoration: underline;
      padding: 0 4px;
    }

    /* ----------------------------------------------------
       HERO SECTION WITH HANGING PHOTO (PHOTO ALBUM AESTHETIC)
       ---------------------------------------------------- */
    main.landing-main {
      display: block !important;
      position: relative !important;
      z-index: 1 !important;
      max-width: 1200px !important;
      width: 100% !important;
      margin: 0 auto !important;
      box-sizing: border-box !important;
      overflow-x: hidden !important;
    }

    .hero-sec {
      padding: 56px 24px 44px;
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      align-items: center;
      gap: 40px;
      position: relative;
      box-sizing: border-box;
    }

    .hero-left {
      will-change: transform;
    }

    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: 'Space Grotesk', monospace;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.8px;
      padding: 5px 12px;
      background: var(--paper-warm);
      border: 1.5px solid var(--ink);
      border-radius: 3px;
      box-shadow: 2px 2px 0 var(--ink);
      margin-bottom: 20px;
      color: var(--ink);
    }

    .hero-badge::before {
      content: '';
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent);
      display: inline-block;
      animation: pulseDot 2s ease-in-out infinite;
    }

    @keyframes pulseDot {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.3); opacity: 0.7; }
    }

    body[data-paper='night'] .hero-badge {
      background: #1e293b;
      border-color: rgba(245, 158, 11, 0.4);
      box-shadow: 2px 2px 0 rgba(245, 158, 11, 0.3);
    }

    .hero-title {
      font-family: 'Playfair Display', serif;
      font-size: clamp(2.1rem, 4.2vw, 3.5rem);
      font-weight: 900;
      line-height: 1.18;
      margin: 0 0 18px 0;
      letter-spacing: -0.5px;
      color: var(--ink);
    }

    .ink-hl-wrap {
      position: relative;
      display: inline-block;
      white-space: nowrap;
    }

    .ink-hl-text {
      color: var(--accent);
      position: relative;
      z-index: 2;
    }

    .ink-swash-svg {
      position: absolute;
      left: -4%;
      bottom: -10px;
      width: 108%;
      height: 26px;
      pointer-events: none;
      z-index: 1;
      transform-origin: left center;
      will-change: transform;
      transition: transform 0.15s ease-out;
    }

    .hero-desc {
      font-size: 18px;
      line-height: 1.6;
      color: var(--ink-soft);
      max-width: 580px;
      margin: 0 0 28px 0;
    }

    .hero-cta-row {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }

    /* Hanging Polaroid Photo Card */
    .hanging-photo-card {
      position: relative;
      background: #ffffff;
      border: var(--card-border);
      border-radius: 4px;
      padding: 14px 14px 22px;
      box-shadow: 
        0 16px 32px rgba(0, 0, 0, 0.12),
        0 3px 8px rgba(0, 0, 0, 0.06);
      transform-origin: top center;
      will-change: transform;
      max-width: 350px;
      margin: 20px auto 0;
      z-index: 2;
      box-sizing: border-box;
      transition: transform 0.2s ease-out;
    }

    body[data-paper='night'] .hanging-photo-card {
      background: #1e293b;
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.6);
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
      border: 1.5px solid rgba(42, 45, 62, 0.18);
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
      height: 215px;
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
      font-size: 19px;
      line-height: 1.25;
      color: var(--ink);
      font-weight: 700;
      transition: transform 0.2s ease;
    }

    .polaroid-date {
      font-family: 'Space Grotesk', monospace;
      font-size: 10.5px;
      font-weight: 800;
      color: var(--ink-muted);
      letter-spacing: 1px;
    }

    /* ----------------------------------------------------
       LIVE SIMULATOR WIDGET SECTION
       ---------------------------------------------------- */
    .simulator-sec {
      padding: 24px;
      margin: 12px 0 36px;
      box-sizing: border-box;
    }

    .sim-card {
      background: var(--panel-card);
      border: var(--card-border);
      border-radius: 4px;
      padding: 24px 28px;
      box-shadow: var(--card-shadow);
      max-width: 980px;
      margin: 0 auto;
      position: relative;
      will-change: transform;
      box-sizing: border-box;
      transition: transform 0.2s ease-out;
    }

    /* Top Washi Tape on Simulator */
    .sim-card::before {
      content: '';
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%) rotate(0.5deg);
      width: 110px;
      height: 24px;
      background: var(--washi-light);
      border-left: 2px dashed rgba(42, 45, 62, 0.18);
      border-right: 2px dashed rgba(42, 45, 62, 0.18);
      box-shadow: 0 2px 5px rgba(0,0,0,0.06);
      z-index: 10;
    }

    .sim-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 20px;
    }

    .sim-head h3 {
      font-family: 'Playfair Display', serif;
      font-size: 22px;
      margin: 0;
      color: var(--ink);
    }

    .sim-slider-box {
      display: flex;
      align-items: center;
      gap: 12px;
      background: var(--paper-warm);
      padding: 6px 14px;
      border: 1.5px solid var(--ink);
      border-radius: 3px;
      position: relative;
      overflow: hidden;
    }

    .slider-fill-track {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      background: rgba(5, 150, 105, 0.12);
      pointer-events: none;
      transition: width 0.3s ease;
      z-index: 0;
    }

    body[data-paper='night'] .sim-slider-box {
      background: #0f172a;
      border-color: rgba(245, 158, 11, 0.35);
    }

    .sim-slider-box input[type="range"] {
      cursor: pointer;
      accent-color: var(--accent);
      position: relative;
      z-index: 1;
    }

    .sim-slider-box label, .sim-slider-box span {
      position: relative;
      z-index: 1;
    }

    .sim-canvas {
      position: relative;
      background: var(--paper-warm);
      border: 1.5px solid rgba(42, 45, 62, 0.15);
      border-radius: 4px;
      padding: 28px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      box-sizing: border-box;
    }

    body[data-paper='night'] .sim-canvas {
      background: #0f172a;
      border-color: rgba(245, 158, 11, 0.2);
    }

    .sim-node {
      background: #ffffff;
      border: 1.5px solid var(--ink);
      border-radius: 3px;
      padding: 10px 14px;
      text-align: center;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 13.5px;
      font-weight: 700;
      color: var(--ink);
      box-shadow: 2px 2px 0 var(--ink);
      z-index: 2;
      flex: 1;
      max-width: 190px;
      transition: all 0.25s ease;
      box-sizing: border-box;
    }

    body[data-paper='night'] .sim-node {
      background: #1e293b;
      border-color: rgba(245, 158, 11, 0.4);
      color: #f1f5f9;
      box-shadow: 2px 2px 0 rgba(245, 158, 11, 0.3);
    }

    .sim-node small {
      display: block;
      font-weight: 500;
      font-size: 11px;
      color: var(--ink-muted);
      margin-top: 3px;
      transition: transform 0.2s ease;
    }

    .sim-node.active-path {
      background: #d1fae5 !important;
      border-color: #047857 !important;
      color: #065f46 !important;
      box-shadow: 3px 3px 0 #047857 !important;
      transform: translateY(-2px);
    }

    body[data-paper='night'] .sim-node.active-path {
      background: #064e3b !important;
      border-color: #10b981 !important;
      color: #6ee7b7 !important;
      box-shadow: 3px 3px 0 #10b981 !important;
    }

    .sim-node.blocked-path {
      background: #fee2e2 !important;
      border-color: #b91c1c !important;
      color: #991b1b !important;
      opacity: 0.7;
    }

    body[data-paper='night'] .sim-node.blocked-path {
      background: #450a0a !important;
      border-color: #ef4444 !important;
      color: #fca5a5 !important;
    }

    .sim-feedback-box {
      margin-top: 14px;
      padding: 10px 14px;
      background: var(--paper-warm);
      border-left: 3px solid var(--accent);
      border-radius: 0 4px 4px 0;
      font-size: 15px;
      color: var(--ink);
    }

    body[data-paper='night'] .sim-feedback-box {
      background: #0f172a;
    }

    /* ----------------------------------------------------
       USE CASES JOURNEY (HANGING SCRAPBOOK CARDS)
       ---------------------------------------------------- */
    .use-cases-sec {
      position: relative;
      padding: 40px 24px 80px;
      max-width: 980px;
      margin: 0 auto;
      box-sizing: border-box;
    }

    .sec-header {
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
    }

    .sec-tag {
      font-family: 'Space Grotesk', monospace;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 1.2px;
      color: var(--accent);
      text-transform: uppercase;
      margin-bottom: 6px;
      display: inline-block;
    }

    .sec-title {
      font-family: 'Playfair Display', serif;
      font-size: clamp(1.8rem, 3.5vw, 2.6rem);
      font-weight: 900;
      margin: 0 0 10px 0;
      color: var(--ink);
    }

    .sec-desc {
      font-size: 16px;
      color: var(--ink-soft);
      max-width: 600px;
      margin: 0 auto;
    }

    .journey-track {
      position: relative;
      display: flex;
      flex-direction: column;
      gap: 52px;
    }

    .card-bay {
      position: relative;
      width: 100%;
    }

    /* Solid Opaque Cards (Frontend-Design Polish) */
    .uc-card {
      background: #ffffff !important;
      border: 1.5px solid rgba(42, 45, 62, 0.18) !important;
      border-radius: 4px;
      padding: 24px 28px;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.09), 0 2px 6px rgba(0, 0, 0, 0.04) !important;
      position: relative;
      box-sizing: border-box;
      opacity: 1 !important;
      will-change: transform;
      transition: box-shadow 0.25s ease, transform 0.2s ease-out;
    }

    body[data-paper='night'] .uc-card {
      background: #182234 !important;
      border-color: rgba(245, 158, 11, 0.3) !important;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6) !important;
      opacity: 1 !important;
    }

    .uc-card:hover {
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.14) !important;
    }

    /* Washi Tape Strip on each card */
    .uc-card::before {
      content: '';
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%) rotate(-0.8deg);
      width: 95px;
      height: 24px;
      background: var(--washi-light);
      border-left: 2px dashed rgba(42, 45, 62, 0.16);
      border-right: 2px dashed rgba(42, 45, 62, 0.16);
      box-shadow: 0 2px 5px rgba(0,0,0,0.06);
      z-index: 10;
    }

    .uc-card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 18px;
      border-bottom: 1.5px dashed rgba(42, 45, 62, 0.14);
      padding-bottom: 12px;
    }

    body[data-paper='night'] .uc-card-header {
      border-bottom-color: rgba(245, 158, 11, 0.2);
    }

    .uc-badge-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .uc-step-num {
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 800;
      color: var(--accent);
      background: var(--paper-warm);
      padding: 3px 8px;
      border: 1px solid var(--accent);
      border-radius: 2px;
      transition: transform 0.2s ease;
      display: inline-block;
    }

    .uc-role {
      font-family: 'Playfair Display', serif;
      font-size: 21px;
      font-weight: 800;
      margin: 0;
      color: var(--ink);
    }

    .uc-status-tag {
      font-family: 'Space Grotesk', monospace;
      font-size: 12px;
      font-weight: 700;
      color: var(--ink-muted);
      background: var(--paper-warm);
      padding: 4px 10px;
      border-radius: 3px;
      border: 1px solid rgba(42, 45, 62, 0.12);
    }

    body[data-paper='night'] .uc-status-tag {
      background: #0f172a;
      border-color: rgba(245, 158, 11, 0.25);
    }

    .uc-content-flex {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
    }

    .uc-details {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .uc-bullet-item {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      font-size: 15px;
      line-height: 1.5;
      position: relative;
    }

    .uc-bullet-item p {
      margin: 0;
      color: var(--ink-soft);
    }

    .bullet-tag {
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 2px;
      flex-shrink: 0;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      transition: transform 0.2s ease;
    }

    .bullet-tag.hurdle {
      background: rgba(220, 38, 38, 0.12);
      color: var(--red);
      border: 1px solid rgba(220, 38, 38, 0.3);
    }

    .bullet-tag.fix {
      background: rgba(5, 150, 105, 0.12);
      color: var(--green);
      border: 1px solid rgba(5, 150, 105, 0.3);
    }

    .uc-humaaan-frame {
      width: 140px;
      height: 140px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .uc-humaaan-img {
      max-height: 140px;
      width: auto;
      object-fit: contain;
      filter: drop-shadow(0 6px 12px rgba(0,0,0,0.08));
      will-change: transform;
      transition: transform 0.2s ease-out;
    }

    .uc-card-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
      padding-top: 14px;
      border-top: 1.5px dashed rgba(42, 45, 62, 0.14);
      position: relative;
    }

    body[data-paper='night'] .uc-card-footer {
      border-top-color: rgba(245, 158, 11, 0.2);
    }

    .uc-stat-pill {
      font-family: 'Space Grotesk', monospace;
      font-size: 12px;
      font-weight: 800;
      color: var(--green);
      background: rgba(5, 150, 105, 0.08);
      padding: 4px 10px;
      border-radius: 3px;
      border: 1px solid rgba(5, 150, 105, 0.25);
      transition: transform 0.2s ease;
      display: inline-block;
    }

    /* Target Arrival Ring on Card 5 */
    .card5-target-wrap {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }

    .card5-target-ring {
      position: absolute;
      width: calc(100% + 14px);
      height: calc(100% + 14px);
      border: 2px dashed #059669;
      border-radius: 6px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease, transform 0.3s ease;
      animation: targetPulse 2s ease-in-out infinite;
    }

    @keyframes targetPulse {
      0%, 100% { transform: scale(1); opacity: 0.9; }
      50% { transform: scale(1.04); opacity: 0.5; }
    }

    /* ----------------------------------------------------
       PRECISION SVG TRACK & TRAVELING ARROW
       ---------------------------------------------------- */
    .journey-svg-track {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 1;
      overflow: visible;
    }

    .traveling-arrow {
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
    }

    /* Scroll HUD */
    .scroll-hud {
      position: fixed;
      right: 20px;
      top: 50%;
      transform: translateY(-50%);
      background: var(--panel);
      border: 1.5px solid var(--ink);
      border-radius: 4px;
      padding: 10px 14px;
      box-shadow: 3px 3px 0 var(--ink);
      z-index: 90;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .hud-step {
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 700;
      color: var(--ink-muted);
      display: flex;
      align-items: center;
      gap: 6px;
      transition: color 0.2s;
    }

    .hud-step.active {
      color: var(--accent);
      font-weight: 900;
    }

    .hud-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--ink-muted);
      transition: background 0.2s, transform 0.2s;
    }

    .hud-step.active .hud-dot {
      background: var(--accent);
      transform: scale(1.4);
    }

    /* ----------------------------------------------------
       RESPONSIVE BREAKPOINTS (MOBILE & TABLET POLISH)
       ---------------------------------------------------- */
    @media (max-width: 1140px) {
      .scroll-hud {
        display: none;
      }
    }

    @media (max-width: 880px) {
      .hero-sec {
        grid-template-columns: 1fr;
        padding: 36px 20px 28px;
        gap: 32px;
        text-align: center;
      }
      .hero-desc {
        margin: 0 auto 24px auto;
      }
      .hero-cta-row {
        justify-content: center;
      }
      .hanging-photo-card {
        margin: 10px auto 0;
      }
      .sim-head {
        flex-direction: column;
        align-items: stretch;
      }
      .sim-slider-box {
        justify-content: space-between;
      }
    }

    @media (max-width: 768px) {
      .landing-header {
        padding: 8px 14px;
        gap: 8px;
      }
      .landing-nav {
        display: none;
      }
      .landing-actions {
        gap: 8px;
      }
      .engraved-switch {
        width: 88px;
        height: 32px;
      }
      .engraved-switch .switch-track {
        width: 86px;
        height: 30px;
        border-radius: 15px;
      }
      .engraved-switch .switch-knob {
        width: 23px;
        height: 23px;
        top: 2px;
        left: 2px;
      }
      .engraved-switch.active .switch-knob {
        transform: translateX(57px);
      }
      .engraved-switch .track-label {
        font-size: 10px;
        left: 26px;
        width: 54px;
      }
      .engraved-switch.active .track-label {
        left: 4px;
        width: 52px;
      }
      .album-btn, .tape-btn {
        padding: 7px 12px;
        font-size: 13px;
      }
      .uc-content-flex {
        flex-direction: column-reverse;
        align-items: center;
        text-align: left;
      }
      .uc-humaaan-frame {
        width: 120px;
        height: 120px;
      }
      .uc-humaaan-img {
        max-height: 120px;
      }
    }

    @media (max-width: 600px) {
      .hero-title {
        font-size: 28px;
      }
      .hero-desc {
        font-size: 15px;
      }
      .sim-canvas {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        padding: 16px 10px;
      }
      .sim-node {
        max-width: none;
        width: 100%;
        padding: 8px 6px;
        font-size: 12px;
      }
      .journey-svg-track, .traveling-arrow {
        display: none;
      }
      .hero-cta-row {
        flex-direction: column;
        width: 100%;
      }
      .hero-cta-row .album-btn {
        width: 100%;
      }
    /* Interactive Tour Button Bounce Animation */
    @keyframes tourBounce {
      0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-6px); }
      60% { transform: translateY(-3px); }
    }
    .tour-bounce-btn {
      animation: tourBounce 2.2s infinite cubic-bezier(0.28, 0.84, 0.42, 1) !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }

      .uc-card {
        padding: 18px 16px;
      }
      .uc-card-header {
        flex-direction: column;
        align-items: flex-start;
      }
      .uc-card-footer {
        flex-direction: column;
        align-items: stretch;
      }
      .uc-card-footer .album-btn {
        width: 100%;
      }
    /* Interactive Tour Button Bounce Animation */
    @keyframes tourBounce {
      0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-6px); }
      60% { transform: translateY(-3px); }
    }
    .tour-bounce-btn {
      animation: tourBounce 2.2s infinite cubic-bezier(0.28, 0.84, 0.42, 1) !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }

    }

    @media (max-width: 420px) {
      #launchPlannerTopBtn {
        display: none;
      }
      .brand .word {
        font-size: 17px;
      }
      .landing-header {
        padding: 8px 10px;
      }
      .hanging-photo-card {
        max-width: 290px;
        padding: 10px 10px 18px;
      }
      .polaroid-inner-art {
        height: 190px;
      }
      .polaroid-humaaan-hero {
        height: 160px;
      }
    }

    /* ----------------------------------------------------
       PROGRESSIVE SCENARIO SIMULATION WALKTHROUGH MODAL
       ---------------------------------------------------- */
    .scenario-modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(5px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 16px;
      box-sizing: border-box;
    }

    .scenario-modal[hidden] {
      display: none;
    }

    .scenario-modal-box {
      background: var(--panel);
      border: 2px solid var(--ink);
      border-radius: 6px;
      box-shadow: 6px 6px 0 var(--ink);
      width: 100%;
      max-width: 580px;
      padding: 26px;
      position: relative;
      box-sizing: border-box;
      max-height: 92vh;
      overflow-y: auto;
    }

    .scenario-modal-head {
      margin-bottom: 18px;
      border-bottom: 1.5px dashed rgba(42, 45, 62, 0.16);
      padding-bottom: 14px;
    }

    .scenario-step-indicator {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 8px;
    }

    .step-pill {
      flex: 1;
      height: 4px;
      background: rgba(42, 45, 62, 0.15);
      border-radius: 2px;
      transition: background 0.25s ease;
    }

    .step-pill.active {
      background: var(--accent);
    }

    .step-pill.passed {
      background: var(--green);
    }

    .scenario-stage-content {
      min-height: 220px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 14px;
    }

    .scenario-card-preview {
      background: var(--paper-warm);
      border: 1.5px solid var(--ink);
      border-radius: 4px;
      padding: 14px 18px;
      box-shadow: 2px 2px 0 var(--ink);
    }

    body[data-paper='night'] .scenario-card-preview {
      background: #0f172a;
      border-color: rgba(245, 158, 11, 0.35);
    }

    .scenario-route-diagram {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin: 10px 0;
    }

    .scenario-node-box {
      flex: 1;
      padding: 8px 10px;
      border: 1.5px solid var(--ink);
      border-radius: 3px;
      font-size: 12px;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      text-align: center;
      background: #ffffff;
      box-shadow: 2px 2px 0 var(--ink);
    }

    body[data-paper='night'] .scenario-node-box {
      background: #1e293b;
    }

    .scenario-node-box.highlight {
      border-color: var(--green) !important;
      background: #d1fae5 !important;
      color: #065f46 !important;
      box-shadow: 2px 2px 0 var(--green) !important;
    }

    body[data-paper='night'] .scenario-node-box.highlight {
      background: #064e3b !important;
      color: #6ee7b7 !important;
    }

    .scenario-node-box.hurdle-node {
      border-color: var(--red) !important;
      background: #fee2e2 !important;
      color: #991b1b !important;
      opacity: 0.75;
    }

    body[data-paper='night'] .scenario-node-box.hurdle-node {
      background: #450a0a !important;
      color: #fca5a5 !important;
    }

    /* Sui Onchain Verification Card (Matching Image 1) */
    .sui-verified-box {
      background: #ecfeff;
      border: 1.5px solid #06b6d4;
      border-radius: 4px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    body[data-paper='night'] .sui-verified-box {
      background: #083344;
      border-color: #0891b2;
    }

    .sui-head-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #0891b2;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 800;
      font-size: 13.5px;
    }

    .sui-badge-pill {
      font-size: 10.5px;
      background: #0891b2;
      color: #ffffff;
      padding: 2px 8px;
      border-radius: 99px;
      font-weight: 700;
    }

    .sui-details-row {
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      color: #155e75;
      line-height: 1.4;
      word-break: break-all;
    }

    body[data-paper='night'] .sui-details-row {
      color: #67e8f9;
    }

    /* Mini Cost Breakdown Bars (Matching Image 1) */
    .mini-chart-bars {
      display: flex;
      align-items: flex-end;
      gap: 12px;
      height: 80px;
      padding: 8px 12px 0;
      border-bottom: 2px solid var(--ink);
      margin: 8px 0;
    }

    .mini-bar-col {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      height: 100%;
      justify-content: flex-end;
    }

    .mini-bar {
      width: 100%;
      max-width: 32px;
      border: 1.5px solid var(--ink);
      border-radius: 2px 2px 0 0;
      transition: height 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .bar-time { background: #10b981; }
    .bar-money { background: #34d399; }
    .bar-effort { background: #f59e0b; }
    .bar-risk { background: #f87171; }

    .scenario-modal-actions {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-top: 20px;
      padding-top: 14px;
      border-top: 1.5px dashed rgba(42, 45, 62, 0.16);
    }

    /* Standard Modals */
    .login-dialog, .home-tour-modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(4px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 16px;
      box-sizing: border-box;
    }

    .login-dialog[hidden], .home-tour-modal[hidden] {
      display: none;
    }

    .login-box, .home-tour-content {
      background: var(--panel);
      border: 2px solid var(--ink);
      border-radius: 4px;
      box-shadow: 5px 5px 0 var(--ink);
      width: 100%;
      max-width: 460px;
      padding: 24px;
      position: relative;
      box-sizing: border-box;
      max-height: 90vh;
      overflow-y: auto;
    }

    .close-modal-btn {
      position: absolute;
      top: 14px;
      right: 14px;
      background: none;
      border: none;
      font-size: 22px;
      line-height: 1;
      color: var(--ink-soft);
      cursor: pointer;
      padding: 4px 8px;
    }

    .close-modal-btn:hover {
      color: var(--ink);
    }

    .modal-head {
      margin-bottom: 18px;
    }

    .modal-head h3 {
      font-family: 'Playfair Display', serif;
      font-size: 22px;
      margin: 0 0 6px 0;
      color: var(--ink);
    }

    .login-opts {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .login-opt-btn {
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 12px 14px;
      background: var(--paper-warm);
      border: 1.5px solid var(--ink);
      border-radius: 3px;
      cursor: pointer;
      text-align: left;
      transition: background 0.15s, transform 0.12s;
    }

    .login-opt-btn:hover {
      background: var(--panel);
      transform: translateX(3px);
    }

    .opt-icon-svg {
      width: 24px;
      height: 24px;
      flex-shrink: 0;
      color: var(--accent);
    }

    .opt-label {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 14px;
      font-weight: 700;
      color: var(--ink);
    }

    .opt-desc {
      font-size: 12px;
      color: var(--ink-muted);
      margin-top: 2px;
    }

    .home-tour-actions {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 20px;
      padding-top: 14px;
      border-top: 1px dashed rgba(42, 45, 62, 0.2);
    }

    .landing-footer {
      border-top: 2px solid var(--ink);
      background: var(--panel);
      padding: 30px 24px;
      text-align: center;
      margin-top: 40px;
    }

    .footer-content {
      max-width: 700px;
      margin: 0 auto;
      font-size: 14px;
      color: var(--ink-soft);
    }

    .footer-brand {
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 800;
      font-size: 18px;
      color: var(--ink);
      margin-bottom: 8px;
    }
  </style>
</head>
<body class="landing-body" data-paper="lined">

  <!-- 5 Background Parallax Humaaans Figures with Calm Parallax -->
  <div class="bg-humaaans-layer" id="bgHumaaansLayer" aria-hidden="true">
    <div class="bg-humaaan-item" id="bgHu1" style="top: 140px; left: 2%;">
      <img src="assets/humaaans/webp/hu_stand_24.webp" alt="" class="bg-humaaan-img">
    </div>
    <div class="bg-humaaan-item" id="bgHu2" style="top: 760px; right: 2%;">
      <img src="assets/humaaans/webp/hu_sit_1.webp" alt="" class="bg-humaaan-img">
    </div>
    <div class="bg-humaaan-item" id="bgHu3" style="top: 1480px; left: 1%;">
      <img src="assets/humaaans/webp/hu_stand_11.webp" alt="" class="bg-humaaan-img">
    </div>
    <div class="bg-humaaan-item" id="bgHu4" style="top: 2200px; right: 2%;">
      <img src="assets/humaaans/webp/hu_stand_16.webp" alt="" class="bg-humaaan-img">
    </div>
    <div class="bg-humaaan-item" id="bgHu5" style="top: 2880px; left: 3%;">
      <img src="assets/humaaans/webp/hu_sit_6.webp" alt="" class="bg-humaaan-img">
    </div>
  </div>

  <!-- Sticky Header with Engraved Pill Switches and Album Action Buttons -->
  <header class="landing-header">
    <a class="brand" href="/home" title="GoalStar Total Recall Edition">
      <svg class="logo" viewBox="0 0 40 40" aria-hidden="true">
        <path class="trail" d="M9.6 31.2 C 14.5 30.5, 14.5 23.5, 21.2 21.4" stroke="#d97706" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <circle cx="6.2" cy="33" r="3.6" fill="#059669"/>
        <polygon points="28.5,3.0 31.0,9.0 37.5,9.6 32.6,13.8 34.1,20.2 28.5,16.8 22.9,20.2 24.4,13.8 19.5,9.6 26.0,9.0" fill="#f59e0b" stroke="#1e293b" stroke-width="1.5"/>
      </svg>
      <span class="word">goal<b>star</b></span>
    </a>

    <nav class="landing-nav">
      <a href="#simulator">A* Simulator</a>
      <a href="#use-cases">Use Cases</a>
      <a href="javascript:void(0)" id="navTourBtn" class="tour-bounce-btn">Walkthrough</a>
      <a href="javascript:void(0)" id="navLaunchApp">Open App</a>
      <select id="themeSelect" class="theme-select engraved-select" style="margin-left:8px;" title="Choose Theme Aesthetic">
        <option value="notebook">Notebook</option>
        <option value="night">Chalkboard</option>
        <option value="blueprint">Blueprint</option>
        <option value="monograph">Monograph</option>
      </select>
    </nav>

    <div class="landing-actions">
      <!-- Engraved Pill Switch for Theme (LIGHT / DARK) -->
      <div class="engraved-switch" id="themeSwitch" role="button" tabindex="0" title="Toggle Light / Dark Mode">
        <div class="switch-track">
          <div class="switch-knob"></div>
          <span class="track-label">LIGHT</span>
        </div>
      </div>

      <!-- Engraved Pill Switch for Sound (AUDIO / MUTE) -->
      <div class="engraved-switch active" id="soundSwitch" role="button" tabindex="0" title="Toggle Snappy Sound">
        <div class="switch-track">
          <div class="switch-knob"></div>
          <span class="track-label">AUDIO</span>
        </div>
      </div>

      <button id="loginBtn" class="album-btn secondary-tape" title="Connect Wallet or Session">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 2l-2 2m-1.5 1.5L16 7l-1.5-1.5L13 7l-1.5-1.5L10 7M3 13a7 7 0 1 0 14 0 7 7 0 0 0-14 0z"/>
        </svg>
        Log In
      </button>

      <div id="userBadge" class="user-badge" hidden>
        <span class="indicator live"></span>
        <span id="userName" class="user-name">Guest</span>
        <button id="logoutBtn" class="logout-link">logout</button>
      </div>

      <button id="launchPlannerTopBtn" class="album-btn primary-tape launch-btn" title="Open Planner">Launch Planner</button>
    </div>
  </header>

  <!-- Fixed Scroll Progress HUD (Desktop) -->
  <aside class="scroll-hud" id="scrollHud" aria-hidden="true">
    <div style="font-size:9.5px; margin-bottom:4px; color:var(--ink); font-weight:900;">A* SEARCH TRAIL</div>
    <div class="hud-step active" data-step="1"><span class="hud-dot"></span> 01 Founder</div>
    <div class="hud-step" data-step="2"><span class="hud-dot"></span> 02 Student</div>
    <div class="hud-step" data-step="3"><span class="hud-dot"></span> 03 Agency</div>
    <div class="hud-step" data-step="4"><span class="hud-dot"></span> 04 Focus</div>
    <div class="hud-step" data-step="5"><span class="hud-dot"></span> 05 Unified</div>
  </aside>

  <main class="landing-main">
    <!-- Hero Section with Hanging Polaroid Album Card -->
    <section class="hero-sec">
      <div class="hero-left" id="heroLeft">
        <div class="hero-badge" id="heroBadge">WALRUS MAINNET MEMORY · TATUM SUI RPC</div>
        <h1 class="hero-title">
          A* Pathfinding for Life Goals, Backed by 
          <span class="ink-hl-wrap">
            <span class="ink-hl-text">Portable Memory</span>
            <svg class="ink-swash-svg" id="inkSwashSvg" viewBox="0 0 340 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
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
            </svg>
          </span>
        </h1>
        <p class="hero-desc">
          Goals fail when friction builds up. GoalStar calculates your lowest-cost path forward, learns your real-world stamina, and reroutes around roadblocks.
        </p>

        <div class="hero-cta-row">
          <button id="heroLaunchBtn" class="album-btn primary-tape" style="font-size: 17px; padding: 11px 26px;">Open Interactive Planner</button>
          <a href="#simulator" class="album-btn secondary-tape" style="font-size: 15px;">Try A* In Browser</a>
          <button id="heroTourBtn" class="album-btn secondary-tape tour-bounce-btn" style="font-size: 15px;">Walkthrough Tour</button>
        </div>
      </div>

      <div class="hero-right">
        <!-- Photo Album Hanging Photo (Suspended on Twine Clothesline) -->
        <div class="hanging-photo-card" id="heroPhoto">
          <!-- Twine Clothesline & Wooden Clothespin -->
          <div class="photo-pin-top">
            <svg class="clothespin-svg" width="34" height="42" viewBox="0 0 34 42" fill="none">
              <!-- Twine line across top -->
              <line x1="-50" y1="8" x2="84" y2="8" stroke="#8b5e3c" stroke-width="2.5" stroke-dasharray="3 3" />
              <!-- Wooden Clip Body -->
              <rect x="12" y="2" width="10" height="30" rx="3" fill="#d4a373" stroke="#2a2d3e" stroke-width="1.8" />
              <rect x="14" y="14" width="6" height="6" rx="1.5" fill="#9c6644" />
              <line x1="17" y1="2" x2="17" y2="12" stroke="#2a2d3e" stroke-width="1.2" />
              <line x1="17" y1="22" x2="17" y2="32" stroke="#2a2d3e" stroke-width="1.2" />
            </svg>
          </div>

          <!-- Polaroid Photo Frame -->
          <div class="polaroid-frame">
            <div class="polaroid-inner-art">
              <img src="assets/humaaans/webp/hu_stand_24.webp" alt="Life Goal Dreamer" class="polaroid-humaaan-hero" loading="lazy">
              <!-- A* Graph Constellation Line Art -->
              <svg class="photo-constellation-svg" id="heroConstellationSvg" viewBox="0 0 240 180" aria-hidden="true">
                <line x1="40" y1="130" x2="110" y2="70" stroke="#059669" stroke-width="2.5" stroke-dasharray="3 3" />
                <line x1="110" y1="70" x2="185" y2="40" stroke="#059669" stroke-width="3" />
                <circle cx="40" cy="130" r="7" fill="#059669" stroke="#1e293b" stroke-width="2" />
                <circle cx="110" cy="70" r="8" fill="#059669" stroke="#1e293b" stroke-width="2" />
                <polygon points="185,26 190,38 203,39 193,48 196,61 185,54 174,61 177,48 167,39 180,38" fill="#f59e0b" stroke="#1e293b" stroke-width="2" />
              </svg>
            </div>
            <!-- Polaroid Chin with Handwritten Annotation -->
            <div class="polaroid-chin">
              <span class="polaroid-handwriting" id="polaroidCaption">"The shortest path between where you are and where you want to be."</span>
              <span class="polaroid-date">OCT 2026 // SUI &amp; WALRUS</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Live Route Simulator Widget -->
    <section id="simulator" class="simulator-sec">
      <div class="sim-card" id="simCard">
        <div class="sim-head">
          <h3 id="simTitle">Try Dynamic A* Rerouting Live:</h3>
          <div class="sim-slider-box" id="simSliderBox">
            <div class="slider-fill-track" id="sliderFillTrack" style="width: 80%;"></div>
            <label for="frictionSlider" style="font-weight: 700; font-size: 14px;">Current Stamina:</label>
            <input type="range" id="frictionSlider" min="1" max="10" value="8" title="Drag slider to test stamina adaptation">
            <span id="staminaLabel" style="font-weight: 800; width: 95px; font-family:'Space Grotesk', monospace; font-size:13px;">HIGH (8/10)</span>
          </div>
        </div>

        <div class="sim-canvas">
          <div class="sim-node start" id="simNodeStart">
            Start<br><small>Idea Conceived</small>
          </div>

          <div id="simNodeMonolith" class="sim-node mid active-path">
            Monolith &amp; K8s<br><small id="monolithCost">Fast if stamina &ge; 6</small>
          </div>

          <div id="simNodeServerless" class="sim-node mid">
            Serverless &amp; Micro-Tasks<br><small id="serverlessCost">Lowest friction route</small>
          </div>

          <div class="sim-node goal" id="simNodeGoal">
            Shipped on Mainnet<br><small>Verified on Sui</small>
          </div>
        </div>

        <div id="simFeedback" class="sim-feedback-box">
          <b>Green Path Selected:</b> Monolith setup is optimal when stamina is high. Drag slider down to simulate fatigue!
        </div>
      </div>
    </section>

    <!-- Use Cases Journey (Hanging Scrapbook Photo Cards 1 to 5) -->
    <section id="use-cases" class="use-cases-sec">
      <div class="sec-header overcome-header-box" id="overcomeHeaderBox">
        <div class="overcome-tape-top"></div>
        <span class="sec-tag">Tested Across High-Stakes Scenarios</span>
        <h2 class="sec-title">Engineered to Overcome Human Friction</h2>
        <p class="sec-desc">Real workflows where willpower fails and dynamic A* pathfinding keeps you moving forward.</p>
      </div>

      <div class="journey-track" id="journeyTrack">
        <!-- SVG Track for Traveling Kinetic Arrow (Desktop) -->
        <svg class="journey-svg-track" id="journeySvgTrack">
          <path id="journeySvgPath" d="" fill="none" stroke="rgba(42, 45, 62, 0.14)" stroke-width="3" stroke-dasharray="6 6"/>
          <path id="journeyActivePath" d="" fill="none" stroke="#059669" stroke-width="4"/>
        </svg>

        <div class="traveling-arrow" id="travelingArrow">
          <svg viewBox="0 0 24 24" fill="#059669">
            <polygon points="12,2 22,22 12,17 2,22"/>
          </svg>
        </div>

        <!-- Card 1 -->
        <div class="card-bay" data-step="1">
          <article class="uc-card" id="card1">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 01</span>
                <h3 class="uc-role">The Indie Hacker &amp; Solo Founder</h3>
              </div>
              <span class="uc-status-tag">Infrastructure Fatigue Rerouting</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item">
                  <span class="bullet-tag hurdle">Hurdle</span>
                  <p><strong>14 days trapped in DevOps:</strong> Wrestling Docker, Kubernetes, and VPC configs before testing a single product idea.</p>
                </div>
                <div class="uc-bullet-item">
                  <span class="bullet-tag fix">A* Route</span>
                  <p><strong>Zero-config serverless pivot:</strong> Detects repetitive setup blocks and dynamically shifts route to serverless PaaS and instant deployments.</p>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_sit_1.webp" alt="Solo founder working" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">-12 Days Saved · Shipped in 48h</span>
              <button class="album-btn scenario-launch-btn" data-scenario="saas">Simulate Route</button>
            </div>
          </article>
        </div>

        <!-- Card 2 -->
        <div class="card-bay" data-step="2">
          <article class="uc-card" id="card2">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 02</span>
                <h3 class="uc-role">The Student &amp; Academic Researcher</h3>
              </div>
              <span class="uc-status-tag">48h Watchdog Auto-Decomposition</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item">
                  <span class="bullet-tag hurdle">Hurdle</span>
                  <p><strong>Blank-page thesis paralysis:</strong> Staring at a 40-page literature review for 5 days until panic sets in.</p>
                </div>
                <div class="uc-bullet-item">
                  <span class="bullet-tag fix">A* Route</span>
                  <p><strong>Automatic micro-step fracture:</strong> Inactive nodes fracture into 15-minute concrete tasks that restore immediate momentum.</p>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_stand_11.webp" alt="Student studying" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">+92% Momentum Restored · 0 Panic</span>
              <button class="album-btn scenario-launch-btn" data-scenario="thesis">Simulate Route</button>
            </div>
          </article>
        </div>

        <!-- Card 3 -->
        <div class="card-bay" data-step="3">
          <article class="uc-card" id="card3">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 03</span>
                <h3 class="uc-role">The Freelancer &amp; Agency Contractor</h3>
              </div>
              <span class="uc-status-tag">Cryptographic Proof of Work</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item">
                  <span class="bullet-tag hurdle">Hurdle</span>
                  <p><strong>Milestone disputes:</strong> Deliverables and sign-off dates lost across messy Slack threads and email chains.</p>
                </div>
                <div class="uc-bullet-item">
                  <span class="bullet-tag fix">A* Route</span>
                  <p><strong>Sui onchain proof stamp:</strong> Tatum gateway hashes completed deliverables directly to Sui Mainnet for verifiable proof.</p>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_stand_16.webp" alt="Freelancer presenting" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">Sui Mainnet Stamped · Irrefutable</span>
              <button class="album-btn scenario-launch-btn" data-scenario="agency">Simulate Route</button>
            </div>
          </article>
        </div>

        <!-- Card 4 -->
        <div class="card-bay" data-step="4">
          <article class="uc-card" id="card4">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 04</span>
                <h3 class="uc-role">The ADHD &amp; Overwhelmed Mind</h3>
              </div>
              <span class="uc-status-tag">Zero-Guilt Single Action Focus</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item">
                  <span class="bullet-tag hurdle">Hurdle</span>
                  <p><strong>To-do list freeze:</strong> 25 competing items cause overwhelm. Missing 2 days triggers shame and abandonment.</p>
                </div>
                <div class="uc-bullet-item">
                  <span class="bullet-tag fix">A* Route</span>
                  <p><strong>Single-step clarity:</strong> Hides future complexity and surfaces only the single highest-value action for today.</p>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_sit_6.webp" alt="Individual meditating" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">Zero-Shame Recalculation</span>
              <button class="album-btn scenario-launch-btn" data-scenario="adhd">Simulate Route</button>
            </div>
          </article>
        </div>

        <!-- Card 5 (Destination of Journey Path) -->
        <div class="card-bay" data-step="5">
          <article class="uc-card" id="card5">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 05</span>
                <h3 class="uc-role">The Cross-Platform Power User</h3>
              </div>
              <span class="uc-status-tag">Terminal, Browser, &amp; IDE Unity</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item">
                  <span class="bullet-tag hurdle">Hurdle</span>
                  <p><strong>Over-training collapse:</strong> Rigid training schedules ignore fatigue, leading to injury and quitting week 3.</p>
                </div>
                <div class="uc-bullet-item">
                  <span class="bullet-tag fix">A* Route</span>
                  <p><strong>Unified portable memory:</strong> Portable context across terminal and web dynamically scales target load to match physical stamina.</p>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_stand_2.webp" alt="Athlete training" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">100% Finish Rate · Injury Prevented</span>
              <div class="card5-target-wrap">
                <div class="card5-target-ring" id="card5TargetRing"></div>
                <button class="album-btn primary-tape launch-btn" id="card5LaunchBtn">Launch GoalStar Now</button>
              </div>
            </div>
          </article>
        </div></div>

        <!-- Centered Destination Terminal (Middle X Position Underneath Last Card) -->
        <div class="journey-terminal" id="journeyTerminal">
          <div class="terminal-circle-target" id="terminalCircleTarget">
            <div class="terminal-core-circle"></div>
          </div>
          <span class="terminal-badge">Goal Reached · Mainnet Verified</span>
          <p class="terminal-sub">Dynamic A* Path Concluded</p>
        </div> </div>
    </section>
  </main>

  <!-- Interactive Scenario Simulation Walkthrough Modal (Progressive Reveal) -->
  <div class="scenario-modal" id="scenarioModal" hidden>
    <div class="scenario-modal-box">
      <button type="button" class="close-modal-btn" id="closeScenarioBtn" aria-label="Close">&times;</button>
      
      <div class="scenario-modal-head">
        <div class="scenario-step-indicator">
          <div class="step-pill active" id="sp1"></div>
          <div class="step-pill" id="sp2"></div>
          <div class="step-pill" id="sp3"></div>
          <div class="step-pill" id="sp4"></div>
          <div class="step-pill" id="sp5"></div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span id="scenarioStepNum" style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent);">PART 1 OF 5</span>
          <span id="scenarioScenarioTag" style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:700; color:var(--ink-muted);">SCENARIO SIMULATION</span>
        </div>
        <h3 id="scenarioStepTitle" style="font-family:'Playfair Display', serif; font-size:22px; margin:4px 0 0; color:var(--ink);">Where You Are: Grounding the Goal</h3>
      </div>

      <div class="scenario-stage-content" id="scenarioStageContent">
        <!-- Injected dynamically per step -->
      </div>

      <div class="scenario-modal-actions">
        <button type="button" class="album-btn secondary-tape" id="prevScenarioStepBtn">Previous</button>
        <div style="display:flex; gap:8px;">
          <button type="button" class="album-btn primary-tape" id="nextScenarioStepBtn">Next Part</button>
          <button type="button" class="album-btn secondary-tape" id="openFullPlannerBtn">Open in Planner</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Login Modal Dialog (Clean SVG, No Emojis) -->
  <div class="login-dialog" id="loginDialog" hidden>
    <div class="login-box">
      <button type="button" class="close-modal-btn" id="closeLoginDlg" aria-label="Close">&times;</button>
      <div class="modal-head">
        <h3>Connect &amp; Sync Portable Memory</h3>
        <p class="muted small" style="margin: 0; color: var(--ink-muted); font-size: 13px;">Save your personal stamina, friction patterns, and onchain milestone proofs across sessions.</p>
      </div>

      <div class="login-opts">
        <button type="button" class="login-opt-btn" id="loginGuestBtn">
          <svg class="opt-icon-svg" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
          <div>
            <div class="opt-label">Instant Guest Mode</div>
            <div class="opt-desc">Zero friction. Starts right now in this browser session.</div>
          </div>
        </button>

        <button type="button" class="login-opt-btn" id="loginSuiBtn">
          <svg class="opt-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M2 12c2.5-3 5-3 7.5 0s5 3 7.5 0 5-3 7 0M2 18c2.5-3 5-3 7.5 0s5 3 7.5 0 5-3 7 0"/>
          </svg>
          <div>
            <div class="opt-label">Sui Web3 Wallet</div>
            <div class="opt-desc">Connect Sui address via Tatum RPC Gateway on Mainnet.</div>
          </div>
        </button>

        <button type="button" class="login-opt-btn" id="loginWalrusBtn">
          <svg class="opt-icon-svg" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="5"/><circle cx="5" cy="8" r="2.5"/><circle cx="19" cy="8" r="2.5"/><circle cx="8" cy="19" r="2"/><circle cx="16" cy="19" r="2"/>
          </svg>
          <div>
            <div class="opt-label">Walrus Memory Direct</div>
            <div class="opt-desc">Decentralized memory stored on Walrus Mainnet.</div>
          </div>
        </button>
      </div>
    </div>
  </div>

  <!-- Walkthrough Tour Modal (Clean SVG, No Emojis) -->
  <div class="home-tour-modal" id="homeTourModal" hidden>
    <div class="home-tour-content">
      <button id="closeHomeTourBtn" class="close-modal-btn" aria-label="Close">&times;</button>
      <div class="modal-head">
        <span id="homeTourStepCount" style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent);">Step 1 of 4</span>
        <h3 id="homeTourTitle" style="margin-top:4px;">How GoalStar Works</h3>
      </div>
      <div id="homeTourBody" style="font-size:15px; line-height:1.6; color:var(--ink-soft); min-height:90px;"></div>
      <div class="home-tour-actions">
        <button id="prevHomeTourBtn" class="album-btn secondary-tape">Previous</button>
        <button id="nextHomeTourBtn" class="album-btn primary-tape">Next Step</button>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="landing-footer">
    <div class="footer-content">
      <div class="footer-brand">GoalStar Total Recall Edition</div>
      <p style="margin: 0; line-height: 1.6;">
        A* Pathfinding for Human Goals · Powered by Walrus Memory on Mainnet &amp; Tatum Sui RPC Gateway.
      </p>
    </div>
  </footer>

  <!-- SCRIPT ENGINE -->
  <script type="module">
    import { sound } from './js/sound.js';
    import { theme } from './js/theme.js';
    import { auth } from './js/auth.js';

    // Initialize core services
    theme.init();
    sound.attachListeners();
    auth.init();

    // Launch action
    function launchPlanner() {
      sound.play('click');
      if (!auth.isLoggedIn()) {
        auth.connectGuest();
      }
      setTimeout(() => {
        window.location.href = '/';
      }, 50);
    }

    document.querySelectorAll('#launchPlannerTopBtn, #heroLaunchBtn, #card5LaunchBtn, #navLaunchApp').forEach(b => {
      b.addEventListener('click', launchPlanner);
    });

    // ---------------------------------------------------------
    // LIVE SIMULATOR LOGIC
    // ---------------------------------------------------------
    const slider = document.getElementById('frictionSlider');
    const sliderFillTrack = document.getElementById('sliderFillTrack');
    const staminaLabel = document.getElementById('staminaLabel');
    const monolith = document.getElementById('simNodeMonolith');
    const serverless = document.getElementById('simNodeServerless');
    const feedback = document.getElementById('simFeedback');

    function updateSim() {
      const val = parseInt(slider.value, 10);
      if (sliderFillTrack) sliderFillTrack.style.width = `${val * 10}%`;

      if (val >= 6) {
        staminaLabel.textContent = `HIGH (${val}/10)`;
        monolith.className = 'sim-node mid active-path';
        serverless.className = 'sim-node mid';
        feedback.innerHTML = '<b>Green Path Selected:</b> Monolith setup is optimal when stamina is high. Drag slider down to simulate fatigue!';
      } else {
        staminaLabel.textContent = `LOW (${val}/10)`;
        monolith.className = 'sim-node mid blocked-path';
        serverless.className = 'sim-node mid active-path';
        feedback.innerHTML = '<b>A* Path Rerouted:</b> High friction detected on monolith! Route shifted to <b>Serverless &amp; Micro-Tasks</b> for lowest activation energy.';
      }
    }

    slider.addEventListener('input', () => {
      sound.play('crunch');
      updateSim();
    });

    // ---------------------------------------------------------
    // UNIVERSAL SCROLL ANIMATION & PRECISION TRAVELING ARROW
    // ---------------------------------------------------------
    const bgHumaaans = [
      { id: 'bgHu1', top: 140, factor: 0.12, baseRot: -4 },
      { id: 'bgHu2', top: 760, factor: -0.10, baseRot: 5 },
      { id: 'bgHu3', top: 1480, factor: 0.14, baseRot: -3 },
      { id: 'bgHu4', top: 2200, factor: -0.12, baseRot: 4 },
      { id: 'bgHu5', top: 2880, factor: 0.11, baseRot: -5 },
    ];

    const heroPhoto = document.getElementById('heroPhoto');
    const heroLeft = document.getElementById('heroLeft');
    const inkSwashSvg = document.getElementById('inkSwashSvg');
    const simCard = document.getElementById('simCard');
    const cards = [
      { el: document.getElementById('card1'), baseTilt: -1.8 },
      { el: document.getElementById('card2'), baseTilt: 2.0 },
      { el: document.getElementById('card3'), baseTilt: -1.5 },
      { el: document.getElementById('card4'), baseTilt: 2.2 },
      { el: document.getElementById('card5'), baseTilt: -1.2 },
    ];

    const bays = document.querySelectorAll('.card-bay');
    const svgPath = document.getElementById('journeySvgPath');
    const activePath = document.getElementById('journeyActivePath');
    const travelingArrow = document.getElementById('travelingArrow');
    const hudSteps = document.querySelectorAll('.hud-step');

    let totalPathLength = 0;
    let ticking = false;

    function buildConnectorPath() {
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
    }

    function animateOnScroll() {
      const scrollY = window.scrollY;
      const winH = window.innerHeight;

      // 1. Hero Left Parallax & Ink Swash Draw-In
      if (heroLeft) {
        heroLeft.style.transform = `translate3d(0, ${Math.min(36, scrollY * 0.1)}px, 0)`;
      }
      if (inkSwashSvg) {
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
      }

      // 2. Hanging Polaroid Card: CALM, SMOOTH GLIDE TO SETTLED DOCKED POINT (ZERO JITTER)
      if (heroPhoto) {
        const heroProgress = Math.min(1, Math.max(0, scrollY / 420));
        const heroY = heroProgress * 32;
        const heroRot = -1.8 + heroProgress * 1.8; // smoothly straightens to 0deg
        const heroScale = 1.0 - heroProgress * 0.02;
        heroPhoto.style.transform = `translate3d(0, ${heroY.toFixed(1)}px, 0) rotate(${heroRot.toFixed(2)}deg) scale(${heroScale.toFixed(3)})`;
      }

      // 3. Live Simulator Card: Calm Perspective Dock-In
      if (simCard) {
        const simRect = simCard.getBoundingClientRect();
        const simDistFromCenter = simRect.top + simRect.height / 2 - winH / 2;
        const simProgress = Math.max(0, Math.min(1, 1 - Math.abs(simDistFromCenter) / (winH * 0.85)));
        const simTilt = (simDistFromCenter / winH) * 4;
        const simScale = 0.95 + 0.05 * simProgress;
        simCard.style.transform = `perspective(1000px) rotateX(${simTilt.toFixed(2)}deg) scale(${simScale.toFixed(3)})`;
      }

      // 4. Background Humaaans Figures (Smooth Linear Parallax, No Erratic Sine Waves)
      bgHumaaans.forEach(h => {
        const el = document.getElementById(h.id);
        if (!el) return;

        const dist = scrollY - h.top + winH * 0.5;
        const ty = dist * h.factor;
        const progress = Math.max(0, Math.min(1, 1 - Math.abs(dist) / (winH * 0.9)));
        const scale = 0.88 + 0.22 * progress;

        const isMobile = window.innerWidth < 768;
        const baseOpacity = isMobile ? 0.11 : (document.body.dataset.paper === 'night' ? 0.16 : 0.22);
        const opacity = baseOpacity * (0.6 + 0.4 * progress);

        el.style.transform = `translate3d(0, ${ty.toFixed(1)}px, 0) scale(${scale.toFixed(2)}) rotate(${h.baseRot}deg)`;
        el.style.opacity = opacity.toFixed(2);
      });

      // 4.5. "Engineered to Overcome" Section Header Box: Fade In & Zoom In (from bigger size scale 1.20 to og size 1.0 in og pos)
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
      });

      // 6. Precision Traveling Arrow & Active Green Path (Meets Exact Point at the End)
      const track = document.getElementById('journeyTrack');
      if (track && svgPath && travelingArrow && window.innerWidth >= 640) {
        const tr = track.getBoundingClientRect();
        const pathLen = totalPathLength || svgPath.getTotalLength();
        if (pathLen > 0) {
          const card1El = document.getElementById('card1');
          const card5El = document.getElementById('card5');
          const endBtn = document.getElementById('card5LaunchBtn') || card5El;
          const terminalTarget = document.getElementById('terminalCircleTarget');
          const c1r = card1El ? card1El.getBoundingClientRect() : tr;
          const er = endBtn ? endBtn.getBoundingClientRect() : tr;
          const ter = terminalTarget ? terminalTarget.getBoundingClientRect() : er;

          // Track journey: from Card 1 all the way down to centered terminal
          const startScrollY = window.scrollY + c1r.top - winH * 0.65;
          const endScrollY = window.scrollY + ter.top - winH * 0.65;
          let progress = 0;
          if (endScrollY > startScrollY) {
            progress = Math.max(0, Math.min(1, (window.scrollY - startScrollY) / (endScrollY - startScrollY)));
          }
          if (ter.top <= winH * 0.8) {
            // Once the terminal target is comfortably on screen, guarantee it snaps to 100%
            const snapProgress = Math.min(1, Math.max(0, 1 - (ter.top - winH * 0.55) / (winH * 0.25)));
            progress = Math.max(progress, snapProgress);
          }
          if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 50) {
            progress = 1.0;
          }

          const currentLen = progress * pathLen;
          if (activePath) {
            activePath.style.strokeDasharray = `${currentLen} ${pathLen}`;
            activePath.style.strokeDashoffset = '0';
          }

          const pt = svgPath.getPointAtLength(currentLen);
          travelingArrow.style.left = `${pt.x}px`;
          travelingArrow.style.top = `${pt.y}px`;

          // TURN INTO A CIRCLE IN THE MIDDLE X POSITION AT THE BOTTOM
          if (progress >= 0.92) {
            travelingArrow.classList.add('is-circle');
            travelingArrow.style.transform = `translate(-50%, -50%) scale(1.18)`;
            if (terminalTarget) terminalTarget.classList.add('arrived');
          } else {
            travelingArrow.classList.remove('is-circle');
            if (terminalTarget) terminalTarget.classList.remove('arrived');
            const pBefore = svgPath.getPointAtLength(Math.max(0, currentLen - 2));
            const pAfter = svgPath.getPointAtLength(Math.min(pathLen, currentLen + 2));
            const angle = Math.atan2(pAfter.y - pBefore.y, pAfter.x - pBefore.x) * (180 / Math.PI);
            travelingArrow.style.transform = `translate(-50%, -50%) rotate(${angle + 90}deg)`;
          }

          // Highlight target arrival ring at Card 5
          const targetRing = document.getElementById('card5TargetRing');
          if (targetRing) {
            targetRing.style.opacity = progress >= 0.82 ? '1' : '0';
          }
        }
      }

      // 7. HUD Active Step Highlight
      bays.forEach((bay, idx) => {
        const rect = bay.getBoundingClientRect();
        if (rect.top < winH * 0.6 && rect.bottom > winH * 0.3) {
          hudSteps.forEach(h => h.classList.remove('active'));
          if (hudSteps[idx]) hudSteps[idx].classList.add('active');
        }
      });

      ticking = false;
    }

    function requestScrollUpdate() {
      if (!ticking) {
        window.requestAnimationFrame(animateOnScroll);
        ticking = true;
      }
    }

    window.addEventListener('scroll', requestScrollUpdate, { passive: true });
    window.addEventListener('resize', () => {
      buildConnectorPath();
      requestScrollUpdate();
    });

    // Initial positioning
    setTimeout(() => {
      buildConnectorPath();
      requestScrollUpdate();
      updateSim();
    }, 100);

    // ---------------------------------------------------------
    // PROGRESSIVE SCENARIO SIMULATION WALKTHROUGH ENGINE
    // ---------------------------------------------------------
    const scenarioData = {
      saas: {
        title: 'The Indie Hacker: Infrastructure Fatigue Rerouting',
        stages: [
          {
            part: 1,
            title: 'Where You Are: Prototype Idea Ready',
            html: `
              <div class="scenario-card-preview">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent); margin-bottom:4px;">INITIAL STATE</div>
                <div style="font-size:16px; font-weight:700;">Now: Prototype Idea Ready</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">Solo founder with a validated product concept. Energy is high, but infrastructure decisions loom.</p>
              </div>
              <p style="font-size:14px; color:var(--ink-soft); line-height:1.5;">GoalStar starts from where you stand right now. No blank-page dread.</p>
            `
          },
          {
            part: 2,
            title: 'Walrus Memory Detects Friction Trap',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--red);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--red); margin-bottom:4px;">RECURRING BLOCKER DETECTED</div>
                <div style="font-size:15px; font-weight:700;">Monolith Docker &amp; Kubernetes Setup (14 Days)</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">Walrus Memory identifies past history: user under-estimates DevOps config by 45%, leading to artificial deadline stress and abandoned launches.</p>
              </div>
              <div class="scenario-route-diagram">
                <div class="scenario-node-box">Idea Ready</div>
                <div style="color:var(--red); font-weight:900;">&rarr;</div>
                <div class="scenario-node-box hurdle-node">+3.5 Friction Penalty</div>
              </div>
            `
          },
          {
            part: 3,
            title: 'A* Engine Reroutes to Lowest Resistance Path',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--green);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--green); margin-bottom:4px;">A* DYNAMIC SOLUTION</div>
                <div style="font-size:15px; font-weight:700;">Deploy to Managed Cloud / PaaS (Low Friction)</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">The graph bypasses Kubernetes entirely. Shifting to serverless eliminates 12 days of setup fatigue and targets a live launch in 48 hours.</p>
              </div>
              <div class="scenario-route-diagram">
                <div class="scenario-node-box">Idea Ready</div>
                <div style="color:var(--green); font-weight:900;">&rarr;</div>
                <div class="scenario-node-box highlight">PaaS / Serverless (Optimal)</div>
              </div>
            `
          },
          {
            part: 4,
            title: 'Path Profile & Cost Breakdown',
            html: `
              <div class="scenario-card-preview">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <span style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--ink);">COST PER STEP</span>
                  <span style="font-size:11px; color:var(--green); font-weight:700;">TIMELINE: 2 DAYS</span>
                </div>
                <div class="mini-chart-bars">
                  <div class="mini-bar-col">
                    <div class="mini-bar bar-time" style="height: 35%;"></div>
                    <span style="font-size:9.5px; font-weight:700; color:var(--ink-muted);">Time</span>
                  </div>
                  <div class="mini-bar-col">
                    <div class="mini-bar bar-money" style="height: 25%;"></div>
                    <span style="font-size:9.5px; font-weight:700; color:var(--ink-muted);">Money</span>
                  </div>
                  <div class="mini-bar-col">
                    <div class="mini-bar bar-effort" style="height: 40%;"></div>
                    <span style="font-size:9.5px; font-weight:700; color:var(--ink-muted);">Effort</span>
                  </div>
                  <div class="mini-bar-col">
                    <div class="mini-bar bar-risk" style="height: 18%;"></div>
                    <span style="font-size:9.5px; font-weight:700; color:var(--ink-muted);">Risk</span>
                  </div>
                </div>
                <div style="font-size:12px; color:var(--ink-muted); text-align:center;">Effort and Risk dropped by 70% compared to monolithic route.</div>
              </div>
            `
          },
          {
            part: 5,
            title: 'Irrefutable Cryptographic Proof Stamped on Sui',
            html: `
              <div class="sui-verified-box">
                <div class="sui-head-row">
                  <span>Verified on Sui Mainnet</span>
                  <span class="sui-badge-pill">Sui</span>
                </div>
                <div class="sui-details-row">
                  <div>Checkpoint: <strong>#64129830</strong></div>
                  <div>Digest: <code>0x4eeff773a393e726774674797865208394655620</code></div>
                </div>
              </div>
              <p style="font-size:13.5px; color:var(--ink-soft); margin-top:10px; line-height:1.5;">When tasks complete, Tatum Gateway records the deliverable on Sui Mainnet, creating permanent proof for investors, peers, or grants.</p>
            `
          }
        ]
      },
      thesis: {
        title: 'The Researcher: 48h Watchdog Auto-Decomposition',
        stages: [
          {
            part: 1,
            title: 'Where You Are: Blank-Page Thesis Stagnation',
            html: `<div class="scenario-card-preview"><div style="font-size:15px; font-weight:700;">Current State: 40-Page Literature Review Pending</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Stuck on the overview chapter for 5 days. High cognitive overload.</p></div>`
          },
          {
            part: 2,
            title: '48-Hour Watchdog Triggers Automatic Fracture',
            html: `<div class="scenario-card-preview" style="border-left:3px solid var(--accent);"><div style="font-size:15px; font-weight:700;">Task Inactive &gt; 48 Hours</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">GoalStar watchdog detects stall and fractures the monolith paper into three 15-minute micro-tasks.</p></div>`
          },
          {
            part: 3,
            title: 'Micro-Checklist Velocity Restored',
            html: `<div class="scenario-card-preview" style="border-left:3px solid var(--green);"><div style="font-size:15px; font-weight:700;">92% Momentum Restored</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Writing 250 words per sub-step restores confidence without triggering perfectionist anxiety.</p></div>`
          },
          {
            part: 4,
            title: 'Cost Profile: Effort Distributed',
            html: `<div class="scenario-card-preview"><div style="font-size:14px; font-weight:700; color:var(--green);">Fatigue Penalty Nullified</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Time is preserved; stamina recovery happens between micro-sprints.</p></div>`
          },
          {
            part: 5,
            title: 'Draft Milestone Stamped on Sui',
            html: `<div class="sui-verified-box"><div class="sui-head-row"><span>Chapter 1 Verified on Sui</span><span class="sui-badge-pill">Sui</span></div><div class="sui-details-row">Checkpoint: <strong>#64129845</strong><br>Digest: <code>0x8f2a...c31b</code></div></div>`
          }
        ]
      },
      agency: {
        title: 'The Contractor: Cryptographic Proof of Work',
        stages: [
          {
            part: 1,
            title: 'Where You Are: Milestone Hand-Off in Dispute',
            html: `<div class="scenario-card-preview"><div style="font-size:15px; font-weight:700;">Milestone 2 Completed, Sign-off Pending</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Deliverables spread across messy email chains and Slack DMs.</p></div>`
          },
          {
            part: 2,
            title: 'Walrus Memory Tracks Historical Scope Creep',
            html: `<div class="scenario-card-preview" style="border-left:3px solid var(--red);"><div style="font-size:15px; font-weight:700;">Scope Dispute Risk Detected</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Memory identifies past client revisions averaging 3 additional rounds.</p></div>`
          },
          {
            part: 3,
            title: 'Sui Onchain Proof Generation',
            html: `<div class="scenario-card-preview" style="border-left:3px solid var(--green);"><div style="font-size:15px; font-weight:700;">Instant Immutable Delivery Hash</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Code and designs are digested into an irrefutable Sui transaction hash.</p></div>`
          },
          {
            part: 4,
            title: 'Risk Profile Eliminated',
            html: `<div class="scenario-card-preview"><div style="font-size:14px; font-weight:700; color:var(--green);">Zero Dispute Overhead</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Both parties have cryptographic proof of exact delivery timestamp.</p></div>`
          },
          {
            part: 5,
            title: 'Proof Stamped on Sui Mainnet',
            html: `<div class="sui-verified-box"><div class="sui-head-row"><span>Milestone Stamped</span><span class="sui-badge-pill">Sui</span></div><div class="sui-details-row">Checkpoint: <strong>#64129890</strong><br>Digest: <code>0xbc91...77fa</code></div></div>`
          }
        ]
      },
      adhd: {
        title: 'The ADHD Mind: Zero-Guilt Single Action Focus',
        stages: [
          {
            part: 1,
            title: 'Where You Are: 25-Task Overwhelm Freeze',
            html: `<div class="scenario-card-preview"><div style="font-size:15px; font-weight:700;">25 Competing To-Do Items</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Too many choices cause complete cognitive stall and task avoidance.</p></div>`
          },
          {
            part: 2,
            title: 'Walrus Memory Bypasses Guilt Traps',
            html: `<div class="scenario-card-preview" style="border-left:3px solid var(--accent);"><div style="font-size:15px; font-weight:700;">Zero-Shame Recalculation</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Missed 3 days? GoalStar resets your friction metrics without judgment.</p></div>`
          },
          {
            part: 3,
            title: 'Single Next Action Isolated',
            html: `<div class="scenario-card-preview" style="border-left:3px solid var(--green);"><div style="font-size:15px; font-weight:700;">Immediate Focus: Send One Email</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Future complexity is hidden from view until the single step completes.</p></div>`
          },
          {
            part: 4,
            title: 'Effort Metric Minimized',
            html: `<div class="scenario-card-preview"><div style="font-size:14px; font-weight:700; color:var(--green);">Activation Energy: 1/5</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Micro-barriers cleared. Action begins immediately.</p></div>`
          },
          {
            part: 5,
            title: 'Progress Stamped on Sui',
            html: `<div class="sui-verified-box"><div class="sui-head-row"><span>Momentum Proof on Sui</span><span class="sui-badge-pill">Sui</span></div><div class="sui-details-row">Checkpoint: <strong>#64129910</strong><br>Digest: <code>0x112b...ee34</code></div></div>`
          }
        ]
      }
    };

    let activeScenarioKey = 'saas';
    let currentScenarioStep = 0;

    const scenarioModal = document.getElementById('scenarioModal');
    const scenarioStepNum = document.getElementById('scenarioStepNum');
    const scenarioScenarioTag = document.getElementById('scenarioScenarioTag');
    const scenarioStepTitle = document.getElementById('scenarioStepTitle');
    const scenarioStageContent = document.getElementById('scenarioStageContent');
    const prevScenarioStepBtn = document.getElementById('prevScenarioStepBtn');
    const nextScenarioStepBtn = document.getElementById('nextScenarioStepBtn');
    const openFullPlannerBtn = document.getElementById('openFullPlannerBtn');
    const stepPills = [
      document.getElementById('sp1'),
      document.getElementById('sp2'),
      document.getElementById('sp3'),
      document.getElementById('sp4'),
      document.getElementById('sp5')
    ];

    function renderScenarioStage() {
      const scenario = scenarioData[activeScenarioKey] || scenarioData['saas'];
      const stage = scenario.stages[currentScenarioStep];

      scenarioStepNum.textContent = `PART ${stage.part} OF 5`;
      scenarioScenarioTag.textContent = scenario.title.split(':')[0].toUpperCase();
      scenarioStepTitle.textContent = stage.title;
      scenarioStageContent.innerHTML = stage.html;

      stepPills.forEach((pill, idx) => {
        pill.className = 'step-pill';
        if (idx < currentScenarioStep) pill.classList.add('passed');
        if (idx === currentScenarioStep) pill.classList.add('active');
      });

      prevScenarioStepBtn.disabled = currentScenarioStep === 0;
      nextScenarioStepBtn.textContent = currentScenarioStep === scenario.stages.length - 1 ? 'Finish Walkthrough' : 'Next Part';
    }

    document.querySelectorAll('.scenario-launch-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        sound.play('pop');
        const sc = btn.getAttribute('data-scenario') || 'saas';
        activeScenarioKey = sc;
        currentScenarioStep = 0;
        renderScenarioStage();
        scenarioModal.hidden = false;
      });
    });

    document.getElementById('closeScenarioBtn')?.addEventListener('click', () => {
      sound.play('click');
      scenarioModal.hidden = true;
    });

    prevScenarioStepBtn?.addEventListener('click', () => {
      if (currentScenarioStep > 0) {
        sound.play('whoosh');
        currentScenarioStep--;
        renderScenarioStage();
      }
    });

    nextScenarioStepBtn?.addEventListener('click', () => {
      sound.play('whoosh');
      const scenario = scenarioData[activeScenarioKey] || scenarioData['saas'];
      if (currentScenarioStep < scenario.stages.length - 1) {
        currentScenarioStep++;
        renderScenarioStage();
      } else {
        scenarioModal.hidden = true;
        launchPlanner();
      }
    });

    openFullPlannerBtn?.addEventListener('click', () => {
      scenarioModal.hidden = true;
      launchPlanner();
    });

    // Quick Home Walkthrough Modal
    const tourSteps = [
      {
        title: '1. Portable Memory',
        body: 'Remembers your personal friction, stamina, and past progress across sessions.'
      },
      {
        title: '2. AI Roadmap',
        body: 'Dreams intermediate milestones between where you are and where you want to be.'
      },
      {
        title: '3. Dynamic A* Route',
        body: 'Calculates the lowest-friction path and reroutes around blockers in real time.'
      },
      {
        title: '4. Verifiable Sui Proof',
        body: 'Stamps finished milestones on Sui Mainnet with immutable cryptographic proof.'
      }
    ];

    let currentHomeStep = 0;
    const tourModal = document.getElementById('homeTourModal');
    const tourTitle = document.getElementById('homeTourTitle');
    const tourBody = document.getElementById('homeTourBody');
    const tourCount = document.getElementById('homeTourStepCount');

    function renderHomeTour() {
      const step = tourSteps[currentHomeStep];
      tourTitle.textContent = step.title;
      tourBody.innerHTML = step.body;
      tourCount.textContent = `Step ${currentHomeStep + 1} of ${tourSteps.length}`;
      document.getElementById('prevHomeTourBtn').disabled = currentHomeStep === 0;
      document.getElementById('nextHomeTourBtn').textContent = currentHomeStep === tourSteps.length - 1 ? 'Finish Tour' : 'Next Step';
    }

    function stopHomeTourBounce() {
      try { localStorage.setItem('goalstar_tour_clicked', 'true'); } catch(e) {}
      document.querySelectorAll('.tour-bounce-btn').forEach(b => b.classList.remove('tour-bounce-btn'));
    }
    if (localStorage.getItem('goalstar_tour_clicked') === 'true' || localStorage.getItem('goalstar_walkthrough_completed') === 'true') {
      stopHomeTourBounce();
    }

    document.querySelectorAll('#heroTourBtn, #navTourBtn').forEach(btn => {
      btn.addEventListener('click', () => {
        stopHomeTourBounce();
        sound.play('pop');
        currentHomeStep = 0;
        renderHomeTour();
        tourModal.hidden = false;
      });
    });

    document.getElementById('closeHomeTourBtn')?.addEventListener('click', () => {
      sound.play('click');
      tourModal.hidden = true;
    });

    document.getElementById('prevHomeTourBtn')?.addEventListener('click', () => {
      if (currentHomeStep > 0) {
        sound.play('whoosh');
        currentHomeStep--;
        renderHomeTour();
      }
    });

    document.getElementById('nextHomeTourBtn')?.addEventListener('click', () => {
      sound.play('whoosh');
      if (currentHomeStep < tourSteps.length - 1) {
        currentHomeStep++;
        renderHomeTour();
      } else {
        tourModal.hidden = true;
        launchPlanner();
      }
    });

    // Login modal handling
    const loginDlg = document.getElementById('loginDialog');
    document.getElementById('loginBtn')?.addEventListener('click', () => {
      sound.play('pop');
      loginDlg.hidden = false;
    });
    document.getElementById('closeLoginDlg')?.addEventListener('click', () => {
      sound.play('click');
      loginDlg.hidden = true;
    });
    document.getElementById('loginGuestBtn')?.addEventListener('click', () => {
      auth.connectGuest();
      loginDlg.hidden = true;
      sound.play('ding');
      launchPlanner();
    });
    document.getElementById('loginSuiBtn')?.addEventListener('click', () => {
      auth.connectSui();
      loginDlg.hidden = true;
      sound.play('ding');
      launchPlanner();
    });
    document.getElementById('loginWalrusBtn')?.addEventListener('click', () => {
      auth.connectWalrus();
      loginDlg.hidden = true;
      sound.play('ding');
      launchPlanner();
    });
  </script>
</body>
</html>
'''

with open('goalstar-recall/home.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated enhanced home.html successfully! Length: {len(html_content)} bytes")
