import os
import re

home_path = r'C:\Users\hmmm\goalstar-recall\home.html'

with open(home_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Hero Title and Underline:
# Replace <h1 class="hero-title">A* Pathfinding for Life Goals, Backed by <span class="hl">Portable Memory</span></h1>
# and its CSS with the calligraphic ink swash SVG.
old_title_pattern = r'<h1 class="hero-title">A\* Pathfinding for Life Goals, Backed by <span class="hl">Portable Memory</span></h1>'

new_title_html = '''<h1 class="hero-title">
          A* Pathfinding for Life Goals, Backed by 
          <span class="ink-hl-wrap">
            <span class="ink-hl-text">Portable Memory</span>
            <svg class="ink-swash-svg" viewBox="0 0 310 28" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <!-- Calligraphic Ink Brush Swash (Image 1 reference) -->
              <path d="M 6 18 C 35 15, 75 22, 120 21 C 170 20, 220 12, 268 9 C 274 8.5, 278 11, 274 13 C 240 21, 190 25, 135 25 C 80 25, 30 22, 6 18 Z" fill="#d97706" />
              <path d="M 18 19 C 70 23, 140 24, 210 18 C 245 15, 270 11, 277 9" stroke="#b45309" stroke-width="2.5" stroke-linecap="round" opacity="0.6" />
              <!-- Ink Splatter Droplets -->
              <circle cx="284" cy="6" r="2.2" fill="#d97706" opacity="0.8" />
              <circle cx="290" cy="12" r="1.5" fill="#d97706" opacity="0.6" />
              <circle cx="276" cy="4" r="1.1" fill="#d97706" opacity="0.5" />
              <circle cx="3" cy="19" r="1.5" fill="#d97706" opacity="0.5" />
            </svg>
          </span>
        </h1>'''

content = re.sub(old_title_pattern, new_title_html, content)

# 2. Shorten Hero Paragraph (less text, more punch):
old_hero_desc = r'<p class="hero-desc">\s*Stop hitting roadblocks and starting over from a blank page\. GoalStar remembers your real-world stamina, learns your friction patterns, and dynamically reroutes your path to what actually works\.\s*</p>'

new_hero_desc = '''<p class="hero-desc">
          Goals fail when friction builds up. GoalStar computes your lowest-cost path forward, learns your real-world stamina, and reroutes around roadblocks.
        </p>'''

content = re.sub(old_hero_desc, new_hero_desc, content)

# 3. Refined Anatomical Face Silhouette (Replace clunky path in sculpture-svg):
old_face_pattern = r'<path d="M 65 240 C 65 200, 75 190, 85 170 C 75 155, 68 135, 70 100 C 72 65, 95 35, 140 35 C 190 35, 205 65, 205 95 C 205 105, 212 112, 220 120 C 212 125, 205 135, 205 145 C 208 160, 195 180, 200 240 Z"\s+fill="#fcf8ec" stroke="#2a2d3e" stroke-width="2\.5" filter="url\(#deepCutShadow\)" />'

new_face_svg = '''<!-- Layer 3: Refined Classical Silhouette Profile (Anatomical Brow, Nose, Lips, Chin) -->
              <path d="M 68 245 C 66 215, 63 190, 64 170 C 65 130, 74 72, 114 42 C 134 28, 162 30, 178 46 C 191 58, 196 76, 198 90 C 196 95, 194 97, 195 100 C 199 105, 213 115, 222 122 C 218 126, 206 127, 202 129 C 203 132, 209 135, 212 138 C 209 141, 202 142, 203 144 C 206 147, 209 149, 210 151 C 207 154, 201 155, 201 158 C 205 163, 210 167, 210 171 C 207 177, 197 183, 187 191 C 173 199, 160 206, 160 221 C 160 231, 166 239, 175 245 Z"
                    fill="#fcf8ec" stroke="#2a2d3e" stroke-width="2.2" filter="url(#deepCutShadow)" />
              
              <!-- Ink Splatter Accent near sculpture base -->
              <g opacity="0.45" fill="#2a2d3e">
                <circle cx="230" cy="235" r="3" />
                <circle cx="238" cy="240" r="1.8" />
                <circle cx="225" cy="242" r="1.2" />
                <circle cx="55" cy="230" r="2.5" />
                <circle cx="48" cy="236" r="1.5" />
              </g>'''

content = re.sub(old_face_pattern, new_face_svg, content)

# 4. Add Humaaan Hero Accent alongside CTA row:
old_cta_row = r'<div class="hero-cta-row">[\s\S]*?</div>\s*</div>\s*<div class="hero-right">'
new_cta_row = '''<div class="hero-cta-row">
          <button id="heroLaunchBtn" class="engraved-btn launch-btn" style="font-size: 19px !important; padding: 10px 24px !important;">🚀 Open Interactive Planner</button>
          <a href="#simulator" class="engraved-btn" style="font-size: 16px; text-decoration: none;">⚡ Test A* In Browser</a>
        </div>
        
        <!-- Humaaan Hero Avatar Card (Fast-loading WebP) -->
        <div class="hero-humaaan-badge">
          <img src="assets/humaaans/webp/hu_stand_24.webp" alt="Planner Human" class="hero-avatar-img" width="56" height="88" loading="lazy">
          <div class="hero-avatar-text">
            <strong>Real-Life Goal Pathing</strong>
            <span>Adapts to human stamina, fatigue, and motivation drops.</span>
          </div>
          <!-- Ink blotch stamp -->
          <svg class="ink-blotch-mini" viewBox="0 0 40 40" aria-hidden="true">
            <path d="M20 5 C28 3, 36 10, 35 18 C38 25, 36 33, 28 36 C20 38, 8 36, 5 28 C2 20, 8 10, 20 5 Z" fill="#2a2d3e" opacity="0.12" />
          </svg>
        </div>
      </div>

      <div class="hero-right">'''

content = re.sub(old_cta_row, new_cta_row, content)

# 5. Overhaul 5 Use Case Cards: Shorten Paragraphs + Embed Humaaans figures + Ink Splatters!
# We will replace each uc-grid with a punchy 2-column layout:
# Left: Short problem bullet + Short solution bullet + Stat pill + Button
# Right: Humaaan Illustration

uc1_old = r'<div class="uc-grid">[\s\S]*?</div>\s*<div class="uc-footer">[\s\S]*?</div>\s*</article>\s*</div>\s*<!-- Use Case 2'
uc1_new = '''<div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item hurdle">
                  <span class="bullet-tag">❌ Hurdle</span>
                  <p><strong>14 days trapped in DevOps:</strong> Wrestling Docker, Kubernetes, and VPC configs before testing a single product idea.</p>
                </div>
                <div class="uc-bullet-item fix">
                  <span class="bullet-tag">✓ A* Fix</span>
                  <p><strong>DevOps friction (+3.5) detected:</strong> Instantly reroutes through zero-config serverless. Ships in 48 hours.</p>
                </div>
                <div class="uc-footer-row">
                  <span class="uc-stat-pill">✨ -12 Days Saved · Shipped in 48h</span>
                  <button class="engraved-btn scenario-launch-btn" data-scenario="Launch SaaS" style="font-size: 14px;">Try This Scenario ➔</button>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_stand_1.webp" alt="Founder Humaaan" class="uc-humaaan-img" width="130" height="200" loading="lazy">
                <div class="humaaan-caption">Solo Founder</div>
              </div>
            </div>
          </article>
        </div>

        <!-- Use Case 2'''

content = re.sub(uc1_old, uc1_new, content)

uc2_old = r'<div class="uc-grid">[\s\S]*?</div>\s*<div class="uc-footer">[\s\S]*?</div>\s*</article>\s*</div>\s*<!-- Use Case 3'
uc2_new = '''<div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item hurdle">
                  <span class="bullet-tag">❌ Hurdle</span>
                  <p><strong>Blank-page thesis paralysis:</strong> Staring at a 40-page literature review for 5 days until panic sets in.</p>
                </div>
                <div class="uc-bullet-item fix">
                  <span class="bullet-tag">✓ A* Fix</span>
                  <p><strong>48h Watchdog trigger:</strong> Decomposes intimidating chapters into three 15-minute micro-actions.</p>
                </div>
                <div class="uc-footer-row">
                  <span class="uc-stat-pill">⚡ +92% Momentum Restored · 0 Panic</span>
                  <button class="engraved-btn scenario-launch-btn" data-scenario="Write Thesis" style="font-size: 14px;">Try This Scenario ➔</button>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_sit_3.webp" alt="Researcher Humaaan" class="uc-humaaan-img" width="140" height="170" loading="lazy">
                <div class="humaaan-caption">Grad Researcher</div>
              </div>
            </div>
          </article>
        </div>

        <!-- Use Case 3'''

content = re.sub(uc2_old, uc2_new, content)

uc3_old = r'<div class="uc-grid">[\s\S]*?</div>\s*<div class="uc-footer">[\s\S]*?</div>\s*</article>\s*</div>\s*<!-- Use Case 4'
uc3_new = '''<div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item hurdle">
                  <span class="bullet-tag">❌ Hurdle</span>
                  <p><strong>Milestone disputes:</strong> Deliverables and sign-off dates lost across messy Slack threads and email chains.</p>
                </div>
                <div class="uc-bullet-item fix">
                  <span class="bullet-tag">✓ A* Fix</span>
                  <p><strong>Onchain Proof of Work:</strong> Milestones immutably stamped to Sui Mainnet with verifiable cryptographic proof.</p>
                </div>
                <div class="uc-footer-row">
                  <span class="uc-stat-pill">📜 Sui Mainnet Stamped · Irrefutable</span>
                  <button class="engraved-btn scenario-launch-btn" data-scenario="Client Contract" style="font-size: 14px;">Try This Scenario ➔</button>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_stand_4.webp" alt="Consultant Humaaan" class="uc-humaaan-img" width="130" height="200" loading="lazy">
                <div class="humaaan-caption">Agency Consultant</div>
              </div>
            </div>
          </article>
        </div>

        <!-- Use Case 4'''

content = re.sub(uc3_old, uc3_new, content)

uc4_old = r'<div class="uc-grid">[\s\S]*?</div>\s*<div class="uc-footer">[\s\S]*?</div>\s*</article>\s*</div>\s*<!-- Use Case 5'
uc4_new = '''<div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item hurdle">
                  <span class="bullet-tag">❌ Hurdle</span>
                  <p><strong>To-do list freeze:</strong> 25 items cause overwhelm. Missing 2 days triggers shame and abandonment.</p>
                </div>
                <div class="uc-bullet-item fix">
                  <span class="bullet-tag">✓ A* Fix</span>
                  <p><strong>Single-action focus:</strong> Shows exactly ONE next step. Missed 3 days? Zero guilt—it reroutes from where you are.</p>
                </div>
                <div class="uc-footer-row">
                  <span class="uc-stat-pill">🧩 Zero-Shame Recalculation</span>
                  <button class="engraved-btn scenario-launch-btn" data-scenario="Focus Routine" style="font-size: 14px;">Try This Scenario ➔</button>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_sit_1.webp" alt="Focused Humaaan" class="uc-humaaan-img" width="140" height="170" loading="lazy">
                <div class="humaaan-caption">Deep Work Focus</div>
              </div>
            </div>
          </article>
        </div>

        <!-- Use Case 5'''

content = re.sub(uc4_old, uc4_new, content)

uc5_old = r'<div class="uc-grid">[\s\S]*?</div>\s*<div class="uc-footer">[\s\S]*?</div>\s*</article>\s*</div>\s*</div>\s*</section>'
uc5_new = '''<div class="uc-content-flex">
              <div class="uc-details">
                <div class="uc-bullet-item hurdle">
                  <span class="bullet-tag">❌ Hurdle</span>
                  <p><strong>Over-training collapse:</strong> Rigid training schedules ignore fatigue, leading to injury and quitting week 3.</p>
                </div>
                <div class="uc-bullet-item fix">
                  <span class="bullet-tag">✓ A* Fix</span>
                  <p><strong>Stamina-weighted routing:</strong> Walrus Memory tracks fatigue limits, shifting high-friction intervals to rest days.</p>
                </div>
                <div class="uc-footer-row">
                  <span class="uc-stat-pill">🏃 100% Finish Rate · Injury Prevented</span>
                  <button class="engraved-btn launch-btn" id="card5LaunchBtn" style="font-size: 14px;">Launch Full Planner ➔</button>
                </div>
              </div>
              <div class="uc-humaaan-frame">
                <img src="assets/humaaans/webp/hu_stand_14.webp" alt="Athlete Humaaan" class="uc-humaaan-img" width="130" height="200" loading="lazy">
                <div class="humaaan-caption">Habit Builder</div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>'''

content = re.sub(uc5_old, uc5_new, content)

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated home.html content with shortened paragraphs, ink swash underline, refined face, and humaaans!')
