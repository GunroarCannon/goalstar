// GoalStar modular theme engine.
//
// A theme is a small token bundle: the paper palette comes from CSS via
// body[data-paper], and the component language (button shape, shadow, type,
// card corners, motion) comes from html[data-theme-preset] custom properties.
// Adding a theme = adding one preset here + one palette block in style.css.
import { sound } from './sound.js';

export const THEME_PRESETS = {
  'simple-dark': {
    id: 'simple-dark', name: 'Minimal Dark', category: 'simple', paper: 'simple-dark', isDark: true,
    swatches: ['#09090b', '#fafafa', '#00d2ff'],
    blurb: 'Pure 3-color minimalism: pitch black, crisp white, electric cyan.'
  },
  'simple-light': {
    id: 'simple-light', name: 'Minimal Light', category: 'simple', paper: 'simple-light', isDark: false,
    swatches: ['#ffffff', '#09090b', '#2563eb'],
    blurb: 'Pure 3-color minimalism: stark white, deep black, cobalt blue.'
  },
  notebook: {
    id: 'notebook', name: 'Notebook', category: 'craft', paper: 'lined', isDark: false,
    swatches: ['#faf7f0', '#1c1917', '#d97706'],
    blurb: 'Warm ivory paper, ink outlines, squared hand-made buttons.'
  },
  night: {
    id: 'night', name: 'Chalkboard', category: 'craft', paper: 'night', isDark: true,
    swatches: ['#161c24', '#f1f5f9', '#7ecba1'],
    blurb: 'Midnight slate, soft chalk dust, sage and warm chalk tones.'
  },
  blueprint: {
    id: 'blueprint', name: 'Blueprint', category: 'craft', paper: 'blueprint', isDark: true,
    swatches: ['#0b1a2f', '#f0f7ff', '#38bdf8'],
    blurb: 'Technical drafting grid, precision CAD lines, architectural mono.'
  },
  terminal: {
    id: 'terminal', name: 'Terminal', category: 'craft', paper: 'terminal', isDark: true,
    swatches: ['#0b0f14', '#4ade80', '#fbbf24'],
    blurb: 'Obsidian console, crisp phosphor green and amber readouts.'
  },
  monograph: {
    id: 'monograph', name: 'Monograph', category: 'craft', paper: 'monograph', isDark: false,
    swatches: ['#f4eee0', '#292524', '#c2410c'],
    blurb: 'Vintage sepia print, sharp corners, editorial type.'
  },
  sunset: {
    id: 'sunset', name: 'Sunset', category: 'craft', paper: 'sunset', isDark: false,
    swatches: ['#fdf3ec', '#3a2430', '#7c3aed'],
    blurb: 'Warm coral and plum, pill buttons, soft shadows.'
  }
};

export const THEME_ORDER = Object.keys(THEME_PRESETS);

export class ThemeManager {
  constructor() {
    this.currentPreset = localStorage.getItem('goalstar_theme_preset') || 'notebook';
    this._listenerAttached = false;
  }

  init() {
    const saved = localStorage.getItem('goalstar_theme_preset')
      || (localStorage.getItem('goalstar_theme') === 'dark' ? 'night' : 'notebook');
    this.applyTheme(THEME_PRESETS[saved] ? saved : 'notebook');
    this.renderCustomPickers();
    this.attachListeners();
  }

  attachListeners() {
    if (this._listenerAttached || typeof document === 'undefined') return;
    this._listenerAttached = true;

    // Light/dark pill: flips between light and dark palettes
    document.addEventListener('click', (e) => {
      const sw = e.target.closest('#themeSwitch, .theme-switch, .theme-toggle-btn, #themeToggleBtn');
      if (sw) {
        e.preventDefault();
        e.stopPropagation();
        this.toggle();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (!e.target.closest?.('#themeSwitch, .theme-switch')) return;
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); this.toggle(); }
    });

    // Theme dropdown handler for native selects
    document.addEventListener('change', (e) => {
      if (e.target.matches('#themeSelect, .theme-select')) this.setPreset(e.target.value);
    });

