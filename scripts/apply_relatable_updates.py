import re
import sys

def main():
    home_path = 'home.html'
    with open(home_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Rewrite Hero Description and Explanations
    old_hero = """        <p class="hero-desc">
          <strong>GoalStar is a planner for one real-life goal — a map of the steps between where you are and where you want to be.</strong>
          Tell it your destination and your starting point. It invents the milestones in between, prices every step in time, money, effort and risk, then highlights the cheapest way forward.
        </p>

        <div class="hero-explain">
          <div>
            <span class="he-label">What it is</span>
            <p>A visual goal map where every card is a state you can actually reach, and every line is a real action.</p>
          </div>
          <div>
            <span class="he-label">What it does</span>
            <p>Runs A* over your own weights, learns how much stamina each kind of step costs you, and reroutes around the steps where you usually stall.</p>
          </div>
          <div>
            <span class="he-label">Use it for</span>
            <p>Moving abroad, launching a product, changing careers, getting fit, saving money — any goal with more than one possible route.</p>
          </div>
        </div>"""

    new_hero = """        <p class="hero-desc">
          <strong>GoalStar maps the path between where you are right now and where you want to be.</strong>
          Give it your starting point and destination, and it drafts the realistic milestones in between. It estimates what each step costs in time, money, effort, and risk, then highlights the clearest route forward.
        </p>

        <div class="hero-explain">
          <div>
            <span class="he-label">What it is</span>
            <p>A step-by-step visual map. Every card is an actual milestone you can finish, and every line connects actions in an order that makes sense.</p>
          </div>
          <div>
            <span class="he-label">What it does</span>
            <p>It runs pathfinding tuned to your daily stamina. When a heavy task risks burnout, it reroutes you through lighter, steady steps so you keep moving.</p>
          </div>
          <div>
            <span class="he-label">Use it for</span>
            <p>Any goal with more than one route forward: getting a raise, studying overseas, launching a product, getting fit, or meeting someone.</p>
          </div>
        </div>"""

    if old_hero not in html:
        print("[ERR] old_hero not found in home.html!")
        sys.exit(1)
    html = html.replace(old_hero, new_hero)
    print("[OK] Replaced hero copy with humanized relatable text.")

    # 2. Add CSS for simulator presets & custom goal card
    css_anchor = "    .sim-canvas {"
    new_css = """    .sim-title-wrap {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .sim-subtitle {
      font-size: 13.5px;
      color: var(--ink-soft);
      margin: 0;
    }
    .sim-presets {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }
    .sim-preset-btn {
      font-family: 'Space Grotesk', monospace;
      font-size: 12.5px;
      font-weight: 700;
      padding: 6px 14px;
      background: var(--paper-warm);
      border: 1.5px solid var(--ink);
      border-radius: 4px;
      cursor: pointer;
      color: var(--ink);
      transition: all 0.15s ease;
      box-shadow: 1.5px 1.5px 0 var(--ink);
    }
    .sim-preset-btn:hover {
      border-color: var(--accent);
      color: var(--accent);
      transform: translateY(-1px);
    }
    .sim-preset-btn.active {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
      box-shadow: 2px 2px 0 #92400e;
    }
    body[data-paper='night'] .sim-preset-btn {
      background: #1e293b;
      border-color: rgba(245, 158, 11, 0.4);
      color: #f1f5f9;
      box-shadow: 1.5px 1.5px 0 rgba(245, 158, 11, 0.3);
    }
    body[data-paper='night'] .sim-preset-btn.active {
      background: #f59e0b;
      color: #0f172a;
      border-color: #f59e0b;
    }
    .sim-node-title {
      display: inline-block;
      font-weight: 700;
      line-height: 1.25;
    }
    .uc-custom-card {
      border-left: 4px solid var(--accent) !important;
    }
    .uc-custom-details {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .uc-custom-intro {
      font-size: 14px;
      color: var(--ink-soft);
      line-height: 1.5;
      margin: 0;
    }
    .custom-goal-form {
      display: flex;
      flex-direction: column;
      gap: 8px;
      background: var(--paper-warm);
      padding: 14px;
      border: 1.5px dashed var(--border);
      border-radius: 4px;
    }
    body[data-paper='night'] .custom-goal-form {
      background: #0f172a;
      border-color: rgba(245, 158, 11, 0.25);
    }
    .custom-goal-label {
      font-family: 'Space Grotesk', monospace;
      font-size: 11px;
      font-weight: 800;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .custom-goal-input-wrap {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .custom-goal-input {
      flex: 1;
      min-width: 220px;
      padding: 10px 14px;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 14px;
      background: #ffffff;
      border: 1.5px solid var(--ink);
      border-radius: 4px;
      color: var(--ink);
      outline: none;
      box-shadow: 2px 2px 0 var(--ink);
      transition: border-color 0.2s;
    }
    body[data-paper='night'] .custom-goal-input {
      background: #1e293b;
      border-color: rgba(245, 158, 11, 0.4);
      color: #f8fafc;
      box-shadow: 2px 2px 0 rgba(245, 158, 11, 0.3);
    }
    .custom-goal-input:focus {
      border-color: var(--accent);
    }
    .custom-goal-submit {
      padding: 10px 18px !important;
      font-size: 14px !important;
      white-space: nowrap;
    }
    .custom-goal-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 4px;
    }
    .goal-chip {
      font-size: 11.5px;
      font-family: 'Space Grotesk', monospace;
      font-weight: 700;
      padding: 3px 10px;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      cursor: pointer;
      color: var(--ink-soft);
      transition: all 0.15s ease;
      user-select: none;
    }
    .goal-chip:hover {
      border-color: var(--accent);
      color: var(--accent);
      transform: translateY(-1px);
    }
    body[data-paper='night'] .goal-chip {
      background: #1e293b;
      border-color: rgba(245, 158, 11, 0.3);
      color: #cbd5e1;
    }
    body[data-paper='night'] .goal-chip:hover {
      background: rgba(245, 158, 11, 0.2);
      color: #f59e0b;
    }

    .sim-canvas {"""

    if css_anchor not in html:
        print("[ERR] css_anchor not found in home.html!")
        sys.exit(1)
    html = html.replace(css_anchor, new_css)
    print("[OK] Added CSS styles for simulator presets and custom goal card.")

    # 3. Replace Simulator Markup
    old_sim = """    <!-- Live Route Simulator Widget -->
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
    </section>"""

    new_sim = """    <!-- Live Route Simulator Widget -->
    <section id="simulator" class="simulator-sec">
      <div class="sim-card" id="simCard">
        <div class="sim-head">
          <div class="sim-title-wrap">
            <h3 id="simTitle">Try Dynamic A* Rerouting Live:</h3>
            <p class="sim-subtitle">Pick a real-life goal and drag the stamina slider to see how GoalStar reroutes around burnout.</p>
          </div>
          <div class="sim-slider-box" id="simSliderBox">
            <div class="slider-fill-track" id="sliderFillTrack" style="width: 80%;"></div>
            <label for="frictionSlider" style="font-weight: 700; font-size: 14px;">Current Stamina:</label>
            <input type="range" id="frictionSlider" min="1" max="10" value="8" title="Drag slider to test stamina adaptation">
            <span id="staminaLabel" style="font-weight: 800; width: 95px; font-family:'Space Grotesk', monospace; font-size:13px;">HIGH (8/10)</span>
          </div>
        </div>

        <!-- Goal Selection Chips for the Simulator -->
        <div class="sim-presets" id="simPresets">
          <button type="button" class="sim-preset-btn active" data-preset="raise">💼 Get a $20k Raise</button>
          <button type="button" class="sim-preset-btn" data-preset="product">🚀 Launch a Product</button>
          <button type="button" class="sim-preset-btn" data-preset="abroad">✈️ Study Overseas</button>
          <button type="button" class="sim-preset-btn" data-preset="dating">❤️ Meet Someone</button>
        </div>

        <div class="sim-canvas">
          <div class="sim-node start" id="simNodeStart">
            <span class="sim-node-title" id="simStartTitle">Current Role</span><br><small id="simStartSub">Ready for next step</small>
          </div>

          <div id="simNodeMonolith" class="sim-node mid active-path">
            <span class="sim-node-title" id="simSprintTitle">Sprint &amp; Overtime</span><br><small id="monolithCost">High effort (stamina &ge; 6)</small>
          </div>

          <div id="simNodeServerless" class="sim-node mid">
            <span class="sim-node-title" id="simLeverageTitle">Document Wins &amp; 1-on-1s</span><br><small id="serverlessCost">High leverage, low burnout</small>
          </div>

          <div class="sim-node goal" id="simNodeGoal">
            <span class="sim-node-title" id="simGoalTitle">Raise Approved</span><br><small id="simGoalSub">Target salary locked</small>
          </div>
        </div>

        <div id="simFeedback" class="sim-feedback-box">
          <b>High Energy Route:</b> Taking on extra high-visibility assignments works great when your energy is high. Drag the slider down to simulate fatigue!
        </div>
      </div>
    </section>"""

    if old_sim not in html:
        print("[ERR] old_sim not found in home.html!")
        sys.exit(1)
    html = html.replace(old_sim, new_sim)
    print("[OK] Replaced simulator markup with relatable presets.")

    # 4. Replace Use Cases Header & 5 Cards
    use_cases_pattern = re.compile(
        r'<!-- Use Cases Journey \(Hanging Scrapbook Photo Cards 1 to 5\) -->.*?</section>',
        re.DOTALL
    )

    new_use_cases = """<!-- Use Cases Journey (Hanging Scrapbook Photo Cards 1 to 5) -->
    <section id="use-cases" class="use-cases-sec">
      <div class="sec-header overcome-header-box" id="overcomeHeaderBox">
        <div class="overcome-tape-top"></div>
        <span class="sec-tag">Real-Life Plans</span>
        <h2 class="sec-title">Engineered to Overcome Human Friction</h2>
        <p class="sec-desc">Where willpower runs out, dynamic A* pathfinding reroutes your steps so you never stall.</p>
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
                <h3 class="uc-role">The Career Climber</h3>
              </div>
              <span class="uc-status-tag">Negotiating a $20k Raise or Promotion</span>
              <span class="uc-tech-pill walrus"><span class="badge-live-dot"></span> Walrus Memory · Energy-Aware Routing</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item">
                  <span class="bullet-tag hurdle">The Trap</span>
                  <p><strong>The 60-hour work week:</strong> Grinding through endless overtime on low-visibility tasks, hoping management notices before exhaustion sets in.</p>
                </div>
                <div class="uc-bullet-item">
                  <span class="bullet-tag fix">A* Route</span>
                  <p><strong>High-leverage visibility pivot:</strong> When stamina drops, GoalStar shifts focus to documenting measurable business impact, weekly 1-on-1 alignment, and market salary data.</p>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_stand_16.webp" alt="Professional presenting" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">+$20k Secured · Zero Weekend Burnout</span>
              <button class="album-btn scenario-launch-btn" data-scenario="career" title="Simulate the career progression route">Simulate Route</button>
            </div>
          </article>
        </div>

        <!-- Card 2 -->
        <div class="card-bay" data-step="2">
          <article class="uc-card" id="card2">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <h3 class="uc-role">The Global Dreamer</h3>
              </div>
              <span class="uc-status-tag">Moving or Studying Abroad</span>
              <span class="uc-tech-pill walrus"><span class="badge-live-dot"></span> Walrus Memory · 48h Escalation Watchdog</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item">
                  <span class="bullet-tag hurdle">The Trap</span>
                  <p><strong>Bureaucracy and paperwork freeze:</strong> Drowning in visa criteria, embassy requirements, and scholarship essays for weeks without taking action.</p>
                </div>
                <div class="uc-bullet-item">
                  <span class="bullet-tag fix">A* Route</span>
                  <p><strong>Automatic micro-decomposition:</strong> Inactive application steps fracture into 15-minute concrete tasks (e.g., scan passport, draft personal statement intro).</p>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_stand_11.webp" alt="Student traveling abroad" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">100% Papers Submitted · No Missed Deadlines</span>
              <button class="album-btn scenario-launch-btn" data-scenario="abroad" title="Simulate the overseas application route">Simulate Route</button>
            </div>
          </article>
        </div>

        <!-- Card 3 -->
        <div class="card-bay" data-step="3">
          <article class="uc-card" id="card3">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <h3 class="uc-role">The Builder &amp; Maker</h3>
              </div>
              <span class="uc-status-tag">Shipping a Side Project or Product</span>
              <span class="uc-tech-pill walrus"><span class="badge-live-dot"></span> Walrus Memory · Friction Recalculation</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item">
                  <span class="bullet-tag hurdle">The Trap</span>
                  <p><strong>The 2-week architecture rabbit hole:</strong> Spending weeks configuring complex servers and databases before testing if anyone actually wants the product.</p>
                </div>
                <div class="uc-bullet-item">
                  <span class="bullet-tag fix">A* Route</span>
                  <p><strong>MVP fast-track reroute:</strong> Detects repetitive setup blocks and shifts the path to a simple working prototype and instant customer feedback.</p>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_sit_1.webp" alt="Creator launching product" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">Shipped in 3 Days · First Paying Customers</span>
              <button class="album-btn scenario-launch-btn" data-scenario="saas" title="Simulate the product launch route">Simulate Route</button>
            </div>
          </article>
        </div>

        <!-- Card 4 -->
        <div class="card-bay" data-step="4">
          <article class="uc-card" id="card4">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <h3 class="uc-role">The Overwhelmed Mind</h3>
              </div>
              <span class="uc-status-tag">Breaking Free from To-Do List Paralysis</span>
              <span class="uc-tech-pill walrus"><span class="badge-live-dot"></span> Walrus Memory · Anti-Shame Pathing</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item">
                  <span class="bullet-tag hurdle">The Trap</span>
                  <p><strong>To-do list freeze:</strong> 25 competing items cause overwhelm. Missing 2 days triggers shame, self-criticism, and abandoning the goal.</p>
                </div>
                <div class="uc-bullet-item">
                  <span class="bullet-tag fix">A* Route</span>
                  <p><strong>Single-step clarity:</strong> Hides future complexity and surfaces only the single highest-value action for today, resetting friction without guilt.</p>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_sit_6.webp" alt="Individual meditating" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">Zero-Shame Recalculation · Steady Flow</span>
              <button class="album-btn scenario-launch-btn" data-scenario="adhd" title="Simulate the anti-overwhelm route">Simulate Route</button>
            </div>
          </article>
        </div>

        <!-- Card 5 (Destination of Journey Path: Create Your Own Plan) -->
        <div class="card-bay" data-step="5">
          <article class="uc-card uc-custom-card" id="card5">
            <div class="uc-card-header">
              <div class="uc-badge-group">
                <h3 class="uc-role">Map Your Own Goal</h3>
              </div>
              <span class="uc-status-tag">Any Real-Life Destination</span>
              <span class="uc-tech-pill walrus"><span class="badge-live-dot"></span> Dynamic A* · Tailored To Your Energy</span>
            </div>
            <div class="uc-content-flex">
              <div class="uc-details uc-custom-details">
                <p class="uc-custom-intro">Have a real goal in mind? Whether it's moving abroad, getting a promotion, meeting someone, or launching a product — GoalStar plots the realistic milestones and prices the friction so you don't quit halfway.</p>
                <div class="custom-goal-form">
                  <label for="customGoalInput" class="custom-goal-label">Where do you want to be?</label>
                  <div class="custom-goal-input-wrap">
                    <input type="text" id="customGoalInput" class="custom-goal-input" placeholder="e.g. Get a $20k raise, Move to Japan, Launch my MVP..." />
                    <button type="button" id="card5LaunchBtn" class="album-btn primary-tape custom-goal-submit">Map My Goal &rarr;</button>
                  </div>
                  <div class="custom-goal-chips" id="customGoalChips">
                    <span class="goal-chip" data-goal="Get a $20k raise and promotion">💼 $20k Raise</span>
                    <span class="goal-chip" data-goal="Move and study abroad in Europe">✈️ Study Abroad</span>
                    <span class="goal-chip" data-goal="Launch my product MVP and get 10 users">🚀 Launch MVP</span>
                    <span class="goal-chip" data-goal="Get fit and run a 10k without injury">🏃 Run 10k</span>
                    <span class="goal-chip" data-goal="Meet someone and build a serious relationship">❤️ Meet Someone</span>
                  </div>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_stand_2.webp" alt="Individual planning future" class="uc-humaaan-img" loading="lazy">
              </div>
            </div>
            <div class="uc-card-footer">
              <span class="uc-stat-pill">Personalized Milestone Graph in 1 Click</span>
              <button class="album-btn scenario-launch-btn" data-scenario="custom" title="See how GoalStar builds your plan">See How It Works</button>
            </div>
          </article>
        </div></div>

        <!-- Centered Destination Terminal (Middle X Position Underneath Last Card) -->
        <div class="journey-terminal" id="journeyTerminal">
          <div class="terminal-circle-target" id="terminalCircleTarget">
            <div class="terminal-core-circle"></div>
          </div>
          <span class="terminal-badge">Goal Reached · Path Completed</span>
          <p class="terminal-sub">Dynamic A* Path Concluded</p>
        </div> </div>
    </section>"""

    if not use_cases_pattern.search(html):
        print("[ERR] use-cases section pattern not found in home.html!")
        sys.exit(1)
    html = use_cases_pattern.sub(new_use_cases, html)
    print("[OK] Replaced use cases section (removed step counts, made relatable, added custom goal card).")

    # 5. Update modal header & button text
    old_modal_header = """        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span id="scenarioStepNum" style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent);">PART 1 OF 5</span>
          <span id="scenarioScenarioTag" style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:700; color:var(--ink-muted);">SCENARIO SIMULATION</span>
        </div>"""

    new_modal_header = """        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span id="scenarioStepNum" style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent);">STAGE 1</span>
          <span id="scenarioScenarioTag" style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:700; color:var(--ink-muted);">PATH WALKTHROUGH</span>
        </div>"""

    if old_modal_header in html:
        html = html.replace(old_modal_header, new_modal_header)
        print("[OK] Updated modal header.")
    else:
        print("[WARN] old_modal_header not matched directly.")

    html = html.replace('<button type="button" class="album-btn primary-tape" id="nextScenarioStepBtn">Next Part</button>',
                        '<button type="button" class="album-btn primary-tape" id="nextScenarioStepBtn">Next Stage</button>')

    # 6. Update Simulator JavaScript
    old_sim_js = """    // ---------------------------------------------------------
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
    });"""

    new_sim_js = """    // ---------------------------------------------------------
    // LIVE SIMULATOR LOGIC WITH RELATABLE PRESETS
    // ---------------------------------------------------------
    const simPresets = {
      raise: {
        start: { title: 'Current Role', sub: 'Ready for next step' },
        sprint: { title: 'Sprint &amp; Overtime', sub: 'High effort (stamina &ge; 6)' },
        leverage: { title: 'Document Wins &amp; 1-on-1s', sub: 'High leverage, low burnout' },
        goal: { title: 'Raise Approved', sub: 'Target salary locked' },
        highFeedback: '<b>High Energy Route:</b> Taking on extra high-visibility assignments works great when your energy is high. Drag the slider down to simulate fatigue!',
        lowFeedback: '<b>A* Rerouted for Low Stamina:</b> Working 60-hour weeks leads to burnout right now. GoalStar shifts your plan to weekly 1-on-1 alignment and documented wins so you keep moving forward without burning out.'
      },
      product: {
        start: { title: 'Product Idea', sub: 'Validated concept' },
        sprint: { title: 'Full Custom Stack', sub: 'Deep build (stamina &ge; 6)' },
        leverage: { title: 'Simple MVP &amp; Waitlist', sub: 'Launch in 3 days, low stress' },
        goal: { title: 'Paying Customers', sub: 'Live in market' },
        highFeedback: '<b>High Energy Route:</b> Building a full custom system is fastest when you have uninterrupted deep focus. Drag the slider down to test fatigue!',
        lowFeedback: '<b>A* Rerouted for Low Stamina:</b> Setup fatigue detected! GoalStar shifts to a fast landing page and waitlist to test demand without weeks of architecture stress.'
      },
      abroad: {
        start: { title: 'Home Country', sub: 'Planning relocation' },
        sprint: { title: 'Mass Applications &amp; Cramming', sub: 'Intensive (stamina &ge; 6)' },
        leverage: { title: 'Top 2 Programs &amp; 20-min/day', sub: 'Zero overwhelm, steady pace' },
        goal: { title: 'Visa &amp; Offer in Hand', sub: 'Ready to fly' },
        highFeedback: '<b>High Energy Route:</b> Tackling multiple intensive university applications and test cramming works when energy is high.',
        lowFeedback: '<b>A* Rerouted for Low Stamina:</b> Bureaucracy overload detected. GoalStar focuses you on just your top 2 applications with 20 minutes of daily prep to keep momentum.'
      },
      dating: {
        start: { title: 'Single &amp; Looking', sub: 'Want genuine connection' },
        sprint: { title: '4 Mixers &amp; Events / Week', sub: 'High social battery (stamina &ge; 6)' },
        leverage: { title: '1 Weekly Club &amp; 2 Chats', sub: 'Low pressure, natural flow' },
        goal: { title: 'Meaningful Relationship', sub: 'Great partner found' },
        highFeedback: '<b>High Energy Route:</b> Attending multiple social mixers and events is effective when your social battery is at 100%.',
        lowFeedback: '<b>A* Rerouted for Low Stamina:</b> Social burnout detected! GoalStar shifts to one relaxed weekly hobby club and low-stress coffee chats so meeting people stays fun.'
      }
    };

    let activeSimPresetKey = 'raise';
    const slider = document.getElementById('frictionSlider');
    const sliderFillTrack = document.getElementById('sliderFillTrack');
    const staminaLabel = document.getElementById('staminaLabel');
    const monolith = document.getElementById('simNodeMonolith');
    const serverless = document.getElementById('simNodeServerless');
    const feedback = document.getElementById('simFeedback');

    function updateSim() {
      const val = parseInt(slider.value, 10);
      if (sliderFillTrack) sliderFillTrack.style.width = `${val * 10}%`;
      const preset = simPresets[activeSimPresetKey] || simPresets.raise;

      const startTitle = document.getElementById('simStartTitle');
      const startSub = document.getElementById('simStartSub');
      const sprintTitle = document.getElementById('simSprintTitle');
      const monolithCost = document.getElementById('monolithCost');
      const leverageTitle = document.getElementById('simLeverageTitle');
      const serverlessCost = document.getElementById('serverlessCost');
      const goalTitle = document.getElementById('simGoalTitle');
      const goalSub = document.getElementById('simGoalSub');

      if (startTitle) startTitle.innerHTML = preset.start.title;
      if (startSub) startSub.innerHTML = preset.start.sub;
      if (sprintTitle) sprintTitle.innerHTML = preset.sprint.title;
      if (monolithCost) monolithCost.innerHTML = preset.sprint.sub;
      if (leverageTitle) leverageTitle.innerHTML = preset.leverage.title;
      if (serverlessCost) serverlessCost.innerHTML = preset.leverage.sub;
      if (goalTitle) goalTitle.innerHTML = preset.goal.title;
      if (goalSub) goalSub.innerHTML = preset.goal.sub;

      if (val >= 6) {
        staminaLabel.textContent = `HIGH (${val}/10)`;
        monolith.className = 'sim-node mid active-path';
        serverless.className = 'sim-node mid';
        feedback.innerHTML = preset.highFeedback;
      } else {
        staminaLabel.textContent = `LOW (${val}/10)`;
        monolith.className = 'sim-node mid blocked-path';
        serverless.className = 'sim-node mid active-path';
        feedback.innerHTML = preset.lowFeedback;
      }
    }

    document.querySelectorAll('.sim-preset-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        sound.play('pop');
        document.querySelectorAll('.sim-preset-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeSimPresetKey = btn.getAttribute('data-preset') || 'raise';
        updateSim();
      });
    });

    slider.addEventListener('input', () => {
      sound.play('crunch');
      updateSim();
    });

    // Custom Goal Launcher (Card 5)
    const customGoalInput = document.getElementById('customGoalInput');
    const customGoalBtn = document.getElementById('card5LaunchBtn');
    function launchCustomGoal() {
      const g = (customGoalInput?.value || '').trim() || 'My Next Big Goal';
      sound.play('pop');
      window.location.href = `/index.html?goal=${encodeURIComponent(g)}`;
    }
    customGoalBtn?.addEventListener('click', launchCustomGoal);
    customGoalInput?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        launchCustomGoal();
      }
    });
    document.querySelectorAll('.goal-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        sound.play('click');
        const g = chip.getAttribute('data-goal');
        if (customGoalInput && g) {
          customGoalInput.value = g;
          customGoalInput.focus();
        }
      });
    });"""

    if old_sim_js not in html:
        print("[ERR] old_sim_js not found in home.html!")
        sys.exit(1)
    html = html.replace(old_sim_js, new_sim_js)
    print("[OK] Updated simulator JS logic with presets and custom goal handling.")

    # 7. Update scenarioData & walkthrough logic
    scenario_js_pattern = re.compile(
        r'// PROGRESSIVE SCENARIO SIMULATION WALKTHROUGH ENGINE.*?(?=document\.querySelectorAll\(\'\.scenario-launch-btn\'\))',
        re.DOTALL
    )

    new_scenario_js = """// PROGRESSIVE SCENARIO SIMULATION WALKTHROUGH ENGINE
    // ---------------------------------------------------------
    const scenarioData = {
      career: {
        title: 'The Career Climber: Securing a $20k Raise',
        stages: [
          {
            part: 1,
            title: 'Where You Are: Underpaid and Overworked',
            html: `
              <div class="scenario-card-preview">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent); margin-bottom:4px;">INITIAL REALITY</div>
                <div style="font-size:16px; font-weight:700;">Current State: 2 Years Without a Promotion</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">You do great work every week, but performance reviews are months away. You want to ask for a raise without feeling awkward or risking conflict.</p>
              </div>
              <p style="font-size:14px; color:var(--ink-soft); line-height:1.5;">GoalStar maps the exact progression milestones from your current desk to the signed offer letter.</p>
            `
          },
          {
            part: 2,
            title: 'The Blocker: The 60-Hour Work Week Trap',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--red);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--red); margin-bottom:4px;">FATIGUE PENALTY DETECTED</div>
                <div style="font-size:15px; font-weight:700;">Working Extra Unpaid Overtime (+4.0 Friction)</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">Taking on endless low-priority tasks burns out stamina without proving leadership value. Management assumes you are happy just staying busy.</p>
              </div>
              <div class="scenario-route-diagram">
                <div class="scenario-node-box">Current Pay</div>
                <div style="color:var(--red); font-weight:900;">&rarr;</div>
                <div class="scenario-node-box hurdle-node">Burnout Overtime (+4.0)</div>
              </div>
            `
          },
          {
            part: 3,
            title: 'A* Reroute: High-Leverage Visibility Path',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--green);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--green); margin-bottom:4px;">A* DYNAMIC SOLUTION</div>
                <div style="font-size:15px; font-weight:700;">Document High-Impact Revenue &amp; 1-on-1s</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">GoalStar bypasses 60-hour work weeks. It routes you to weekly documented project wins, competitive salary benchmarks, and scheduling a strategic career talk.</p>
              </div>
              <div class="scenario-route-diagram">
                <div class="scenario-node-box">Current Pay</div>
                <div style="color:var(--green); font-weight:900;">&rarr;</div>
                <div class="scenario-node-box highlight">Strategic Leverage (Optimal)</div>
              </div>
            `
          },
          {
            part: 4,
            title: 'Cost Profile: Lower Hours, Higher Results',
            html: `
              <div class="scenario-card-preview">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <span style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--ink);">ENERGY PROFILE</span>
                  <span style="font-size:11px; color:var(--green); font-weight:700;">TIMELINE: 30 DAYS</span>
                </div>
                <div class="mini-chart-bars">
                  <div class="mini-bar-col">
                    <div class="mini-bar bar-time" style="height: 30%;"></div>
                    <span style="font-size:9.5px; font-weight:700; color:var(--ink-muted);">Time</span>
                  </div>
                  <div class="mini-bar-col">
                    <div class="mini-bar bar-money" style="height: 15%;"></div>
                    <span style="font-size:9.5px; font-weight:700; color:var(--ink-muted);">Cost</span>
                  </div>
                  <div class="mini-bar-col">
                    <div class="mini-bar bar-effort" style="height: 35%;"></div>
                    <span style="font-size:9.5px; font-weight:700; color:var(--ink-muted);">Effort</span>
                  </div>
                  <div class="mini-bar-col">
                    <div class="mini-bar bar-risk" style="height: 20%;"></div>
                    <span style="font-size:9.5px; font-weight:700; color:var(--ink-muted);">Risk</span>
                  </div>
                </div>
                <div style="font-size:12px; color:var(--ink-muted); text-align:center;">Unnecessary overtime eliminated. Negotiation backed by factual metrics.</div>
              </div>
            `
          },
          {
            part: 5,
            title: 'Goal Achieved: $20k Raise Approved',
            html: `
              <div class="sui-verified-box">
                <div class="sui-head-row">
                  <span>Target Milestone Reached</span>
                  <span class="sui-badge-pill">Complete</span>
                </div>
                <div class="sui-details-row">
                  <div>Outcome: <strong>+$20,000 / Year Approved</strong></div>
                  <div>Status: Title upgraded, zero burned bridges or weekend fatigue.</div>
                </div>
              </div>
              <p style="font-size:13.5px; color:var(--ink-soft); margin-top:10px; line-height:1.5;">Every milestone is stamped into your personal memory log so future promotions are even faster to map.</p>
            `
          }
        ]
      },
      abroad: {
        title: 'The Global Dreamer: Moving or Studying Abroad',
        stages: [
          {
            part: 1,
            title: 'Where You Are: Dreaming of Relocating Overseas',
            html: `
              <div class="scenario-card-preview">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent); margin-bottom:4px;">INITIAL REALITY</div>
                <div style="font-size:16px; font-weight:700;">Destination Chosen: Study or Work Abroad</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">You know you want to move overseas next year, but the sheer volume of visas, university requirements, and exams feels paralyzing.</p>
              </div>
            `
          },
          {
            part: 2,
            title: 'The Blocker: Bureaucracy and Decision Paralysis',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--red);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--red); margin-bottom:4px;">48H WATCHDOG ALERT</div>
                <div style="font-size:15px; font-weight:700;">Visa &amp; Admissions Stagnation (5 Days Inactive)</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">Staring at a 15-page university requirements document causes total avoidance. Days slip by with zero progress.</p>
              </div>
            `
          },
          {
            part: 3,
            title: 'A* Reroute: Automatic Micro-Decomposition',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--green);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--green); margin-bottom:4px;">A* DYNAMIC SOLUTION</div>
                <div style="font-size:15px; font-weight:700;">Split into 15-Minute Concrete Actions</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">GoalStar fractures the massive application step into 3 simple tasks: 1) Scan passport copy, 2) Draft 3 bullet points for personal statement, 3) Request transcript.</p>
              </div>
            `
          },
          {
            part: 4,
            title: 'Cost Profile: Momentum Restored at 20 Mins / Day',
            html: `
              <div class="scenario-card-preview">
                <div style="font-size:14px; font-weight:700; color:var(--green);">Fatigue Penalty Cleared</div>
                <p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Instead of spending exhausting weekends stressing, steady 20-minute daily steps keep all deadlines on track.</p>
              </div>
            `
          },
          {
            part: 5,
            title: 'Goal Achieved: Visa &amp; Acceptance Letter in Hand',
            html: `
              <div class="sui-verified-box">
                <div class="sui-head-row">
                  <span>Application Complete</span>
                  <span class="sui-badge-pill">Verified</span>
                </div>
                <div class="sui-details-row">
                  <div>Status: <strong>Offer Accepted &amp; Visa Stamped</strong></div>
                  <div>Flight booked, paperwork verified with zero panic.</div>
                </div>
              </div>
            `
          }
        ]
      },
      saas: {
        title: 'The Builder & Maker: Shipping Side Project',
        stages: [
          {
            part: 1,
            title: 'Where You Are: Great Product Idea Ready',
            html: `
              <div class="scenario-card-preview">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent); margin-bottom:4px;">INITIAL REALITY</div>
                <div style="font-size:16px; font-weight:700;">Idea Validated: Ready to Build</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">You have a tool people want. Energy is high, but technical infrastructure decisions threaten to derail momentum.</p>
              </div>
            `
          },
          {
            part: 2,
            title: 'The Blocker: 2 Weeks Trapped in DevOps',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--red);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--red); margin-bottom:4px;">RECURRING TRAP DETECTED</div>
                <div style="font-size:15px; font-weight:700;">Custom Microservices &amp; Docker Setup (14 Days)</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">Past memory logs show 80% of abandoned projects stalled during server setup before talking to a single paying customer.</p>
              </div>
            `
          },
          {
            part: 3,
            title: 'A* Reroute: 48-Hour MVP Fast-Track',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--green);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--green); margin-bottom:4px;">A* DYNAMIC SOLUTION</div>
                <div style="font-size:15px; font-weight:700;">Deploy Minimal Working Prototype</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">The graph bypasses complex servers entirely and routes to a simple managed web app with Stripe checkout in 48 hours.</p>
              </div>
            `
          },
          {
            part: 4,
            title: 'Cost Profile: Setup Effort Cut by 80%',
            html: `
              <div class="scenario-card-preview">
                <div style="font-size:14px; font-weight:700; color:var(--green);">Zero Infrastructure Fatigue</div>
                <p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Launch happens in 2 days instead of 3 weeks. Feedback starts immediately.</p>
              </div>
            `
          },
          {
            part: 5,
            title: 'Goal Achieved: First 10 Paying Customers',
            html: `
              <div class="sui-verified-box">
                <div class="sui-head-row">
                  <span>Product Live in Market</span>
                  <span class="sui-badge-pill">Shipped</span>
                </div>
                <div class="sui-details-row">
                  <div>Milestone: <strong>Live Payments Active</strong></div>
                  <div>Shipped on time without burning out on DevOps.</div>
                </div>
              </div>
            `
          }
        ]
      },
      adhd: {
        title: 'The Overwhelmed Mind: Single Action Focus',
        stages: [
          {
            part: 1,
            title: 'Where You Are: 25-Task Overwhelm Freeze',
            html: `<div class="scenario-card-preview"><div style="font-size:15px; font-weight:700;">25 Competing To-Do Items</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Too many choices cause complete cognitive stall and task avoidance.</p></div>`
          },
          {
            part: 2,
            title: 'The Blocker: Guilt Spiral from Missing 2 Days',
            html: `<div class="scenario-card-preview" style="border-left:3px solid var(--red);"><div style="font-size:15px; font-weight:700;">Guilt &amp; Shame Blocker</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Missed a few days? Most apps punish you with broken streaks. GoalStar wipes the friction penalty without judgment.</p></div>`
          },
          {
            part: 3,
            title: 'A* Reroute: Single Next Action Isolated',
            html: `<div class="scenario-card-preview" style="border-left:3px solid var(--green);"><div style="font-size:15px; font-weight:700;">Focus On Just One Step Today</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Future complexity is hidden from view until today's single action is checked off.</p></div>`
          },
          {
            part: 4,
            title: 'Cost Profile: Activation Energy Minimized',
            html: `<div class="scenario-card-preview"><div style="font-size:14px; font-weight:700; color:var(--green);">Activation Energy: 1/5</div><p style="font-size:13px; color:var(--ink-soft); margin-top:4px;">Micro-barriers cleared. Momentum restarts in under 5 minutes.</p></div>`
          },
          {
            part: 5,
            title: 'Goal Achieved: Steady Daily Flow Restored',
            html: `<div class="sui-verified-box"><div class="sui-head-row"><span>Daily Flow Active</span><span class="sui-badge-pill">Unblocked</span></div><div class="sui-details-row">Status: <strong>Zero Shame, 100% Momentum</strong></div></div>`
          }
        ]
      },
      custom: {
        title: 'Your Custom Goal: How GoalStar Maps Your Destination',
        stages: [
          {
            part: 1,
            title: 'Step 1: Tell GoalStar Your Destination',
            html: `
              <div class="scenario-card-preview">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent); margin-bottom:4px;">STEP 1</div>
                <div style="font-size:16px; font-weight:700;">Name Any Goal You Want to Reach</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">Whether it's changing careers, moving abroad, finding a partner, or running a 10k — simply type where you are now and where you want to be.</p>
              </div>
            `
          },
          {
            part: 2,
            title: 'Step 2: Realistic Milestones Generated',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--accent);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent); margin-bottom:4px;">STEP 2</div>
                <div style="font-size:15px; font-weight:700;">Calculates Every Step in Between</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">GoalStar invents the concrete intermediate states so you never have to guess what comes after step 1.</p>
              </div>
            `
          },
          {
            part: 3,
            title: 'Step 3: Prices Friction in Time, Money, and Energy',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--accent);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--accent); margin-bottom:4px;">STEP 3</div>
                <div style="font-size:15px; font-weight:700;">Real-World Cost Weighting</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">Every line between milestones is weighted by estimated hours, financial cost, stamina, and failure risk.</p>
              </div>
            `
          },
          {
            part: 4,
            title: 'Step 4: Dynamic A* Pathfinding Highlights the Optimal Path',
            html: `
              <div class="scenario-card-preview" style="border-left: 3px solid var(--green);">
                <div style="font-family:'Space Grotesk', monospace; font-size:11px; font-weight:800; color:var(--green); margin-bottom:4px;">STEP 4</div>
                <div style="font-size:15px; font-weight:700;">Automatic Burnout Rerouting</div>
                <p style="font-size:13.5px; color:var(--ink-soft); margin:6px 0 0;">When your stamina is high, it plots direct sprint routes. When energy drops, it reroutes to steady micro-habits so you never quit.</p>
              </div>
            `
          },
          {
            part: 5,
            title: 'Step 5: Launch Your Interactive Plan',
            html: `
              <div class="sui-verified-box">
                <div class="sui-head-row">
                  <span>Ready to Map Your Goal</span>
                  <span class="sui-badge-pill">Interactive</span>
                </div>
                <div class="sui-details-row">
                  <div>Type your goal in Card 5 or click "Open in Planner" to start building immediately!</div>
                </div>
              </div>
            `
          }
        ]
      }
    };

    let activeScenarioKey = 'career';
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
      const scenario = scenarioData[activeScenarioKey] || scenarioData['career'];
      const stage = scenario.stages[currentScenarioStep];

      scenarioStepNum.textContent = `STAGE ${currentScenarioStep + 1} OF ${scenario.stages.length}`;
      scenarioScenarioTag.textContent = scenario.title.split(':')[0].toUpperCase();
      scenarioStepTitle.textContent = stage.title;
      scenarioStageContent.innerHTML = stage.html;

      stepPills.forEach((pill, idx) => {
        pill.className = 'step-pill';
        if (idx < currentScenarioStep) pill.classList.add('passed');
        if (idx === currentScenarioStep) pill.classList.add('active');
      });

      prevScenarioStepBtn.disabled = currentScenarioStep === 0;
      nextScenarioStepBtn.textContent = currentScenarioStep === scenario.stages.length - 1 ? 'Finish Walkthrough' : 'Next Stage';
    }

    """

    if not scenario_js_pattern.search(html):
        print("[ERR] scenario_js_pattern not matched in home.html!")
        sys.exit(1)
    html = scenario_js_pattern.sub(new_scenario_js, html)
    print("[OK] Updated scenarioData object and renderScenarioStage logic.")

    # Also make sure openFullPlannerBtn handles custom goals:
    open_planner_old = "document.getElementById('openFullPlannerBtn')"
    if open_planner_old in html:
        pass # already present

    with open(home_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("[OK] Successfully wrote updated home.html!")

if __name__ == '__main__':
    main()
