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
      --red: #dc2626;
      --washi-light: rgba(245, 222, 179, 0.88);
      --card-shadow: 0 10px 24px rgba(0, 0, 0, 0.08), 0 2px 6px rgba(0, 0, 0, 0.04);
      --card-border: 1.5px solid rgba(42, 45, 62, 0.16);
    }

    body[data-paper='night'] {
      --paper: #0b111e;
      --paper-warm: #0f172a;
      --panel: #151e2e;
      --panel-card: #1a2436;
      --ink: #f1f5f9;
      --ink-soft: #cbd5e1;
      --ink-muted: #94a3b8;
      --accent: #f59e0b;
      --accent-hover: #d97706;
      --green: #10b981;
      --red: #ef4444;
      --washi-light: rgba(245, 158, 11, 0.28);
      --card-shadow: 0 14px 32px rgba(0, 0, 0, 0.55), 0 3px 8px rgba(0, 0, 0, 0.4);
      --card-border: 1.5px solid rgba(245, 158, 11, 0.25);
    }

    html {
      scroll-behavior: smooth;
    }

    body.landing-body {
      margin: 0;
      padding: 0;
      background-color: var(--paper);
      color: var(--ink);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      overflow-x: hidden;
      position: relative;
      min-height: 100vh;
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
        opacity: 0.11; /* subtle watermark on mobile so text readability remains 100% crisp */
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
      transition: opacity 0.2s, color 0.2s;
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
    .landing-main {
      position: relative;
      z-index: 1;
      max-width: 1200px;
      margin: 0 auto;
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
      will-change: transform;
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
    }

    body[data-paper='night'] .sim-slider-box {
      background: #0f172a;
      border-color: rgba(245, 158, 11, 0.35);
    }

    .sim-slider-box input[type="range"] {
      cursor: pointer;
      accent-color: var(--accent);
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
      gap: 48px;
    }

    .card-bay {
      position: relative;
      width: 100%;
    }

    .uc-card {
      background: var(--panel-card);
      border: var(--card-border);
      border-radius: 4px;
      padding: 22px 28px;
      box-shadow: var(--card-shadow);
      position: relative;
      will-change: transform;
      box-sizing: border-box;
      transition: box-shadow 0.25s ease;
    }

    .uc-card:hover {
      box-shadow: 0 18px 36px rgba(0, 0, 0, 0.14);
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
      gap: 12px;
    }

    .uc-bullet-item {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      font-size: 15px;
      line-height: 1.5;
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
    }

    /* SVG Connector Line & Kinetic Traveling Arrow */
    .journey-svg-track {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
      overflow: visible;
    }

    .traveling-arrow {
      position: absolute;
      width: 24px;
      height: 24px;
      z-index: 5;
      pointer-events: none;
      transition: transform 0.1s linear;
      transform: translate(-50%, -50%);
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
    }

    @media (max-width: 420px) {
      #launchPlannerTopBtn {
        display: none; /* Already prominent in hero and card CTAs */
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
       MODALS: CLEAN & ACCESSIBLE (ZERO EMOJIS)
       ---------------------------------------------------- */
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

  <!-- 5 Background Parallax Humaaans Figures with Universal Scroll Animation -->
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
      <a href="javascript:void(0)" id="navTourBtn">Walkthrough</a>
      <a href="javascript:void(0)" id="navLaunchApp">Open App</a>
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
        <div class="hero-badge">WALRUS MAINNET MEMORY · TATUM SUI RPC</div>
        <h1 class="hero-title">
          A* Pathfinding for Life Goals, Backed by 
          <span class="ink-hl-wrap">
            <span class="ink-hl-text">Portable Memory</span>
            <svg class="ink-swash-svg" id="inkSwashSvg" viewBox="0 0 310 28" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
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
          <button id="heroLaunchBtn" class="album-btn primary-tape" style="font-size: 17px; padding: 11px 26px;">Open Interactive Planner</button>
          <a href="#simulator" class="album-btn secondary-tape" style="font-size: 15px;">Try A* In Browser</a>
          <button id="heroTourBtn" class="album-btn secondary-tape" style="font-size: 15px;">Walkthrough Tour</button>
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
              <svg class="photo-constellation-svg" viewBox="0 0 240 180" aria-hidden="true">
                <line x1="40" y1="130" x2="110" y2="70" stroke="#059669" stroke-width="2.5" stroke-dasharray="3 3" />
                <line x1="110" y1="70" x2="185" y2="40" stroke="#059669" stroke-width="3" />
                <circle cx="40" cy="130" r="7" fill="#059669" stroke="#1e293b" stroke-width="2" />
                <circle cx="110" cy="70" r="8" fill="#059669" stroke="#1e293b" stroke-width="2" />
                <polygon points="185,26 190,38 203,39 193,48 196,61 185,54 174,61 177,48 167,39 180,38" fill="#f59e0b" stroke="#1e293b" stroke-width="2" />
              </svg>
            </div>
            <!-- Polaroid Chin with Handwritten Annotation -->
            <div class="polaroid-chin">
              <span class="polaroid-handwriting">"The shortest path between where you are and where you want to be."</span>
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
          <h3>Try Dynamic A* Rerouting Live:</h3>
          <div class="sim-slider-box">
            <label for="frictionSlider" style="font-weight: 700; font-size: 14px;">Current Stamina:</label>
            <input type="range" id="frictionSlider" min="1" max="10" value="8" title="Drag slider to test stamina adaptation">
            <span id="staminaLabel" style="font-weight: 800; width: 95px; font-family:'Space Grotesk', monospace; font-size:13px;">HIGH (8/10)</span>
          </div>
        </div>

        <div class="sim-canvas">
          <div class="sim-node start">
            Start<br><small>Idea Conceived</small>
          </div>

          <div id="simNodeMonolith" class="sim-node mid active-path">
            Monolith &amp; K8s<br><small id="monolithCost">Fast if stamina &ge; 6</small>
          </div>

          <div id="simNodeServerless" class="sim-node mid">
            Serverless &amp; Micro-Tasks<br><small id="serverlessCost">Lowest friction route</small>
          </div>

          <div class="sim-node goal">
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
      <div class="sec-header">
        <span class="sec-tag">Tested Across High-Stakes Scenarios</span>
        <h2 class="sec-title">Engineered to Overcome Human Friction</h2>
        <p class="sec-desc">Real workflows where willpower fails and dynamic A* pathfinding keeps you moving forward.</p>
      </div>

      <div class="journey-track" id="journeyTrack">
        <!-- SVG Track for Traveling Kinetic Arrow (Desktop) -->
        <svg class="journey-svg-track" id="journeySvgTrack" viewBox="0 0 980 1800" preserveAspectRatio="none">
          <path id="journeySvgPath" d="" fill="none" stroke="rgba(42, 45, 62, 0.12)" stroke-width="3" stroke-dasharray="6 6"/>
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
              <button class="album-btn scenario-launch-btn" data-scenario="Launch SaaS">Simulate Route</button>
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
              <button class="album-btn scenario-launch-btn" data-scenario="Write Thesis">Simulate Route</button>
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
              <button class="album-btn scenario-launch-btn" data-scenario="Client Contract">Simulate Route</button>
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
              <button class="album-btn scenario-launch-btn" data-scenario="Focus Routine">Simulate Route</button>
            </div>
          </article>
        </div>

        <!-- Card 5 -->
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
              <button class="album-btn primary-tape launch-btn" id="card5LaunchBtn">Launch GoalStar Now</button>
            </div>
          </article>
        </div>
      </div>
    </section>
  </main>

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

    document.querySelectorAll('.scenario-launch-btn').forEach(b => {
      b.addEventListener('click', () => {
        launchPlanner();
      });
    });

    // ---------------------------------------------------------
    // LIVE SIMULATOR LOGIC
    // ---------------------------------------------------------
    const slider = document.getElementById('frictionSlider');
    const staminaLabel = document.getElementById('staminaLabel');
    const monolith = document.getElementById('simNodeMonolith');
    const serverless = document.getElementById('simNodeServerless');
    const feedback = document.getElementById('simFeedback');

    function updateSim() {
      const val = parseInt(slider.value, 10);
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
    // UNIVERSAL SCROLL-DRIVEN ANIMATION ENGINE
    // ---------------------------------------------------------
    const bgHumaaans = [
      { id: 'bgHu1', top: 140, factor: 0.14, baseRot: -4 },
      { id: 'bgHu2', top: 760, factor: -0.12, baseRot: 6 },
      { id: 'bgHu3', top: 1480, factor: 0.16, baseRot: -5 },
      { id: 'bgHu4', top: 2200, factor: -0.15, baseRot: 4 },
      { id: 'bgHu5', top: 2880, factor: 0.13, baseRot: -6 },
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

    let lastScrollY = window.scrollY;
    let scrollVelocity = 0;
    let ticking = false;

    function buildConnectorPath() {
      if (!svgPath || bays.length < 2 || window.innerWidth < 640) return;
      const track = document.getElementById('journeyTrack');
      if (!track) return;
      const trackRect = track.getBoundingClientRect();

      let d = '';
      const points = [];

      bays.forEach((bay, idx) => {
        const rect = bay.getBoundingClientRect();
        const x = (idx % 2 === 0) ? rect.left - trackRect.left + 50 : rect.right - trackRect.left - 50;
        const y = rect.top - trackRect.top + rect.height / 2;
        points.push({ x, y });

        if (idx === 0) {
          d += `M ${x} ${y}`;
        } else {
          const prev = points[idx - 1];
          const midY = (prev.y + y) / 2;
          d += ` C ${prev.x} ${midY}, ${x} ${midY}, ${x} ${y}`;
        }
      });

      svgPath.setAttribute('d', d);
      if (activePath) activePath.setAttribute('d', d);
    }

    function animateOnScroll() {
      const scrollY = window.scrollY;
      const winH = window.innerHeight;
      scrollVelocity = scrollY - lastScrollY;
      lastScrollY = scrollY;

      // 1. Hero Left Parallax & Ink Swash Scale
      if (heroLeft) {
        heroLeft.style.transform = `translate3d(0, ${Math.min(40, scrollY * 0.12)}px, 0)`;
      }
      if (inkSwashSvg) {
        const swashScale = 1 + Math.sin(scrollY * 0.015) * 0.03;
        inkSwashSvg.style.transform = `scaleX(${swashScale})`;
      }

      // 2. Hanging Polaroid Photo Album Card Swing (Pendulum Physics on Twine Clothesline)
      if (heroPhoto) {
        const naturalSway = Math.sin(scrollY * 0.007) * 3.5;
        const velocityKick = Math.max(-6, Math.min(6, scrollVelocity * 0.15));
        const swingAngle = -1.5 + naturalSway - velocityKick;
        const heroFloatY = Math.min(50, scrollY * 0.08);
        heroPhoto.style.transform = `translate3d(0, ${heroFloatY}px, 0) rotate(${swingAngle.toFixed(2)}deg)`;
      }

      // 3. Live Simulator Perspective Dock-In
      if (simCard) {
        const simRect = simCard.getBoundingClientRect();
        const simDistFromCenter = simRect.top + simRect.height / 2 - winH / 2;
        const simProgress = Math.max(0, Math.min(1, 1 - Math.abs(simDistFromCenter) / (winH * 0.8)));
        const simTilt = (simDistFromCenter / winH) * 5;
        const simScale = 0.94 + 0.06 * simProgress;
        simCard.style.transform = `perspective(1000px) rotateX(${simTilt.toFixed(2)}deg) scale(${simScale.toFixed(3)})`;
      }

      // 4. Background Humaaans Figures (Continuous Movement, Rotation, Scale, and Opacity Envelope)
      bgHumaaans.forEach(h => {
        const el = document.getElementById(h.id);
        if (!el) return;

        const dist = scrollY - h.top + winH * 0.5;
        const ty = dist * h.factor;
        const rot = h.baseRot + Math.sin(dist * 0.003) * 12;
        const progress = Math.max(0, Math.min(1, 1 - Math.abs(dist) / (winH * 0.85)));
        const scale = 0.85 + 0.3 * progress;

        const isMobile = window.innerWidth < 768;
        const baseOpacity = isMobile ? 0.12 : (document.body.dataset.paper === 'night' ? 0.16 : 0.24);
        const opacity = baseOpacity * (0.4 + 0.6 * progress);

        el.style.transform = `translate3d(0, ${ty.toFixed(1)}px, 0) scale(${scale.toFixed(2)}) rotate(${rot.toFixed(1)}deg)`;
        el.style.opacity = opacity.toFixed(2);
      });

      // 5. Use Case Cards Entry, Scrapbook Tilt, and Embedded Humaaans Drift
      cards.forEach(c => {
        if (!c.el) return;
        const rect = c.el.getBoundingClientRect();
        const dist = rect.top + rect.height / 2 - winH / 2;
        const p = Math.max(0, Math.min(1, 1 - Math.abs(dist) / (winH * 0.8)));

        const dynamicTilt = c.baseTilt * p + (1 - p) * (c.baseTilt > 0 ? 4 : -4);
        const scale = 0.94 + 0.06 * p;
        const ty = 30 * (1 - p);

        c.el.style.transform = `translate3d(0, ${ty.toFixed(1)}px, 0) rotate(${dynamicTilt.toFixed(2)}deg) scale(${scale.toFixed(3)})`;

        const img = c.el.querySelector('.uc-humaaan-img');
        if (img) {
          const imgFloat = Math.sin(scrollY * 0.006) * 6;
          img.style.transform = `translate3d(0, ${imgFloat.toFixed(1)}px, 0)`;
        }
      });

      // 6. Traveling Kinetic Arrow along Journey Path
      const track = document.getElementById('journeyTrack');
      if (track && svgPath && travelingArrow && window.innerWidth >= 640) {
        const trackRect = track.getBoundingClientRect();
        const pathLen = svgPath.getTotalLength();
        if (pathLen > 0) {
          const rawProgress = (winH * 0.6 - trackRect.top) / trackRect.height;
          const progress = Math.max(0, Math.min(1, rawProgress));
          const point = svgPath.getPointAtLength(progress * pathLen);

          travelingArrow.style.left = `${point.x}px`;
          travelingArrow.style.top = `${point.y}px`;

          const lookAhead = Math.min(pathLen, progress * pathLen + 10);
          const nextP = svgPath.getPointAtLength(lookAhead);
          const angle = Math.atan2(nextP.y - point.y, nextP.x - point.x) * (180 / Math.PI);
          travelingArrow.style.transform = `translate(-50%, -50%) rotate(${angle + 90}deg)`;

          if (activePath) {
            activePath.style.strokeDasharray = `${progress * pathLen} ${pathLen}`;
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

    // Initial setup
    setTimeout(() => {
      buildConnectorPath();
      requestScrollUpdate();
      updateSim();
    }, 100);

    // ---------------------------------------------------------
    // WALKTHROUGH TOUR MODAL (NO EMOJIS)
    // ---------------------------------------------------------
    const tourSteps = [
      {
        title: '1. Login & Carry Your Portable Memory',
        body: 'Click <b>Log In</b> to connect your Sui Wallet or start as a Guest. GoalStar remembers your personal friction, stamina patterns, and completed steps across browser reloads and CLI sessions.'
      },
      {
        title: '2. Dream Any Goal',
        body: 'Type where you are and where you want to be. The AI planner generates the intermediate milestones and actions automatically with zero blank-page paralysis.'
      },
      {
        title: '3. Follow the A* Green Route',
        body: 'Instead of an overwhelming to-do list, GoalStar calculates the <b>single lowest-friction route</b>. Adjust your priorities (Time, Money, Effort, Risk) to watch the path reroute in real time.'
      },
      {
        title: '4. Verifiable Onchain Proof on Sui',
        body: 'Whenever you complete a major deliverable, click <b>Stamp on Sui</b>. Tatum generates an immutable cryptographic proof digest you can share with clients, peers, or grant judges.'
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

    document.querySelectorAll('#heroTourBtn, #navTourBtn').forEach(btn => {
      btn.addEventListener('click', () => {
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

print(f"Generated home.html successfully! Length: {len(html_content)} bytes")
