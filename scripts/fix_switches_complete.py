import re

# 1. Update js/theme.js
theme_js_code = '''// GoalStar Dark & Light Theme Manager
// Synchronizes chalkboard / night paper mode across App & Landing page
import { sound } from './sound.js';

export class ThemeManager {
  constructor() {
    this.theme = localStorage.getItem('goalstar_theme') || 'light';
    this._listenerAttached = false;
  }

  init() {
    const saved = localStorage.getItem('goalstar_theme');
    if (saved) {
      this.theme = saved;
    } else if (document.body.dataset.paper === 'night') {
      this.theme = 'dark';
    }
    this.applyTheme(this.theme);
    this.attachListeners();
  }

  attachListeners() {
    if (this._listenerAttached || typeof document === 'undefined') return;
    this._listenerAttached = true;

    // Single delegated listener on document for all theme switches & buttons
    document.addEventListener('click', (e) => {
      const sw = e.target.closest('#themeSwitch, .theme-switch, .theme-toggle-btn, #themeToggleBtn');
      if (sw) {
        e.preventDefault();
        e.stopPropagation();
        this.toggle();
      }
    });

    // Keyboard accessibility (Space / Enter)
    document.addEventListener('keydown', (e) => {
      if ((e.key === ' ' || e.key === 'Enter') && e.target.closest('#themeSwitch, .theme-switch')) {
        e.preventDefault();
        this.toggle();
      }
    });
  }

  toggle() {
    this.theme = this.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('goalstar_theme', this.theme);
    sound.play('toggle');
    this.applyTheme(this.theme);
  }

  applyTheme(theme) {
    const isDark = theme === 'dark';
    document.documentElement.classList.toggle('dark-mode', isDark);
    document.body.dataset.paper = isDark ? 'night' : 'lined';

    if (typeof window !== 'undefined' && window.data && window.data.settings && window.data.settings.display) {
      window.data.settings.display.paper = isDark ? 'night' : 'lined';
    }

    // Update all engraved switches in DOM without adding duplicate listeners
    document.querySelectorAll('#themeSwitch, .theme-switch').forEach(sw => {
      sw.classList.toggle('active', isDark);
      const label = sw.querySelector('.track-label');
      if (label) {
        label.textContent = isDark ? 'DARK' : 'LIGHT';
      }
      sw.setAttribute('aria-checked', isDark ? 'true' : 'false');
      sw.title = isDark ? 'Theme: DARK (Click for Light)' : 'Theme: LIGHT (Click for Dark)';
    });

    // Legacy fallback buttons
    document.querySelectorAll('.theme-toggle-btn, #themeToggleBtn').forEach(btn => {
      btn.innerHTML = isDark ? '☀️ <span class="txt">Light</span>' : '🌙 <span class="txt">Dark</span>';
      btn.title = isDark ? 'Switch to Light Notebook' : 'Switch to Night Chalkboard';
      btn.classList.toggle('active', isDark);
    });
  }
}

export const theme = new ThemeManager();
if (typeof window !== 'undefined') {
  window.theme = theme;
}
'''

with open(r'C:\Users\hmmm\goalstar-recall\js\theme.js', 'w', encoding='utf-8') as f:
    f.write(theme_js_code)
print('[OK] Updated js/theme.js')

# 2. Update js/sound.js (Fix duplicate event listeners in updateUI / attachListeners)
with open(r'C:\Users\hmmm\goalstar-recall\js\sound.js', 'r', encoding='utf-8') as f:
    sound_js = f.read()

# Replace updateUI in sound.js so it only updates DOM and NEVER adds event listeners
old_update_ui = r'updateUI\(\)\s*\{[\s\S]*?btns\.forEach\(btn => \{[\s\S]*?\}\);\s*\}'
new_update_ui = '''updateUI() {
    document.querySelectorAll('#soundSwitch, .sound-switch').forEach(sw => {
      sw.classList.toggle('active', this.enabled);
      const label = sw.querySelector('.track-label');
      if (label) {
        label.textContent = this.enabled ? 'AUDIO' : 'MUTE';
      }
      sw.setAttribute('aria-checked', this.enabled ? 'true' : 'false');
      sw.title = this.enabled ? 'Sound: AUDIO ON (Click to Mute)' : 'Sound: MUTED (Click for Audio)';
    });

    document.querySelectorAll('.sound-toggle-btn, #soundToggleBtn').forEach(btn => {
      btn.innerHTML = this.enabled ? '🔊 <span class="txt">Sound</span>' : '🔇 <span class="txt">Muted</span>';
      btn.title = this.enabled ? 'Mute sound effects' : 'Enable snappy sound effects';
      btn.classList.toggle('muted', !this.enabled);
    });
  }'''

