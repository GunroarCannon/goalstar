import re

new_home_html = '''<!doctype html>
<html lang="en" class="landing-html">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GoalStar — Smart Agents for Real Life Goals</title>
  <meta name="description" content="A* Pathfinding for Life Goals, backed by Walrus Portable Memory on Mainnet and Tatum Sui RPC.">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cpath d='M9.6 31.2 C 14.5 30.5, 14.5 23.5, 21.2 21.4' fill='none' stroke='%232a2d3e' stroke-width='2.4' stroke-linecap='round' stroke-dasharray='0.1 4.4'/%3E%3Ccircle cx='6.2' cy='33' r='3.6' fill='%232f9e6a' stroke='%232a2d3e' stroke-width='1.8'/%3E%3Cpolygon points='28.5,3.0 31.0,9.0 37.5,9.6 32.6,13.8 34.1,20.2 28.5,16.8 22.9,20.2 24.4,13.8 19.5,9.6 26.0,9.0' fill='%23f2b705' stroke='%232a2d3e' stroke-width='1.8' stroke-linejoin='round'/%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Fraunces:ital,opsz,wght@0,9..144,600..900;1,9..144,400&family=Patrick+Hand&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <style>
    /* Specific Landing Page Styles with High-Craft Tactile Papercraft Aesthetic */
    html.landing-html, body.landing-body {
      height: auto !important;
      min-height: 100vh;
      display: block !important;
      overflow-x: hidden !important;
      overflow-y: auto !important;
    }
    .landing-body {
      background: var(--paper);
      color: var(--ink);
      font-family: 'Patrick Hand', var(--ui);
      background-image: 
        radial-gradient(var(--line) 1px, transparent 1px),
        linear-gradient(to right, rgba(0,0,0,0.02) 1px, transparent 1px);
      background-size: 24px 24px, 120px 100%;
    }
    body[data-paper='night'] .landing-body {
      background-image: 
        radial-gradient(rgba(140, 170, 220, 0.12) 1px, transparent 1px),
        linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px);
    }

    /* Sticky Engraved Header */
    .landing-header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--panel);
      border-bottom: 2.5px solid var(--ink);
      box-shadow: 0 3px 0 var(--ink), 0 6px 12px rgba(0,0,0,0.12);
      display: flex;
      align-items: center;
      padding: 10px 24px;
      gap: 16px;
      backdrop-filter: blur(8px);
    }
    .landing-nav {
      display: flex;
      gap: 18px;
      margin-left: 20px;
    }
    .landing-nav a {
      color: var(--ink);
      text-decoration: none;
      font-size: 16px;
      font-weight: bold;
      padding: 4px 10px;
      border-radius: 3px;
      transition: all 0.15s;
      border: 1px dashed transparent;
    }
    .landing-nav a:hover {
      border-color: var(--ink);
      background: var(--hl);
      transform: translateY(-1px);
    }
    .landing-actions {
      margin-left: auto;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    /* Hero Section with Layered Cutout Paper Sculpture */
    .hero-sec {
      padding: 48px 24px 36px;
      max-width: 1140px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      align-items: center;
      gap: 36px;
      position: relative;
    }
    @media (max-width: 900px) {
      .hero-sec { grid-template-columns: 1fr; text-align: center; }
      .hero-left { text-align: center; }
      .hero-cta-row { justify-content: center; }
    }
    .hero-badge {
      display: inline-block;
      background: #fffbeb;
      border: 2px solid var(--ink);
      box-shadow: 2px 2px 0 var(--ink);
      padding: 4px 14px;
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.5px;
      margin-bottom: 16px;
      border-radius: 255px 8px 225px 8px/8px 225px 8px 255px;
      color: var(--ink);
    }
    body[data-paper='night'] .hero-badge {
      background: #232c3e;
      color: #f2c84b;
      border-color: #f59e0b;
    }
    .hero-title {
      font-family: 'Fraunces', 'Caveat', serif;
      font-size: clamp(38px, 5.2vw, 62px);
      line-height: 1.08;
      margin: 0 0 18px;
      letter-spacing: -0.8px;
      color: var(--ink);
    }
    .hero-title span.hl {
      color: #d97706;
      text-decoration: underline wavy #10b981 3px;
      text-underline-offset: 8px;
    }
    .hero-desc {
      font-size: clamp(18px, 2.2vw, 22px);
      margin: 0 0 32px;
      color: var(--ink-soft);
      line-height: 1.45;
    }
    .hero-cta-row {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
    }

    /* Paper Cutout Head Sculpture (Reference 1 & 2) */
    .paper-sculpture-card {
      position: relative;
      background: var(--panel);
      border: 2.5px solid var(--ink);
      box-shadow: 6px 6px 0 var(--ink), 0 10px 20px rgba(0,0,0,0.15);
      border-radius: 6px;
      padding: 20px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    .sculpture-meta {
      width: 100%;
      display: flex;
      justify-content: space-between;
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 800;
      color: var(--ink-soft);
      border-bottom: 1.5px dashed var(--ink);
      padding-bottom: 6px;
      margin-bottom: 14px;
      letter-spacing: 1px;
    }
    .sculpture-svg-wrap {
      width: 100%;
      max-width: 320px;
      height: 280px;
      position: relative;
    }
    .sculpture-svg {
      width: 100%;
      height: 100%;
      filter: drop-shadow(0 8px 16px rgba(0,0,0,0.18));
      transition: transform 0.3s ease;
    }
    .sculpture-tagline {
      margin-top: 10px;
      font-family: 'Caveat', cursive;
      font-size: 19px;
      font-weight: bold;
      color: var(--ink);
    }

    /* Live Interactive Simulator Widget */
    .sim-card {
      background: var(--panel);
      border: 2.5px solid var(--ink);
      box-shadow: 5px 5px 0 var(--ink), 0 8px 16px rgba(0,0,0,0.12);
      border-radius: 6px;
      padding: 24px;
      max-width: 1040px;
      margin: 32px auto 60px;
      text-align: left;
    }
    .sim-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 12px;
    }
    .sim-head h3 {
      font-family: 'Fraunces', 'Caveat', serif;
      font-size: 26px;
      margin: 0;
    }
    .sim-slider-box {
      display: flex;
      align-items: center;
      gap: 12px;
      background: var(--card);
      border: 2px solid var(--ink);
      padding: 6px 14px;
      box-shadow: 2px 2px 0 var(--ink);
      border-radius: 4px;
    }
    .sim-canvas {
      position: relative;
      height: 160px;
      background: var(--paper);
      border: 2.5px solid var(--ink);
      box-shadow: inset 2px 2px 5px rgba(0,0,0,0.15);
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: space-around;
      padding: 0 20px;
      overflow: hidden;
    }
    .sim-node {
      position: relative;
      z-index: 2;
      background: var(--panel);
      border: 2px solid var(--ink);
      box-shadow: 2.5px 2.5px 0 var(--ink);
      padding: 10px 16px;
      font-weight: bold;
      font-size: 16px;
      text-align: center;
      transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .sim-node.start {
      border-color: #10b981;
      background: #ecfdf5;
      color: #064e3b;
    }
    body[data-paper='night'] .sim-node.start {
      background: #143527;
      color: #a7f3d0;
    }
    .sim-node.goal {
      border-color: #f59e0b;
      background: #fffbeb;
      color: #78350f;
    }
    body[data-paper='night'] .sim-node.goal {
      background: #3b3216;
      color: #fde68a;
    }
    .sim-node.mid {
      opacity: 0.55;
      transform: scale(0.95);
    }
    .sim-node.active-path {
      opacity: 1;
      transform: scale(1.05);
      border-color: #10b981;
      box-shadow: 3.5px 3.5px 0 #10b981;
    }
    .sim-node.blocked-path {
      opacity: 0.35;
      text-decoration: line-through;
      filter: grayscale(80%);
    }

    /* Scroll Use Cases Journey */
    .use-cases-sec {
      padding: 60px 24px 80px;
      max-width: 960px;
      margin: 0 auto;
      position: relative;
    }
    .sec-header {
      text-align: center;
      margin-bottom: 50px;
    }
    .sec-header h2 {
      font-family: 'Fraunces', 'Caveat', serif;
      font-size: clamp(34px, 4.5vw, 50px);
      margin: 0 0 10px;
      color: var(--ink);
    }
    .sec-header p {
      font-size: 21px;
      color: var(--ink-soft);
      max-width: 640px;
      margin: 0 auto;
    }

    /* Fixed Scroll Progress Ribbon */
    .scroll-hud {
      position: fixed;
      left: 20px;
      top: 50%;
      transform: translateY(-50%);
      background: var(--panel);
      border: 2px solid var(--ink);
      box-shadow: 3px 3px 0 var(--ink);
      padding: 10px 14px;
      border-radius: 4px;
      z-index: 90;
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.8px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      opacity: 0;
      transition: opacity 0.3s;
      pointer-events: none;
    }
    @media (max-width: 1200px) {
      .scroll-hud { display: none; }
    }
    .scroll-hud.visible {
      opacity: 0.95;
    }
    .hud-step {
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--ink-soft);
      transition: color 0.2s;
    }
    .hud-step.active {
      color: #10b981;
      font-weight: 900;
    }
    .hud-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      border: 1px solid var(--ink);
      background: var(--paper);
    }
    .hud-step.active .hud-dot {
      background: #10b981;
      box-shadow: 0 0 6px #10b981;
    }

    .journey-track {
      position: relative;
      padding: 20px 0;
    }

    /* Kinetic SVG Overlay for Connecting Path & Traveling Arrow */
    .journey-svg {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 1;
      overflow: visible;
    }
    .journey-path {
      fill: none;
      stroke: var(--ink);
      stroke-width: 3.5;
      stroke-dasharray: 8 6;
      stroke-linecap: round;
      opacity: 0.75;
      transition: stroke 0.3s;
    }
    body[data-paper='night'] .journey-path {
      stroke: #7d9cff;
    }
    .journey-path-active {
      fill: none;
      stroke: #10b981;
      stroke-width: 4;
      stroke-linecap: round;
      stroke-linejoin: round;
      opacity: 0.95;
    }

    /* Use Case Cards inside Bays */
    .card-bay {
      position: relative;
      background: rgba(42, 45, 62, 0.04);
      border: 2px dashed rgba(42, 45, 62, 0.3);
      border-radius: 6px;
      box-shadow: 
        inset 3px 3px 8px rgba(0, 0, 0, 0.12),
        inset -2px -2px 6px rgba(255, 255, 255, 0.6);
      padding: 6px;
      margin-bottom: 50px;
      transition: all 0.3s ease;
    }
    body[data-paper='night'] .card-bay {
      background: rgba(0, 0, 0, 0.3);
      border-color: rgba(245, 158, 11, 0.25);
      box-shadow: 
        inset 3px 3px 10px rgba(0, 0, 0, 0.7),
        inset -1px -1px 4px rgba(255, 255, 255, 0.05);
    }
    .card-bay.docked {
      border-style: solid;
      border-color: #10b981;
    }

    .uc-card {
      position: relative;
      z-index: 2;
      background: var(--panel);
      border: 2px solid var(--ink);
      box-shadow: 4px 4px 0 var(--ink);
      border-radius: 4px;
      padding: 26px;
      transform: translateY(30px) scale(0.96) rotate(-1.5deg);
      opacity: 0.55;
      transition: 
        transform 0.45s cubic-bezier(0.34, 1.56, 0.64, 1),
        box-shadow 0.3s ease,
        opacity 0.3s ease;
    }
    .uc-card.docked-in {
      transform: translateY(0) scale(1) rotate(0deg) !important;
      opacity: 1 !important;
      border-color: #10b981 !important;
      box-shadow: 5px 5px 0 var(--ink) !important;
    }
    .uc-card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 14px;
      flex-wrap: wrap;
      gap: 10px;
    }
    .uc-badge-group {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .uc-step-num {
      background: #10b981;
      color: #fff;
      font-size: 13.5px;
      font-weight: 800;
      padding: 3px 8px;
      border: 1.5px solid var(--ink);
      box-shadow: 1.5px 1.5px 0 var(--ink);
      font-family: 'Space Grotesk', monospace;
    }
    .uc-role {
      font-family: 'Fraunces', 'Caveat', serif;
      font-size: 27px;
      margin: 0;
      line-height: 1.1;
    }
    .uc-status-tag {
      background: #fffbeb;
      border: 1.5px solid var(--ink);
      padding: 4px 10px;
      font-size: 13.5px;
      font-weight: bold;
      box-shadow: 1.5px 1.5px 0 var(--ink);
      border-radius: 2px;
    }
    body[data-paper='night'] .uc-status-tag {
      background: #232c3e;
      color: #f2c84b;
    }

    .uc-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin: 16px 0;
    }
    @media (max-width: 680px) {
      .uc-grid { grid-template-columns: 1fr; }
    }
    .uc-box-problem {
      background: rgba(239, 68, 68, 0.08);
      border: 1.5px solid rgba(239, 68, 68, 0.4);
      padding: 14px;
      border-radius: 3px;
    }
    .uc-box-problem h4 {
      margin: 0 0 6px;
      color: #b91c1c;
      font-size: 17px;
    }
    body[data-paper='night'] .uc-box-problem h4 {
      color: #f87171;
    }
    .uc-box-solution {
      background: rgba(16, 185, 129, 0.08);
      border: 1.5px solid rgba(16, 185, 129, 0.4);
      padding: 14px;
      border-radius: 3px;
    }
    .uc-box-solution h4 {
      margin: 0 0 6px;
      color: #047857;
      font-size: 17px;
    }
    body[data-paper='night'] .uc-box-solution h4 {
      color: #34d399;
    }

    .uc-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1.5px dashed var(--ink-soft);
      padding-top: 14px;
      font-size: 15px;
      flex-wrap: wrap;
      gap: 10px;
    }
    .uc-stat-pill {
      font-weight: bold;
      color: #10b981;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 16px;
    }

    /* Footer */
    .landing-footer {
      border-top: 2.5px solid var(--ink);
      background: var(--panel);
      padding: 40px 24px;
      text-align: center;
      margin-top: 60px;
      box-shadow: 0 -3px 0 var(--ink);
    }
  </style>
</head>
<body class="landing-body" data-paper="lined">
  <!-- Sticky Engraved Header -->
  <header class="landing-header">
    <a class="brand" href="/home" title="GoalStar">
      <svg class="logo" viewBox="0 0 40 40" aria-hidden="true">
        <path class="trail" d="M9.6 31.2 C 14.5 30.5, 14.5 23.5, 21.2 21.4"/>
        <circle cx="6.2" cy="33" r="3.6" class="dot0"/>
        <g class="st"><polygon points="28.5,3.0 31.0,9.0 37.5,9.6 32.6,13.8 34.1,20.2 28.5,16.8 22.9,20.2 24.4,13.8 19.5,9.6 26.0,9.0"/></g>
      </svg>
      <span class="word">goal<b>star</b></span>
    </a>

    <nav class="landing-nav">
      <a href="#simulator">Live Simulator</a>
      <a href="#use-cases">Use Cases</a>
      <a href="javascript:void(0)" id="navLaunchApp">Launch App</a>
    </nav>

    <div class="landing-actions">
      <!-- Engraved Pill Switch for Theme (Reference Image 0) -->
      <div class="engraved-switch" id="themeSwitch" role="button" tabindex="0" title="Toggle Light / Dark Mode">
        <div class="switch-track">
          <span class="track-label left">LIGHT</span>
          <span class="track-label right">DARK</span>
          <div class="switch-knob"></div>
        </div>
      </div>

      <!-- Engraved Pill Switch for Sound (Reference Image 0) -->
      <div class="engraved-switch active" id="soundSwitch" role="button" tabindex="0" title="Toggle Snappy Sound">
        <div class="switch-track">
          <span class="track-label left">MUTE</span>
          <span class="track-label right">AUDIO</span>
          <div class="switch-knob"></div>
        </div>
      </div>

      <button id="loginBtn" class="engraved-btn login-btn" title="Log In or Connect Wallet">🔑 Log In</button>
      <div id="userBadge" class="user-badge" hidden>
        <span class="indicator live"></span>
        <span id="userName" class="user-name">Guest</span>
        <button id="logoutBtn" class="logout-link">logout</button>
      </div>

      <button id="launchPlannerTopBtn" class="engraved-btn launch-btn" title="Open Planner">🚀 Launch Planner</button>
    </div>
  </header>

  <!-- Fixed Scroll Progress HUD -->
  <aside class="scroll-hud" id="scrollHud" aria-hidden="true">
    <div style="font-size:9.5px; margin-bottom:4px; color:var(--ink); font-weight:900;">A* SEARCH TRAIL</div>
    <div class="hud-step active" data-step="1"><span class="hud-dot"></span> 01 Founder</div>
    <div class="hud-step" data-step="2"><span class="hud-dot"></span> 02 Student</div>
    <div class="hud-step" data-step="3"><span class="hud-dot"></span> 03 Agency</div>
    <div class="hud-step" data-step="4"><span class="hud-dot"></span> 04 ADHD</div>
    <div class="hud-step" data-step="5"><span class="hud-dot"></span> 05 Terminal</div>
  </aside>

  <main>
    <!-- Hero Section with Paper Cutout Sculpture (Reference 1 & 2) -->
    <section class="hero-sec">
      <div class="hero-left">
        <div class="hero-badge">🧠 WALRUS MAINNET MEMORY · TATUM SUI RPC</div>
        <h1 class="hero-title">A* Pathfinding for Life Goals, Backed by <span class="hl">Portable Memory</span></h1>
        <p class="hero-desc">
          Stop hitting roadblocks and starting over from a blank page. GoalStar remembers your real-world stamina, learns your friction patterns, and dynamically reroutes your path to what actually works.
        </p>

        <div class="hero-cta-row">
          <button id="heroLaunchBtn" class="engraved-btn launch-btn" style="font-size: 19px !important; padding: 10px 24px !important;">🚀 Open Interactive Planner</button>
          <button id="heroTourBtn" class="engraved-btn" style="font-size: 19px !important; padding: 10px 20px !important;">🎓 How It Works Tour</button>
        </div>
      </div>

      <div class="hero-right">
        <!-- Paper Cutout Multi-layered Sculpture (Reference 1, 2) -->
        <div class="paper-sculpture-card" id="sculptureCard">
          <div class="sculpture-meta">
            <span>NO. 042 // RECALL ARCH</span>
            <span>OCT 28, 2026</span>
          </div>

          <div class="sculpture-svg-wrap">
            <svg class="sculpture-svg" viewBox="0 0 300 260" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <filter id="cutShadow" x="-10%" y="-10%" width="130%" height="130%">
                  <feDropShadow dx="2" dy="4" stdDeviation="3" flood-opacity="0.32" />
                </filter>
                <filter id="deepCutShadow" x="-15%" y="-15%" width="135%" height="135%">
                  <feDropShadow dx="3" dy="6" stdDeviation="4" flood-opacity="0.4" />
                </filter>
              </defs>

              <!-- Layer 1: Background Warm Paper Plate with Grid Stamp (Reference 2) -->
              <rect x="15" y="15" width="270" height="230" rx="8" fill="#e8dfcb" stroke="#2a2d3e" stroke-width="2" />
              <g opacity="0.25">
                <line x1="15" y1="60" x2="285" y2="60" stroke="#2a2d3e" stroke-width="1" stroke-dasharray="2 2" />
                <line x1="15" y1="110" x2="285" y2="110" stroke="#2a2d3e" stroke-width="1" stroke-dasharray="2 2" />
                <line x1="15" y1="160" x2="285" y2="160" stroke="#2a2d3e" stroke-width="1" stroke-dasharray="2 2" />
                <line x1="15" y1="210" x2="285" y2="210" stroke="#2a2d3e" stroke-width="1" stroke-dasharray="2 2" />
                <line x1="80" y1="15" x2="80" y2="245" stroke="#2a2d3e" stroke-width="1" stroke-dasharray="2 2" />
                <line x1="150" y1="15" x2="150" y2="245" stroke="#2a2d3e" stroke-width="1" stroke-dasharray="2 2" />
                <line x1="220" y1="15" x2="220" y2="245" stroke="#2a2d3e" stroke-width="1" stroke-dasharray="2 2" />
              </g>

              <!-- Layer 2: Terracotta Paper Sun (Reference 2) -->
              <circle cx="210" cy="80" r="42" fill="#d9532f" filter="url(#cutShadow)" />

              <!-- Layer 3: Paper Cutout Silhouette Head Profile (Reference 1) -->
              <path d="M 65 240 C 65 200, 75 190, 85 170 C 75 155, 68 135, 70 100 C 72 65, 95 35, 140 35 C 190 35, 205 65, 205 95 C 205 105, 212 112, 220 120 C 212 125, 205 135, 205 145 C 208 160, 195 180, 200 240 Z" 
                    fill="#fcf8ec" stroke="#2a2d3e" stroke-width="2.5" filter="url(#deepCutShadow)" />

              <!-- Layer 4: Deep Blue Ocean Path Wave inside head (Reference 1) -->
              <path d="M 75 220 C 95 210, 130 225, 160 215 C 180 210, 195 218, 200 225 L 200 240 L 70 240 Z" 
                    fill="#1e3a8a" filter="url(#cutShadow)" />
              <path d="M 72 195 C 100 185, 135 200, 165 190 C 185 185, 195 192, 203 198 L 203 218 L 73 218 Z" 
                    fill="#0284c7" filter="url(#cutShadow)" />
              <path d="M 78 170 C 110 160, 140 175, 175 165 C 190 160, 198 168, 205 175 L 205 190 L 76 190 Z" 
                    fill="#38bdf8" filter="url(#cutShadow)" />

              <!-- Layer 5: Dynamic A* Graph Nodes glowing in the Mind -->
              <line x1="105" y1="135" x2="145" y2="105" stroke="#10b981" stroke-width="3" stroke-dasharray="3 3" />
              <line x1="145" y1="105" x2="180" y2="75" stroke="#10b981" stroke-width="3" />
              <line x1="105" y1="135" x2="155" y2="145" stroke="#ef4444" stroke-width="2" stroke-dasharray="2 2" opacity="0.6" />

              <circle cx="105" cy="135" r="7" fill="#10b981" stroke="#2a2d3e" stroke-width="1.8" filter="url(#cutShadow)" />
              <circle cx="145" cy="105" r="8" fill="#10b981" stroke="#2a2d3e" stroke-width="2" filter="url(#cutShadow)" />
              <circle cx="155" cy="145" r="6" fill="#f87171" stroke="#2a2d3e" stroke-width="1.5" />

              <!-- Layer 6: Radiant Goal Gold Star -->
              <polygon points="180,60 184,70 195,71 187,79 189,90 180,84 171,90 173,79 165,71 176,70" 
                       fill="#f59e0b" stroke="#2a2d3e" stroke-width="1.8" filter="url(#cutShadow)" />

              <!-- Paper clouds overlapping (Reference 1 & 2) -->
              <path d="M 85 85 C 85 75, 95 68, 105 72 C 112 65, 128 65, 135 75 C 142 75, 148 82, 145 90 C 130 92, 95 92, 85 85 Z" 
                    fill="#ffffff" opacity="0.95" stroke="#2a2d3e" stroke-width="1.5" filter="url(#cutShadow)" />
            </svg>
          </div>

          <div class="sculpture-tagline">"The mind reroutes where friction permits."</div>
        </div>
      </div>
    </section>

    <!-- Live Route Simulator Mini-Widget -->
    <section id="simulator" style="padding: 0 24px;">
      <div class="sim-card">
        <div class="sim-head">
          <h3>⚡ Try Dynamic A* Rerouting Live:</h3>
          <div class="sim-slider-box">
            <label for="frictionSlider" style="font-weight: bold; font-size: 16px;">Current Stamina:</label>
            <input type="range" id="frictionSlider" min="1" max="10" value="8" title="Drag to simulate high vs low stamina">
            <span id="staminaLabel" style="font-weight: 800; width: 95px; font-family:'Space Grotesk', monospace;">HIGH (8/10)</span>
          </div>
        </div>

        <div class="sim-canvas">
          <div class="sim-node start">
            📍 Start<br><small>Idea Conceived</small>
          </div>

          <div id="simNodeMonolith" class="sim-node mid active-path">
            ⚠️ Monolith &amp; K8s<br><small id="monolithCost">Fast if stamina &ge; 6</small>
          </div>

          <div id="simNodeServerless" class="sim-node mid">
            🌱 Serverless &amp; Micro-Tasks<br><small id="serverlessCost">Lowest friction route</small>
          </div>

          <div class="sim-node goal">
            ★ Shipped on Mainnet<br><small>Verified on Sui</small>
          </div>
        </div>
        <div id="simFeedback" class="small muted" style="margin-top: 14px; font-size: 16px;">
          👉 <b>Green Path Selected:</b> Monolith setup is optimal when stamina is high. Drag the stamina slider down to simulate fatigue!
        </div>
      </div>
    </section>

    <!-- Scroll Use Cases Journey with Traveling Kinetic Arrow -->
    <section id="use-cases" class="use-cases-sec">
      <div class="sec-header">
        <h2>How Real People Beat Real-World Friction</h2>
        <p>As you scroll, watch the A* path dynamically shoot across the screen and click each milestone into its bay.</p>
      </div>

      <div class="journey-track" id="journeyTrack">
        <!-- Kinetic SVG Path with Traveling Arrow Overlay -->
        <svg class="journey-svg" id="journeySvg">
          <defs>
            <filter id="arrowShadow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="2" dy="4" stdDeviation="3" flood-opacity="0.35" />
            </filter>
          </defs>
          <path id="journeySvgPath" class="journey-path" d="M 50 80 Q 200 200 50 360 T 50 680 T 50 1020" />
          <path id="journeyActivePath" class="journey-path-active" d="M 50 80" />
          
          <!-- Traveling Arrowhead Group -->
          <g id="travelingArrow" class="traveling-arrow-group" transform="translate(50, 80)">
            <circle cx="0" cy="0" r="9" fill="#10b981" stroke="#2a2d3e" stroke-width="2" />
            <polygon points="-4,-7 14,0 -4,7 0,0" fill="#f59e0b" stroke="#2a2d3e" stroke-width="2" />
          </g>
        </svg>

        <!-- Use Case 1 Bay -->
        <div class="card-bay" data-step="1">
          <article class="uc-card" id="card1">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 01</span>
                <h3 class="uc-role">The Indie Hacker &amp; Solo Founder</h3>
              </div>
              <span class="uc-status-tag">🚀 Infrastructure Fatigue Rerouting</span>
            </div>
            <div class="uc-grid">
              <div class="uc-box-problem">
                <h4>❌ The Common Hurdle</h4>
                <p>Spending 14 days wrestling with Docker, Kubernetes, and VPC configs before testing a single product idea, resulting in burnout and an abandoned repo.</p>
              </div>
              <div class="uc-box-solution">
                <h4>✓ The GoalStar Solution</h4>
                <p>Walrus Memory recognizes recurring DevOps fatigue (+3.5 friction). The A* engine instantly recalculates your route through zero-config serverless, cutting 12 days of wasted overhead!</p>
              </div>
            </div>
            <div class="uc-footer">
              <span class="uc-stat-pill">✨ Impact: -12 Days Saved · Shipped in 48 Hours</span>
              <button class="engraved-btn scenario-launch-btn" data-scenario="Launch SaaS" style="font-size: 14px;">Try This Scenario ➔</button>
            </div>
          </article>
        </div>

        <!-- Use Case 2 Bay -->
        <div class="card-bay" data-step="2">
          <article class="uc-card" id="card2">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 02</span>
                <h3 class="uc-role">The Student &amp; Academic Researcher</h3>
              </div>
              <span class="uc-status-tag">📚 48h Watchdog Auto-Decomposition</span>
            </div>
            <div class="uc-grid">
              <div class="uc-box-problem">
                <h4>❌ The Common Hurdle</h4>
                <p>Staring blankly at a 40-page thesis literature review for 5 consecutive days. The intimidation barrier causes total procrastination until panic sets in.</p>
              </div>
              <div class="uc-box-solution">
                <h4>✓ The GoalStar Solution</h4>
                <p>When an edge sits idle for over 48 hours, GoalStar's Watchdog steps in: it automatically breaks the thesis milestone into three 15-minute micro-actions: find 2 sources, outline paragraph 1, export bibtex.</p>
              </div>
            </div>
            <div class="uc-footer">
              <span class="uc-stat-pill">⚡ Impact: +92% Momentum Restored · 0 Panic</span>
              <button class="engraved-btn scenario-launch-btn" data-scenario="Write Thesis" style="font-size: 14px;">Try This Scenario ➔</button>
            </div>
          </article>
        </div>

        <!-- Use Case 3 Bay -->
        <div class="card-bay" data-step="3">
          <article class="uc-card" id="card3">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 03</span>
                <h3 class="uc-role">The Freelancer &amp; Agency Contractor</h3>
              </div>
              <span class="uc-status-tag">💼 Cryptographic Proof of Work</span>
            </div>
            <div class="uc-grid">
              <div class="uc-box-problem">
                <h4>❌ The Common Hurdle</h4>
                <p>Client disputes over project deliverables and milestone completion dates buried across messy Slack chats and email threads.</p>
              </div>
              <div class="uc-box-solution">
                <h4>✓ The GoalStar Solution</h4>
                <p>Completed deliverables are stamped immutably onto Sui Mainnet via Tatum RPC. Clients receive shareable cryptographic proof digests with verified checkpoint numbers.</p>
              </div>
            </div>
            <div class="uc-footer">
              <span class="uc-stat-pill">📜 Impact: Sui Mainnet Stamped · Irrefutable Trust</span>
              <button class="engraved-btn scenario-launch-btn" data-scenario="Client Contract" style="font-size: 14px;">Try This Scenario ➔</button>
            </div>
          </article>
        </div>

        <!-- Use Case 4 Bay -->
        <div class="card-bay" data-step="4">
          <article class="uc-card" id="card4">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 04</span>
                <h3 class="uc-role">The ADHD &amp; Overwhelmed Mind</h3>
              </div>
              <span class="uc-status-tag">🧩 Zero-Guilt Single Action Focus</span>
            </div>
            <div class="uc-grid">
              <div class="uc-box-problem">
                <h4>❌ The Common Hurdle</h4>
                <p>A 25-item to-do list creates decision freeze. Missing 2 days triggers a shame spiral, leading to deleting the task app and giving up.</p>
              </div>
              <div class="uc-box-solution">
                <h4>✓ The GoalStar Solution</h4>
                <p>GoalStar never shows you 25 items at once. It computes ONE single lowest-activation-energy next step. Missed 3 days? No scolding—it just recalculates the next best route from where you are right now.</p>
              </div>
            </div>
            <div class="uc-footer">
              <span class="uc-stat-pill">🧘 Impact: 1 Action at a Time · Zero Guilt</span>
              <button class="engraved-btn scenario-launch-btn" data-scenario="Focus Routine" style="font-size: 14px;">Try This Scenario ➔</button>
            </div>
          </article>
        </div>

        <!-- Use Case 5 Bay -->
        <div class="card-bay" data-step="5">
          <article class="uc-card" id="card5">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <span class="uc-step-num">STEP 05</span>
                <h3 class="uc-role">The Cross-Platform Power User</h3>
              </div>
              <span class="uc-status-tag">⚡ Terminal, Browser, &amp; IDE Unity</span>
            </div>
            <div class="uc-grid">
              <div class="uc-box-problem">
                <h4>❌ The Common Hurdle</h4>
                <p>Planning state trapped inside browser tabs while real coding happens in terminal and Neovim/VSCode; context is lost every time you switch apps.</p>
              </div>
              <div class="uc-box-solution">
                <h4>✓ The GoalStar Solution</h4>
                <p>Walrus decentralized memory bridges CLI and Web seamlessly. Run <code>npm run cli "stamped step 3"</code> in your shell, and your web planner reflects it instantly!</p>
              </div>
            </div>
            <div class="uc-footer">
              <span class="uc-stat-pill">💻 Impact: 100% Synced CLI &amp; Web Session</span>
              <button class="engraved-btn launch-btn" id="card5LaunchBtn" style="font-size: 14px;">Launch Full Planner ➔</button>
            </div>
          </article>
        </div>
      </div>
    </section>
  </main>

  <!-- Login Dialog -->
  <dialog id="loginDlg" class="crunchy-modal">
    <div class="modal-card">
      <div class="modal-head">
        <h3>🔑 Connect &amp; Sync Portable Memory</h3>
        <button type="button" class="close-login-dlg" id="closeLoginDlg" aria-label="Close">✕</button>
      </div>
      <p class="muted small" style="margin-bottom: 16px;">
        Your stamina profile, completed milestones, and friction rules follow you across sessions and the CLI via Walrus Mainnet.
      </p>

      <div class="login-options">
        <div class="login-option" id="loginGuestOpt">
          <div class="opt-icon">⚡</div>
          <div class="opt-info">
            <h4>One-Click Guest Profile</h4>
            <p>Instant access with local persistence &amp; Walrus cloud bridge.</p>
          </div>
          <button id="connectGuestBtn" class="engraved-btn">Instant Login</button>
        </div>

        <div class="login-option" id="loginWalletOpt">
          <div class="opt-icon">🌊</div>
          <div class="opt-info">
            <h4>Connect Sui Web3 Wallet</h4>
            <p>Suiet, Slush, Ethos or any browser Sui wallet.</p>
          </div>
          <button id="connectWalletBtn" class="engraved-btn secondary">Connect Wallet</button>
        </div>

        <div class="login-option" id="loginWalrusOpt">
          <div class="opt-icon">🧠</div>
          <div class="opt-info">
            <h4>Walrus Account ID</h4>
            <p>Sync with your decentralized memory namespace.</p>
            <input type="text" id="walrusAccountInput" placeholder="e.g. 0x8a94b2... or alice-dev" />
          </div>
          <button id="connectWalrusBtn" class="engraved-btn secondary">Sync Memory</button>
        </div>
      </div>
    </div>
  </dialog>

  <!-- Quick Walkthrough Modal for /home -->
  <div id="homeTourModal" class="modal-overlay" hidden>
    <div class="modal-card" style="max-width: 540px;">
      <div class="modal-head">
        <h3 id="homeTourTitle">🎓 How GoalStar Works</h3>
        <button id="closeHomeTourBtn" class="close-modal">✕</button>
      </div>
      <div id="homeTourBody" style="font-size: 18px; line-height: 1.5; margin: 16px 0;">
        <!-- Injected by script -->
      </div>
      <div class="modal-actions" style="justify-content: space-between;">
        <button id="prevHomeTourBtn" class="engraved-btn secondary">Back</button>
        <span id="homeTourStepCount" class="small muted" style="align-self: center; font-family:'Space Grotesk', monospace;">Step 1 of 4</span>
        <button id="nextHomeTourBtn" class="engraved-btn">Next ➔</button>
      </div>
    </div>
  </div>

  <footer class="landing-footer">
    <div class="brand" style="justify-content: center; margin-bottom: 12px;">
      <span class="word" style="font-size: 26px;">goal<b>star</b></span>
    </div>
    <p>Smart Agents for Real Life · Total Recall Edition</p>
    <p class="small muted">Built for Sui &amp; Walrus Hackathon · Tatum RPC Gateway Mainnet &amp; Devnet Active</p>
  </footer>

  <script type="module">
    import { sound } from './js/sound.js';
    import { theme } from './js/theme.js';
    import { auth } from './js/auth.js';

    // Init theme, sound, and auth
    theme.init();
    sound.attachListeners();
    auth.init();

    // Universal Launch Action: if not logged in, auto-login as guest so there are zero roadblocks
    function launchPlanner() {
      sound.play('click');
      if (!auth.isLoggedIn()) {
        auth.connectGuest();
      } else {
        window.location.href = '/';
      }
    }

    document.querySelectorAll('#launchPlannerTopBtn, #heroLaunchBtn, #card5LaunchBtn, #navLaunchApp').forEach(b => {
      b.addEventListener('click', launchPlanner);
    });

    document.querySelectorAll('.scenario-launch-btn').forEach(b => {
      b.addEventListener('click', () => {
        launchPlanner();
      });
    });

    // Simulator interactive logic
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
        feedback.innerHTML = '👉 <b>Green Path Selected:</b> Monolith setup is optimal when stamina is high. Drag slider down to simulate fatigue!';
      } else {
        staminaLabel.textContent = `LOW (${val}/10)`;
        monolith.className = 'sim-node mid blocked-path';
        serverless.className = 'sim-node mid active-path';
        feedback.innerHTML = '👉 <b>A* Path Rerouted:</b> High friction detected on monolith! Route shifted to <b>Serverless &amp; Micro-Tasks</b> for lowest activation energy.';
      }
    }
    slider.addEventListener('input', () => {
      sound.play('crunch');
      updateSim();
    });

    // ---------------------------------------------------------
    // KINETIC SCROLL ANIMATION & TRAVELING ARROW ENGINE
    // ---------------------------------------------------------
    const bays = document.querySelectorAll('.card-bay');
    const cards = document.querySelectorAll('.uc-card');
    const svgPath = document.getElementById('journeySvgPath');
    const activePath = document.getElementById('journeyActivePath');
    const travelingArrow = document.getElementById('travelingArrow');
    const scrollHud = document.getElementById('scrollHud');
    const hudSteps = document.querySelectorAll('.hud-step');

    let pathPoints = [];
    let totalPathLength = 0;

    function buildConnectorPath() {
      if (!svgPath || bays.length < 2) return;
      const track = document.getElementById('journeyTrack');
      const trackRect = track.getBoundingClientRect();

      let d = '';
      pathPoints = [];

      bays.forEach((bay, idx) => {
        const rect = bay.getBoundingClientRect();
        // Zigzag coordinate across card centers
        const x = (idx % 2 === 0) ? rect.left - trackRect.left + 50 : rect.right - trackRect.left - 50;
        const y = rect.top - trackRect.top + rect.height / 2;
        pathPoints.push({ x, y });

        if (idx === 0) {
          d += `M ${x} ${y}`;
        } else {
          const prev = pathPoints[idx - 1];
          const midY = (prev.y + y) / 2;
          d += ` C ${prev.x} ${midY}, ${x} ${midY}, ${x} ${y}`;
        }
      });

      svgPath.setAttribute('d', d);
      totalPathLength = svgPath.getTotalLength();
    }

    const dockedMap = new Set();

    function onScroll() {
      const windowH = window.innerHeight;
      const triggerY = windowH * 0.75;
      const track = document.getElementById('journeyTrack');
      if (!track) return;

      const trackRect = track.getBoundingClientRect();

      // Show/hide HUD
      if (trackRect.top < windowH && trackRect.bottom > 100) {
        scrollHud?.classList.add('visible');
      } else {
        scrollHud?.classList.remove('visible');
      }

      // Check docking of cards into bays
      bays.forEach((bay, i) => {
        const rect = bay.getBoundingClientRect();
        const card = bay.querySelector('.uc-card');
        const stepNum = i + 1;

        if (rect.top < triggerY) {
          if (!dockedMap.has(i)) {
            dockedMap.add(i);
            bay.classList.add('docked');
            card?.classList.add('docked-in');
            sound.play('click'); // Audible click into place!
          }
          hudSteps.forEach(h => {
            if (parseInt(h.dataset.step, 10) <= stepNum) h.classList.add('active');
          });
        } else {
          if (dockedMap.has(i)) {
            dockedMap.delete(i);
            bay.classList.remove('docked');
            card?.classList.remove('docked-in');
          }
          hudSteps.forEach(h => {
            if (parseInt(h.dataset.step, 10) > stepNum) h.classList.remove('active');
          });
        }
      });

      // Update traveling arrow along the SVG curve
      if (totalPathLength > 0 && travelingArrow && activePath) {
        const scrollFraction = Math.max(0, Math.min(1, (-trackRect.top + windowH * 0.4) / (trackRect.height || 1)));
        const targetLen = scrollFraction * totalPathLength;

        // Draw active path up to current length
        const pt = svgPath.getPointAtLength(targetLen);
        const ptNext = svgPath.getPointAtLength(Math.min(totalPathLength, targetLen + 4));

        // Rotation tangent
        const angle = Math.atan2(ptNext.y - pt.y, ptNext.x - pt.x) * (180 / Math.PI);

        travelingArrow.setAttribute('transform', `translate(${pt.x}, ${pt.y}) rotate(${angle})`);

        // Subdivide active path
        try {
          // Update active path segment
          activePath.setAttribute('d', svgPath.getAttribute('d'));
          activePath.style.strokeDasharray = `${targetLen} ${totalPathLength}`;
        } catch (e) {}
      }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', () => {
      buildConnectorPath();
      onScroll();
    });

    setTimeout(() => {
      buildConnectorPath();
      onScroll();
    }, 120);

    // Quick Home Walkthrough Modal
    const tourSteps = [
      {
        title: '🔑 1. Login & Carry Your Portable Memory',
        body: 'Click <b>Log In</b> to connect your Sui Wallet or start as a Guest. GoalStar remembers your personal friction, stamina patterns, and completed steps across browser reloads and CLI sessions.'
      },
      {
        title: '✦ 2. Dream Any Goal',
        body: 'Type where you are and where you want to be. The AI planner generates the intermediate milestones and actions automatically—no blank-page paralysis!'
      },
      {
        title: '🧭 3. Follow the A* Green Route',
        body: 'Instead of an overwhelming to-do list, GoalStar calculates the <b>single lowest-stress route</b>. Adjust your priorities (Time, Money, Effort, Risk) to watch the path reroute in real time.'
      },
      {
        title: '📜 4. Verifiable Onchain Proof on Sui',
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
      document.getElementById('nextHomeTourBtn').textContent = currentHomeStep === tourSteps.length - 1 ? 'Launch Planner ➔' : 'Next ➔';
    }

    document.getElementById('heroTourBtn')?.addEventListener('click', () => {
      sound.play('pop');
      currentHomeStep = 0;
      renderHomeTour();
      tourModal.hidden = false;
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
  </script>
</body>
</html>
'''

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'w', encoding='utf-8') as f:
    f.write(new_home_html)

print('Wrote new high-craft home.html successfully')
