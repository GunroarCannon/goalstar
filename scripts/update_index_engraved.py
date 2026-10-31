path = r'C:\Users\hmmm\goalstar-recall\index.html'

with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace plain icon buttons with engraved switches in topbar
old_toggles = '''    <button id="themeToggleBtn" class="theme-toggle-btn icon" title="Toggle Dark/Light Mode" aria-label="Toggle Dark Mode">🌙</button>
    <button id="soundToggleBtn" class="sound-toggle-btn icon" title="Toggle Sound Effects" aria-label="Toggle Sound">🔊</button>'''

new_toggles = '''    <!-- Engraved Pill Switches (Reference Image 0) -->
    <div class="engraved-switch" id="themeSwitch" role="button" tabindex="0" title="Toggle Light / Dark Mode">
      <div class="switch-track">
        <span class="track-label left">LIGHT</span>
        <span class="track-label right">DARK</span>
        <div class="switch-knob"></div>
      </div>
    </div>
    <div class="engraved-switch active" id="soundSwitch" role="button" tabindex="0" title="Toggle Snappy Sound">
      <div class="switch-track">
        <span class="track-label left">MUTE</span>
        <span class="track-label right">AUDIO</span>
        <div class="switch-knob"></div>
      </div>
    </div>
    <button id="themeToggleBtn" class="theme-toggle-btn" hidden></button>
    <button id="soundToggleBtn" class="sound-toggle-btn" hidden></button>'''

if old_toggles in html:
    html = html.replace(old_toggles, new_toggles, 1)

# Add engraved-btn to nav-home-btn, newGoalBtn, dreamBtn, searchBtn, tourBtn, loginBtn
html = html.replace('class="nav-home-btn"', 'class="nav-home-btn engraved-btn"')
html = html.replace('id="newGoalBtn" title="New goal"', 'id="newGoalBtn" class="engraved-btn" title="New goal"')
html = html.replace('id="dreamBtn" class="primary"', 'id="dreamBtn" class="primary engraved-btn"')
html = html.replace('id="searchBtn" class="gold"', 'id="searchBtn" class="gold engraved-btn"')
html = html.replace('class="tour-nav-btn"', 'class="tour-nav-btn engraved-btn"')
html = html.replace('class="login-btn"', 'class="login-btn engraved-btn"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated index.html with engraved switches and buttons')