sound_js = re.sub(old_update_ui, new_update_ui, sound_js)

# Replace attachListeners in sound.js to use clean single delegated listener
old_attach_listeners = r'attachListeners\(\)\s*\{[\s\S]*?this\.updateUI\(\);\s*\}'
new_attach_listeners = '''attachListeners() {
    if (typeof window === 'undefined' || this._listenersAttached) return;
    this._listenersAttached = true;

    // Attach unlock on first interaction
    const unlock = () => {
      this.init();
      window.removeEventListener('click', unlock);
      window.removeEventListener('keydown', unlock);
    };
    window.addEventListener('click', unlock, { once: true });
    window.addEventListener('keydown', unlock, { once: true });

    // Global listener for crunchy tactile clicks and switches
    document.addEventListener('click', (e) => {
      const sw = e.target.closest('#soundSwitch, .sound-switch, .sound-toggle-btn, #soundToggleBtn');
      if (sw) {
        e.preventDefault();
        e.stopPropagation();
        this.toggle();
        return;
      }

      const target = e.target.closest('button, .node, .checkbox, input[type="radio"], input[type="checkbox"], a.brand, a.nav-home-btn, .mini-ink-btn, .engraved-btn');
      if (target) {
        if (target.matches('.node, input[type="checkbox"]')) {
          this.play('pop');
        } else {
          this.play('click');
        }
      }
    });

    // Keyboard accessibility for sound switch
    document.addEventListener('keydown', (e) => {
      if ((e.key === ' ' || e.key === 'Enter') && e.target.closest('#soundSwitch, .sound-switch')) {
        e.preventDefault();
        this.toggle();
      }
    });

    // Slider crunchy feedback
    document.addEventListener('input', (e) => {
      if (e.target.matches('input[type="range"]')) {
        this.play('crunch');
      }
    });

    this.updateUI();
  }'''

sound_js = re.sub(old_attach_listeners, new_attach_listeners, sound_js)

with open(r'C:\Users\hmmm\goalstar-recall\js\sound.js', 'w', encoding='utf-8') as f:
    f.write(sound_js)
print('[OK] Updated js/sound.js')

# 3. Update css/style.css for .engraved-switch, .switch-track, .switch-knob, .track-label
with open(r'C:\Users\hmmm\goalstar-recall\css\style.css', 'r', encoding='utf-8') as f:
    style_css = f.read()

old_switch_css = r'/\* Engraved Recessed Switches \(Reference Image 0\) \*/[\s\S]*?/\* Tactile Engraved Buttons'