    // Dismiss custom theme picker popovers when clicking outside or pressing Escape
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.theme-picker-container')) {
        this.closeAllPickers();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeAllPickers();
      }
    });
  }

  closeAllPickers() {
    if (typeof document === 'undefined') return;
    document.querySelectorAll('.theme-picker-popover.open').forEach(p => p.classList.remove('open'));
    document.querySelectorAll('.theme-picker-btn[aria-expanded="true"]').forEach(b => b.setAttribute('aria-expanded', 'false'));
  }

  toggle() {
    const preset = THEME_PRESETS[this.currentPreset] || THEME_PRESETS.notebook;
    const next = preset.isDark ? 'notebook' : 'night';
    this.setPreset(next);
  }

  setPreset(presetId) {
    if (!THEME_PRESETS[presetId]) presetId = 'notebook';
    this.applyTheme(presetId);
    sound.play('toggle');
  }

  applyTheme(presetId) {
    const preset = THEME_PRESETS[presetId] || THEME_PRESETS.notebook;
    this.currentPreset = preset.id;
    localStorage.setItem('goalstar_theme_preset', preset.id);
    localStorage.setItem('goalstar_theme', preset.isDark ? 'dark' : 'light');

    const root = document.documentElement;
    root.classList.add('theme-switching');
    root.classList.toggle('dark-mode', preset.isDark);
    root.setAttribute('data-theme-preset', preset.id);
    root.setAttribute('data-theme-mode', preset.isDark ? 'dark' : 'light');
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        root.classList.remove('theme-switching');
      });
    });
    if (document.body) {
      document.body.dataset.paper = preset.paper;
    }

    if (typeof window !== 'undefined' && window.data?.settings?.display) {
      window.data.settings.display.paper = preset.paper;
    }

    // Pill switches
    document.querySelectorAll('#themeSwitch, .theme-switch').forEach((sw) => {
      sw.classList.toggle('active', preset.isDark);
      const label = sw.querySelector('.track-label');
      if (label) label.textContent = preset.isDark ? 'DARK' : 'LIGHT';
      sw.setAttribute('aria-checked', preset.isDark ? 'true' : 'false');
      sw.title = `Theme: ${preset.name} — click to switch ${preset.isDark ? 'to light' : 'to dark'}`;
    });

    // Native dropdowns (keeps value in sync)
    document.querySelectorAll('#themeSelect, .theme-select').forEach((sel) => {
      if (sel.value !== preset.id) sel.value = preset.id;
    });

    // Update bespoke custom pickers
    this.updateCustomPickers(preset);

    // Legacy label buttons
    document.querySelectorAll('.theme-toggle-btn, #themeToggleBtn').forEach((btn) => {
      btn.innerHTML = `<span class="txt">${preset.name}</span>`;
      btn.classList.toggle('active', preset.isDark);
    });

    document.dispatchEvent(new CustomEvent('goalstar:theme', { detail: preset }));
  }

  renderCustomPickers() {
    if (typeof document === 'undefined') return;

    document.querySelectorAll('#themeSelect, .theme-select').forEach((sel) => {
      // Ensure all options exist in underlying native select for forms and accessibility
      Object.values(THEME_PRESETS).forEach((p) => {
        if (!sel.querySelector(`option[value="${p.id}"]`)) {
          const opt = document.createElement('option');
          opt.value = p.id;
          opt.textContent = p.name;
          sel.appendChild(opt);
        }
      });

      // Avoid double-wrapping
      let wrap = sel.closest('.theme-picker-container');
      if (!wrap) {
        wrap = document.createElement('div');
        wrap.className = 'theme-picker-container';
        sel.parentNode.insertBefore(wrap, sel);
        wrap.appendChild(sel);
        sel.style.display = 'none';

        const currentPreset = THEME_PRESETS[this.currentPreset] || THEME_PRESETS.notebook;

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'theme-picker-btn engraved-btn';
        btn.setAttribute('aria-haspopup', 'listbox');
        btn.setAttribute('aria-expanded', 'false');
        btn.title = 'Choose a visual theme';
        btn.innerHTML = `
          <span class="tp-swatches">${currentPreset.swatches.map(c => `<span class="tp-dot" style="background:${c}"></span>`).join('')}</span>
          <span class="tp-name">${currentPreset.name}</span>
          <svg class="tp-chevron" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
        `;

        const popover = document.createElement('div');
        popover.className = 'theme-picker-popover';
        popover.setAttribute('role', 'listbox');

        // Simple themes section
        const simpleHeader = document.createElement('div');
        simpleHeader.className = 'tp-section-header';
        simpleHeader.textContent = 'Minimal 3-Color';
        popover.appendChild(simpleHeader);

        Object.values(THEME_PRESETS).filter(p => p.category === 'simple').forEach(p => {
          popover.appendChild(this._createOptionEl(p));
        });

        // Thematic Craft section
        const craftHeader = document.createElement('div');
        craftHeader.className = 'tp-section-header';
        craftHeader.textContent = 'Thematic Craft';
        popover.appendChild(craftHeader);

        Object.values(THEME_PRESETS).filter(p => p.category !== 'simple').forEach(p => {
          popover.appendChild(this._createOptionEl(p));
        });

        wrap.appendChild(btn);
        wrap.appendChild(popover);

        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const isOpen = popover.classList.contains('open');
          this.closeAllPickers();
          if (!isOpen) {
            popover.classList.add('open');
            btn.setAttribute('aria-expanded', 'true');
          }
        });
      }
    });

    this.updateCustomPickers(THEME_PRESETS[this.currentPreset] || THEME_PRESETS.notebook);
  }

  _createOptionEl(p) {
    const optEl = document.createElement('button');
    optEl.type = 'button';
    optEl.className = 'tp-option';
    optEl.setAttribute('role', 'option');
    optEl.dataset.themeId = p.id;
    optEl.innerHTML = `
      <div class="tp-opt-left">
        <span class="tp-swatches">${p.swatches.map(c => `<span class="tp-dot" style="background:${c}"></span>`).join('')}</span>
        <span class="tp-opt-title">${p.name}</span>
      </div>
      <span class="tp-opt-badge ${p.isDark ? 'dark' : 'light'}">${p.category === 'simple' ? '3-COL' : (p.isDark ? 'DARK' : 'LIGHT')}</span>
    `;

    optEl.addEventListener('click', (e) => {
      e.stopPropagation();
      this.setPreset(p.id);
      this.closeAllPickers();
    });

    return optEl;
  }

  updateCustomPickers(preset) {
    if (typeof document === 'undefined') return;
    document.querySelectorAll('.theme-picker-container').forEach(wrap => {
      const btn = wrap.querySelector('.theme-picker-btn');
      if (btn) {
        const nameEl = btn.querySelector('.tp-name');
        if (nameEl) nameEl.textContent = preset.name;
        const swatchesEl = btn.querySelector('.tp-swatches');
        if (swatchesEl) {
          swatchesEl.innerHTML = preset.swatches.map(c => `<span class="tp-dot" style="background:${c}"></span>`).join('');
        }
      }
      wrap.querySelectorAll('.tp-option').forEach(opt => {
        const isActive = opt.dataset.themeId === preset.id;
        opt.classList.toggle('active', isActive);
        opt.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });
    });
  }
}

export const theme = new ThemeManager();
if (typeof window !== 'undefined') {
  window.theme = theme;
}
