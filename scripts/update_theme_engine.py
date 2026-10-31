import sys

# 1. Update js/theme.js with 4-theme management
theme_js_code = """// GoalStar Harmonious Multi-Theme Engine
// Supports 4 curated aesthetic themes: Notebook, Chalkboard (Night), Blueprint, Monograph
import { sound } from './sound.js';

export const THEME_PRESETS = {
  notebook: { id: 'notebook', name: 'Notebook (Warm Paper)', paper: 'lined', isDark: false },
  night: { id: 'night', name: 'Chalkboard (Night)', paper: 'night', isDark: true },
  blueprint: { id: 'blueprint', name: 'Blueprint (Technical Navy)', paper: 'blueprint', isDark: true },
  monograph: { id: 'monograph', name: 'Monograph (Vintage Sepia)', paper: 'monograph', isDark: false }
};

export class ThemeManager {
  constructor() {
    this.currentPreset = localStorage.getItem('goalstar_theme_preset') || 'notebook';
    this._listenerAttached = false;
  }

  init() {
    const saved = localStorage.getItem('goalstar_theme_preset') || (localStorage.getItem('goalstar_theme') === 'dark' ? 'night' : 'notebook');
    this.applyTheme(saved);
    this.attachListeners();
  }

  attachListeners() {
    if (this._listenerAttached || typeof document === 'undefined') return;
    this._listenerAttached = true;

    // Toggle switch handler (cycles between notebook and night)
    document.addEventListener('click', (e) => {
      const sw = e.target.closest('#themeSwitch, .theme-switch, .theme-toggle-btn, #themeToggleBtn');
      if (sw) {
        e.preventDefault();
        e.stopPropagation();
        this.toggle();
      }
    });

    // Theme select dropdown handler
    document.addEventListener('change', (e) => {
      if (e.target.matches('#themeSelect, .theme-select')) {
        this.setPreset(e.target.value);
      }
    });
  }

  toggle() {
    const next = this.currentPreset === 'night' || this.currentPreset === 'blueprint' ? 'notebook' : 'night';
    this.setPreset(next);
    sound.play('toggle');
  }

  setPreset(presetId) {
    if (!THEME_PRESETS[presetId]) presetId = 'notebook';
    this.currentPreset = presetId;
    localStorage.setItem('goalstar_theme_preset', presetId);
    localStorage.setItem('goalstar_theme', THEME_PRESETS[presetId].isDark ? 'dark' : 'light');
    this.applyTheme(presetId);
  }

  applyTheme(presetId) {
    const preset = THEME_PRESETS[presetId] || THEME_PRESETS.notebook;
    this.currentPreset = preset.id;
    const isDark = preset.isDark;

    document.documentElement.classList.toggle('dark-mode', isDark);
    document.documentElement.setAttribute('data-theme-preset', preset.id);
    document.body.dataset.paper = preset.paper;

    if (typeof window !== 'undefined' && window.data && window.data.settings && window.data.settings.display) {
      window.data.settings.display.paper = preset.paper;
    }

    // Update pill switches
    document.querySelectorAll('#themeSwitch, .theme-switch').forEach(sw => {
      sw.classList.toggle('active', isDark);
      const label = sw.querySelector('.track-label');
      if (label) {
        label.textContent = isDark ? 'DARK' : 'LIGHT';
      }
      sw.setAttribute('aria-checked', isDark ? 'true' : 'false');
      sw.title = `Theme: ${preset.name} (Click to toggle)`;
    });

    // Update dropdown selectors
    document.querySelectorAll('#themeSelect, .theme-select').forEach(sel => {
      sel.value = preset.id;
    });

    // Legacy buttons
    document.querySelectorAll('.theme-toggle-btn, #themeToggleBtn').forEach(btn => {
      btn.innerHTML = `<span class="txt">${preset.name}</span>`;
      btn.classList.toggle('active', isDark);
    });
  }
}

export const theme = new ThemeManager();
if (typeof window !== 'undefined') {
  window.theme = theme;
}
"""

with open(r'C:\Users\hmmm\goalstar-recall\js\theme.js', 'w', encoding='utf-8') as f:
    f.write(theme_js_code)

print("Updated js/theme.js with 4-theme engine!")