new_switch_css = '''/* Engraved Recessed Switches (Reference Image 0) */
.engraved-switch {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  font-family: 'Space Grotesk', system-ui, sans-serif;
  text-decoration: none;
  outline: none;
  vertical-align: middle;
}
.switch-track {
  position: relative;
  width: 104px;
  height: 32px;
  background: #ded7c3;
  border-radius: 99px;
  border: 2px solid var(--ink);
  box-shadow: 
    inset 2.5px 3.5px 6px rgba(0, 0, 0, 0.28),
    inset -2px -2px 4px rgba(255, 255, 255, 0.75),
    0 1.5px 0 rgba(255, 255, 255, 0.4);
  box-sizing: border-box;
  overflow: hidden;
  transition: background 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}
body[data-paper='night'] .switch-track,
.dark-mode .switch-track {
  background: #111622;
  border-color: #f59e0b;
  box-shadow: 
    inset 3px 4px 7px rgba(0, 0, 0, 0.75),
    inset -1.5px -1.5px 3px rgba(255, 255, 255, 0.08),
    0 1px 0 rgba(255, 255, 255, 0.05);
}

/* Debossed Label centered in the open trench (Zero Overlap with Knob) */
.track-label {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 68px;
  right: 5px; /* Inactive (Knob on left): text sits in open right trench */
  left: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 1.4px;
  color: var(--ink);
  opacity: 0.88;
  text-shadow: 
    1px 1px 0 rgba(255, 255, 255, 0.8),
    -1px -1px 0 rgba(0, 0, 0, 0.2);
  pointer-events: none;
  z-index: 1;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
body[data-paper='night'] .track-label,
.dark-mode .track-label {
  color: #f59e0b;
  text-shadow: 
    1px 1px 0 rgba(0, 0, 0, 0.9),
    -1px -1px 0 rgba(255, 255, 255, 0.1);
}

/* When Switch is Active: knob slides right, text moves to open left trench */
.engraved-switch.active .track-label {
  right: auto;
  left: 5px;
}

/* Tactile Raised Sliding Knob (Reference Image 0) */
.switch-knob {
  position: absolute;
  top: 3px;
  left: 4px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffffff 0%, #ded7c3 100%);
  border: 1.5px solid var(--ink);
  box-shadow: 
    2px 3px 5px rgba(0, 0, 0, 0.25),
    -1px -1px 2px rgba(255, 255, 255, 0.9),
    inset 1px 1px 1.5px rgba(255, 255, 255, 0.9),
    inset -1px -1.5px 2px rgba(0, 0, 0, 0.15);
  z-index: 2;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.25s ease;
}
.engraved-switch.active .switch-knob {
  transform: translateX(68px);
}
body[data-paper='night'] .switch-knob,
.dark-mode .switch-knob {
  background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
  border-color: #f59e0b;
  box-shadow: 
    2px 3px 6px rgba(0, 0, 0, 0.6),
    -1px -1px 2px rgba(255, 255, 255, 0.1),
    inset 1px 1px 2px rgba(255, 255, 255, 0.2),
    inset -1px -1.5px 3px rgba(0, 0, 0, 0.5);
}

/* Tactile Engraved Buttons'''

style_css = re.sub(old_switch_css, new_switch_css, style_css)

with open(r'C:\Users\hmmm\goalstar-recall\css\style.css', 'w', encoding='utf-8') as f:
    f.write(style_css)
print('[OK] Updated css/style.css')

# 4. Update home.html switches
with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    home_html = f.read()

# Replace the two switches with clean track-label structure
old_home_theme_sw = r'<div class="engraved-switch" id="themeSwitch"[\s\S]*?</div>\s*</div>'
new_home_theme_sw = '''<div class="engraved-switch" id="themeSwitch" role="button" tabindex="0" title="Toggle Light / Dark Mode">
        <div class="switch-track">
          <div class="switch-knob"></div>
          <span class="track-label">LIGHT</span>
        </div>
      </div>'''

home_html = re.sub(old_home_theme_sw, new_home_theme_sw, home_html, count=1)

old_home_sound_sw = r'<div class="engraved-switch active" id="soundSwitch"[\s\S]*?</div>\s*</div>'
new_home_sound_sw = '''<div class="engraved-switch active" id="soundSwitch" role="button" tabindex="0" title="Toggle Snappy Sound">
        <div class="switch-track">
          <div class="switch-knob"></div>
          <span class="track-label">AUDIO</span>
        </div>
      </div>'''

home_html = re.sub(old_home_sound_sw, new_home_sound_sw, home_html, count=1)

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'w', encoding='utf-8') as f:
    f.write(home_html)
print('[OK] Updated home.html switches')

# 5. Update index.html switches
with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

old_idx_theme_sw = r'<div class="engraved-switch" id="themeSwitch"[\s\S]*?</div>\s*</div>'
new_idx_theme_sw = '''<div class="engraved-switch" id="themeSwitch" role="button" tabindex="0" title="Toggle Light / Dark Mode">
      <div class="switch-track">
        <div class="switch-knob"></div>
        <span class="track-label">LIGHT</span>
      </div>
    </div>'''

index_html = re.sub(old_idx_theme_sw, new_idx_theme_sw, index_html, count=1)

old_idx_sound_sw = r'<div class="engraved-switch active" id="soundSwitch"[\s\S]*?</div>\s*</div>'
new_idx_sound_sw = '''<div class="engraved-switch active" id="soundSwitch" role="button" tabindex="0" title="Toggle Snappy Sound">
      <div class="switch-track">
        <div class="switch-knob"></div>
        <span class="track-label">AUDIO</span>
      </div>
    </div>'''

index_html = re.sub(old_idx_sound_sw, new_idx_sound_sw, index_html, count=1)

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print('[OK] Updated index.html switches')
print('=== ALL FIXES APPLIED SUCCESSFULLY! ===')
