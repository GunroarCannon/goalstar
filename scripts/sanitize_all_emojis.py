import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update index.html
with open('goalstar-recall/index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

# Replace Groq pane in settings
groq_old = '''        <div class="pane" data-pane="groq">
          <label>API key <input type="password" name="groq.apiKey" placeholder="gsk_…" autocomplete="off"></label>
          <label>Model <input name="groq.model" list="groqModels" placeholder="openai/gpt-oss-20b"></label>
          <datalist id="groqModels">
            <option value="openai/gpt-oss-20b">
            <option value="openai/gpt-oss-120b">
            <option value="qwen/qwen3.8-27b">
          </datalist>
          <p class="muted small">Fast and has a free tier. Your key is stored only in this browser. Get one at console.groq.com.</p>
        </div>'''

groq_new = '''        <div class="pane" data-pane="groq">
          <div class="configured-token-box" style="padding: 10px 14px; background: rgba(16, 185, 129, 0.08); border: 1.5px solid rgba(16, 185, 129, 0.3); border-radius: 6px; margin-bottom: 12px; font-size: 13px; line-height: 1.4;">
            <div style="font-weight: 700; color: #047857; display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
              <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981;"></span>
              Token Pre-Configured (Active)
            </div>
            <span class="muted small" style="color: var(--ink-soft);">Loaded automatically from <code>royal-ramble/.env</code>. Instant high-speed dreaming is active without needing manual token input.</span>
          </div>
          <label>Model <input name="groq.model" list="groqModels" placeholder="openai/gpt-oss-120b"></label>
          <datalist id="groqModels">
            <option value="openai/gpt-oss-120b">
            <option value="openai/gpt-oss-20b">
            <option value="qwen/qwen3.8-27b">
          </datalist>
          <p class="muted small">High-speed inference on Groq LPU with zero token setup required.</p>
        </div>'''

if groq_old in idx_content:
    idx_content = idx_content.replace(groq_old, groq_new)
else:
    # regex fallback for groq pane
    idx_content = re.sub(
        r'<div class="pane" data-pane="groq">.*?<\/div>\s*<div class="pane" data-pane="claude">',
        groq_new + '\n        <div class="pane" data-pane="claude">',
        idx_content,
        flags=re.DOTALL
    )

# Replace all emojis in index.html
replacements_index = [
    ('>☰<', '><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg><'),
    ('🏠 Home', 'Home'),
    ('✦ Dream…', 'Dream…'),
    ('★ Search', 'Search'),
    ('🎓 Tour', 'Tour'),
    ('🔑 Log In', 'Log In'),
    ('>⚙️<', '><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg><'),
    ('★ Best path', 'Best Path'),
    ('🎓 Replay Product Tour', 'Replay Product Tour'),
    ('<div class="tuesday-icon">🧠</div>', '<div class="tuesday-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a5 5 0 0 1 5 5c0 2.2-1.4 4.1-3.4 4.8.4.7.4 1.5.4 2.2H10c0-.7 0-1.5.4-2.2C8.4 11.1 7 9.2 7 7a5 5 0 0 1 5-5z"/><line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="21" x2="14" y2="21"/></svg></div>'),
    ('★ Search budget', 'Search Budget'),
    ('🔑 Connect &amp; Sync Portable Memory', 'Connect &amp; Sync Portable Memory'),
    ('✕', '&times;'),
    ('<div class="opt-icon">⚡</div>', '<div class="opt-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>'),
    ('<div class="opt-icon">🌊</div>', '<div class="opt-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M2 12c2.5-3 5-3 7.5 0s5 3 7.5 0 5-3 7 0M2 18c2.5-3 5-3 7.5 0s5 3 7.5 0 5-3 7 0"/></svg></div>'),
    ('<div class="opt-icon">🧠</div>', '<div class="opt-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="6"/><circle cx="5" cy="8" r="3"/><circle cx="19" cy="8" r="3"/><circle cx="8" cy="19" r="2.5"/><circle cx="16" cy="19" r="2.5"/></svg></div>'),
]

for old, new in replacements_index:
    idx_content = idx_content.replace(old, new)

with open('goalstar-recall/index.html', 'w', encoding='utf-8') as f:
    f.write(idx_content)

print("index.html sanitized of emojis and Groq token field removed!")

# 2. Update js/tour.js
with open('goalstar-recall/js/tour.js', 'r', encoding='utf-8') as f:
    tour_content = f.read()

replacements_tour = [
    ("🔑 Step 1: Log In & Carry Your Memory", "Step 1: Log In & Carry Your Memory"),
    ("✦ Step 2: Choose or Dream Any Goal", "Step 2: Choose or Dream Any Goal"),
    ("🧭 Step 3: Click Nodes to See Action Checklists", "Step 3: Click Nodes to See Action Checklists"),
    ("🎚️ Step 4: Drag Sliders to Reroute Instantly", "Step 4: Drag Sliders to Reroute Instantly"),
    ("⚡ Step 5: Log Blockers & 48h Watchdog", "Step 5: Log Blockers & 48h Watchdog"),
    ("📜 Step 6: Stamp Verifiable Proof on Sui", "Step 6: Stamp Verifiable Proof on Sui"),
    ('<div class="sketch-pin">📌</div>', '<div class="sketch-pin"><svg width="16" height="16" viewBox="0 0 24 24" fill="#d97706"><circle cx="12" cy="7" r="5"/><polygon points="12,12 12,22 10,14"/></svg></div>'),
    ('🚀 Open Interactive Planner', 'Open Planner'),
    ('Next ➔', 'Next'),
]

for old, new in replacements_tour:
    tour_content = tour_content.replace(old, new)

with open('goalstar-recall/js/tour.js', 'w', encoding='utf-8') as f:
    f.write(tour_content)

print("js/tour.js sanitized of emojis!")

# 3. Update js/theme.js
with open('goalstar-recall/js/theme.js', 'r', encoding='utf-8') as f:
    theme_content = f.read()

theme_content = theme_content.replace(
    "btn.innerHTML = isDark ? '☀️ <span class=\"txt\">Light</span>' : '🌙 <span class=\"txt\">Dark</span>';",
    "btn.innerHTML = isDark ? '<span class=\"txt\">Light</span>' : '<span class=\"txt\">Dark</span>';"
)

with open('goalstar-recall/js/theme.js', 'w', encoding='utf-8') as f:
    f.write(theme_content)

print("js/theme.js sanitized of emojis!")

# 4. Update js/sound.js
with open('goalstar-recall/js/sound.js', 'r', encoding='utf-8') as f:
    sound_content = f.read()

sound_content = sound_content.replace(
    "btn.innerHTML = this.enabled ? '🔊 <span class=\"txt\">Sound</span>' : '🔇 <span class=\"txt\">Muted</span>';",
    "btn.innerHTML = this.enabled ? '<span class=\"txt\">Sound</span>' : '<span class=\"txt\">Muted</span>';"
)

with open('goalstar-recall/js/sound.js', 'w', encoding='utf-8') as f:
    f.write(sound_content)

print("js/sound.js sanitized of emojis!")
