// GoalStar Audio Engine (Loaded from Platformer sound effects)
// Snappy, tactile, organic sounds with zero latency

const SOUND_FILES = {
  click: 'assets/sounds/ui/switch_on.ogg',
  pop: 'assets/sounds/ui/drop_001.ogg',
  paper: 'assets/sounds/ui/drop_002.ogg',
  scribble: 'assets/sounds/ui/drop_002.ogg',
  stamp: 'assets/sounds/gem-gather-stereo-reverb.wav',
  chime: 'assets/sounds/gem-gather-stereo-reverb.wav',
  toggle: 'assets/sounds/ui/switch_on.ogg',
  toggle_off: 'assets/sounds/ui/switch_off.ogg',
  crunch: 'assets/sounds/tick_004.ogg',
  whoosh: 'assets/sounds/ui/drop_002.ogg',
  ding: 'assets/sounds/ui/confirmation_001.ogg'
};

class SoundEngine {
  constructor() {
    this.ctx = null;
    this.enabled = typeof localStorage !== 'undefined' ? localStorage.getItem('goalstar_sound_enabled') !== 'false' : true;
    this.audioPool = new Map();
    this.preload();
  }

  preload() {
    if (typeof window === 'undefined') return;
    for (const [key, src] of Object.entries(SOUND_FILES)) {
      if (!this.audioPool.has(src)) {
        try {
          const a = new Audio();
          a.src = src;
          a.preload = 'auto';
          this.audioPool.set(src, a);
        } catch (e) {}
      }
    }
  }

  init() {
    if (!this.ctx && (typeof window !== 'undefined')) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume().catch(() => {});
    }
    this.preload();
  }

  toggle() {
    this.enabled = !this.enabled;
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('goalstar_sound_enabled', this.enabled ? 'true' : 'false');
    }
    if (this.enabled) {
      this.init();
      this.play('toggle');
    } else {
      this.play('toggle_off');
    }
    this.updateUI();
    const sw = document.getElementById('soundSwitch');
    if (sw) {
      sw.classList.toggle('active', this.enabled);
    }
    return this.enabled;
  }

  updateUI() {
    if (typeof document === 'undefined') return;
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
      btn.innerHTML = this.enabled ? '<span class="txt">Sound</span>' : '<span class="txt">Muted</span>';
      btn.title = this.enabled ? 'Mute sound effects' : 'Enable snappy sound effects';
      btn.classList.toggle('muted', !this.enabled);
    });
  }

  play(type) {
    if (!this.enabled) return;
    this.init();

    const src = SOUND_FILES[type] || SOUND_FILES.click;
    try {
      const audio = new Audio(src);
      audio.volume = (type === 'stamp' || type === 'chime') ? 0.5 : (type === 'crunch' ? 0.35 : 0.45);
      const p = audio.play();
      if (p && typeof p.catch === 'function') {
        p.catch(() => {});
      }
    } catch (e) {
      console.warn('Sound play error:', e);
    }
  }

  attachListeners() {
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
      if ((e.key === ' ' || e.key === 'Enter') && e.target.closest?.('#soundSwitch, .sound-switch')) {
        e.preventDefault();
        this.toggle();
      }
    });

    // Soft tactile feedback only when releasing a slider, never during continuous drag
    document.addEventListener('change', (e) => {
      if (e.target.matches('input[type="range"]')) {
        this.play('click');
      }
    });

    this.updateUI();
  }
}

export const sound = new SoundEngine();
if (typeof window !== 'undefined') {
  window.sound = sound;
}
