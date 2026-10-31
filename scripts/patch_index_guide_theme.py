import sys

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header block in index.html
old_header = """<header class="topbar">
    <button id="sideToggle" class="icon only-narrow" title="Toggle panel" aria-label="Toggle panel"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
    <a class="brand" href="./" title="goalstar"><svg class="logo" viewBox="0 0 40 40" aria-hidden="true"><path class="trail" d="M9.6 31.2 C 14.5 30.5, 14.5 23.5, 21.2 21.4"/><circle cx="6.2" cy="33" r="3.6" class="dot0"/><g class="st"><polygon points="28.5,3.0 31.0,9.0 37.5,9.6 32.6,13.8 34.1,20.2 28.5,16.8 22.9,20.2 24.4,13.8 19.5,9.6 26.0,9.0"/></g></svg><span class="word">goal<b>star</b></span></a>
    <a href="/home" class="nav-home-btn engraved-btn" title="Go to Home / Landing Page">Home</a>
    <select id="boardPick" title="Your goals" aria-label="Your goals"></select>
    <button id="newGoalBtn" class="engraved-btn" title="New goal"><span aria-hidden="true">+</span><span class="txt"> New goal</span></button>
    <div class="spacer"></div>
      <button id="dreamBtn" class="primary engraved-btn" title="Generate states and actions with an AI dreamer">Dream</button>
      <button id="searchBtn" class="gold engraved-btn" title="A* search for the lowest-cost path from START to GOAL">Search</button>
    <button id="stopBtn" hidden>■<span class="txt"> Stop</span></button>
    <button id="syncBtn" class="icon" title="Sync with GitHub Gist" aria-label="Sync">⟳</button>
      <button id="tourBtn" class="tour-nav-btn engraved-btn" title="Take a visual walkthrough of Total Recall features">Tour</button>
    <!-- Engraved Pill Switches (Reference Image 0) -->
    <div class="engraved-switch" id="themeSwitch" role="button" tabindex="0" title="Toggle Light / Dark Mode">
      <div class="switch-track">
        <div class="switch-knob"></div>
        <span class="track-label">LIGHT</span>
      </div>
    </div>
    </div>
    <div class="engraved-switch active" id="soundSwitch" role="button" tabindex="0" title="Toggle Snappy Sound">
      <div class="switch-track">
        <div class="switch-knob"></div>
        <span class="track-label">AUDIO</span>
      </div>
    </div>
    </div>
    <button id="themeToggleBtn" class="theme-toggle-btn" hidden></button>
    <button id="soundToggleBtn" class="sound-toggle-btn" hidden></button>
    <button id="loginBtn" class="login-btn engraved-btn" title="Log In or Connect Wallet">Log In</button>
    <div id="userBadge" class="user-badge" hidden>
      <span class="indicator live"></span>
      <span id="userName" class="user-name">Guest</span>
      <button id="logoutBtn" class="logout-link">logout</button>
    </div>
    <button id="settingsBtn" class="icon" title="Settings" aria-label="Settings"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></button>
  </header>"""

new_header = """<header class="topbar">
    <button id="sideToggle" class="icon only-narrow" title="Toggle panel" aria-label="Toggle panel"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
    <a class="brand" href="./" title="goalstar"><svg class="logo" viewBox="0 0 40 40" aria-hidden="true"><path class="trail" d="M9.6 31.2 C 14.5 30.5, 14.5 23.5, 21.2 21.4"/><circle cx="6.2" cy="33" r="3.6" class="dot0"/><g class="st"><polygon points="28.5,3.0 31.0,9.0 37.5,9.6 32.6,13.8 34.1,20.2 28.5,16.8 22.9,20.2 24.4,13.8 19.5,9.6 26.0,9.0"/></g></svg><span class="word">goal<b>star</b></span></a>
    <a href="/home" class="nav-home-btn engraved-btn" title="Go to Home / Landing Page">Home</a>
    <select id="boardPick" title="Your goals" aria-label="Your goals"></select>
    <button id="newGoalBtn" class="engraved-btn" title="New goal"><span aria-hidden="true">+</span><span class="txt"> New goal</span></button>
    <div class="spacer"></div>
    <button id="dreamBtn" class="primary engraved-btn" title="Generate states and actions with an AI dreamer">Dream</button>
    <button id="searchBtn" class="gold engraved-btn" title="A* search for the lowest-cost path from START to GOAL">Search</button>
    <button id="stopBtn" hidden><span class="txt">Stop</span></button>
    <button id="syncBtn" class="icon" title="Sync with GitHub Gist" aria-label="Sync"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg></button>
    
    <!-- Tutorial & Explainer Guide -->
    <button id="tourBtn" class="tour-nav-btn engraved-btn" title="Take a visual walkthrough of Total Recall features">Tour</button>
    <button id="uiGuideBtn" class="guide-btn engraved-btn" title="Open Interactive UI Explainer Guide"><span style="color:var(--accent);">?</span> Guide</button>

    <!-- 4 Curated Themes Selector -->
    <select id="themeSelect" class="theme-select engraved-select" title="Choose Theme Aesthetic">
      <option value="notebook">Notebook (Paper)</option>
      <option value="night">Chalkboard (Night)</option>
      <option value="blueprint">Blueprint (Technical)</option>
      <option value="monograph">Monograph (Vintage)</option>
    </select>

    <!-- Engraved Pill Switches -->
    <div class="engraved-switch" id="themeSwitch" role="button" tabindex="0" title="Toggle Light / Dark Mode">
      <div class="switch-track">
        <div class="switch-knob"></div>
        <span class="track-label">LIGHT</span>
      </div>
    </div>
    <div class="engraved-switch active" id="soundSwitch" role="button" tabindex="0" title="Toggle Snappy Sound">
      <div class="switch-track">
        <div class="switch-knob"></div>
        <span class="track-label">AUDIO</span>
      </div>
    </div>

    <button id="themeToggleBtn" class="theme-toggle-btn" hidden></button>
    <button id="soundToggleBtn" class="sound-toggle-btn" hidden></button>
    <button id="loginBtn" class="login-btn engraved-btn" title="Log In or Connect Wallet">Log In</button>
    <div id="userBadge" class="user-badge" hidden>
      <span class="indicator live"></span>
      <span id="userName" class="user-name">Guest</span>
      <button id="logoutBtn" class="logout-link">logout</button>
    </div>
    <button id="settingsBtn" class="icon" title="Settings" aria-label="Settings"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></button>
  </header>"""

assert old_header in text, "old_header not found in index.html"
text = text.replace(old_header, new_header)

# Add UI Guide Modal right before </body>
ui_guide_modal = """
  <!-- Interactive UI Explainer Modal (What Each Element Does) -->
  <dialog id="uiGuideDlg" style="max-width: 680px; width: 92%; border-radius: 12px; border: 1.5px solid var(--border); background: var(--panel); box-shadow: 0 18px 48px var(--shadow); padding: 0;">
    <div style="padding: 20px 24px; border-bottom: 1.5px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
      <div>
        <span style="font-family:'Space Grotesk',monospace; font-size:11px; font-weight:800; color:var(--accent); text-transform:uppercase;">Interactive Interface Guide</span>
        <h3 style="margin: 2px 0 0; font-size: 20px;">What Each GoalStar Element Does</h3>
      </div>
      <button type="button" id="closeUiGuideBtn" class="close-modal-btn" style="border:none; background:none; font-size:24px; cursor:pointer;">&times;</button>
    </div>
    
    <div style="padding: 20px 24px; max-height: 70vh; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; font-size: 13.5px; line-height: 1.5;">
      
      <div style="padding: 12px 14px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">1. Goal Selector &amp; Progress Bar (Left Sidebar):</b>
        <p style="margin: 4px 0 0; color:var(--ink-soft);">Tracks your current macro-goal, percentage completed, and days remaining calculated by A* path analysis.</p>
      </div>

      <div style="padding: 12px 14px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">2. 4-Bar Path Profile:</b>
        <p style="margin: 4px 0 0; color:var(--ink-soft);">Breaks down total cognitive and physical friction across 4 dimensions: <b>Time</b> (calendar days), <b>Money</b> (budget cost), <b>Effort</b> (stamina drain), and <b>Risk</b> (uncertainty).</p>
      </div>

      <div style="padding: 12px 14px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">3. Best Path Checklist:</b>
        <p style="margin: 4px 0 0; color:var(--ink-soft);">The lowest-resistance sequence of actions to reach your destination. Click any action to inspect sub-checklists or check it off as completed.</p>
      </div>

      <div style="padding: 12px 14px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">4. Dream vs. Search (Top Bar):</b>
        <p style="margin: 4px 0 0; color:var(--ink-soft);"><b>Dream</b> uses AI (Groq LPU or offline) to brainstorm realistic intermediate states and breakdown steps. <b>Search</b> runs the A* graph algorithm to find the optimal bridge across your roadmap.</p>
      </div>

      <div style="padding: 12px 14px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">5. Interactive Canvas &amp; Minimap (Center):</b>
        <p style="margin: 4px 0 0; color:var(--ink-soft);">The live state graph. Double-click blank paper to create states. Drag states to reposition. Drag paper to pan; mouse wheel to zoom. Use <b>Fit</b> and <b>Tidy</b> in the minimap to auto-arrange.</p>
      </div>

      <div style="padding: 12px 14px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">6. &quot;Where You Are&quot; Inspector (Right Sidebar):</b>
        <p style="margin: 4px 0 0; color:var(--ink-soft);">Inspects the selected state: edit real-world notes, check accumulated path cost (g), and dream outward actions directly from this milestone.</p>
      </div>

      <div style="padding: 12px 14px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">7. Walrus Memory Banner &amp; Sui Blockchain Proof:</b>
        <p style="margin: 4px 0 0; color:var(--ink-soft);">Top banner tracks decentralized memory blobs on Walrus Mainnet. When you reach a milestone, click <b>Verify Milestone on Sui</b> to stamp an immutable, verifiable proof on the Sui ledger.</p>
      </div>

    </div>

    <div style="padding: 14px 24px; border-top: 1.5px solid var(--border); display: flex; justify-content: flex-end; gap: 10px;">
      <button type="button" id="launchTourFromGuideBtn" class="primary" style="background:var(--accent); border-color:var(--accent); color:#fff;">Start Interactive Spotlight Tour</button>
      <button type="button" id="closeGuideDlgBtn">Close Guide</button>
    </div>
  </dialog>
"""

idx_body = text.rfind('</body>')
text = text[:idx_body] + ui_guide_modal + text[idx_body:]

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated index.html with Theme Selector, UI Guide button, and Guide Modal!")
