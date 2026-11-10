// Paper-note tooltips + a themed confirm sheet.
//
// Any element with `title` or `data-tip` gets a hand-drawn note instead of the
// browser's grey tooltip. The original title is removed while the note is open
// so the two never appear together, then restored on hide.
//
// `askConfirm()` replaces window.confirm with a card that matches the app.

let tipEl = null;
let tipTarget = null;
let activeAnchor = null;
let showTimer = null;
let hideTimer = null;
let loopRaf = 0;
let isScrolling = false;
let scrollEndTimer = null;
let lastScrollTime = 0;
let lastPointerX = -1;
let lastPointerY = -1;
let tipAnim = null;

const TIP_IN_MS = 240;
const TIP_OUT_MS = 140;

// In-quad swing: enters from 13deg left at 0.7 scale, smoothly accelerating into place.
const TIP_IN_FRAMES = [
  { opacity: 0, transform: 'rotate(-13deg) scale(0.7)' },
  { opacity: 1, transform: 'rotate(0deg) scale(1)' },
];

// Clean, snappy exit: smooth fade and subtle scale down without stuttery multi-bounce
const TIP_OUT_FRAMES = [
  { opacity: 1, transform: 'rotate(0deg) scale(1)' },
  { opacity: 0, transform: 'rotate(-4deg) scale(0.9)' },
];

const TIP_IN_REDUCED = [
  { opacity: 0, transform: 'scale(0.92)' },
  { opacity: 1, transform: 'scale(1)' },
];
const TIP_OUT_REDUCED = [
  { opacity: 1, transform: 'scale(1)' },
  { opacity: 0, transform: 'scale(0.9)' },
];

const prefersReducedMotion = () =>
  typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

function playTip(frames, duration, easing, reducedFrames) {
  if (!tipEl) return;
  if (tipAnim) {
    tipAnim.cancel();
    tipAnim = null;
  }
  if (typeof tipEl.animate !== 'function') return; // .show / .out still hold the end state
  const reduced = prefersReducedMotion();
  tipAnim = tipEl.animate(reduced ? reducedFrames : frames, {
    duration: reduced ? 150 : duration,
    easing: reduced ? 'linear' : easing,
    fill: 'both',
  });
}

function ensureTip() {
  if (tipEl) return tipEl;
  tipEl = document.createElement('div');
  tipEl.className = 'gs-tip';
  tipEl.setAttribute('role', 'tooltip');
  document.body.appendChild(tipEl);
  return tipEl;
}

function place(el) {
  if (!el || !el.isConnected) return;
  const tip = ensureTip();
  const r = el.getBoundingClientRect();
  const tw = tip.offsetWidth || 140;
  const th = tip.offsetHeight || 36;
  const margin = 10;

  let above = r.top > th + margin * 2;
  let top = above ? r.top - th - margin : r.bottom + margin;
  let left = r.left + r.width / 2 - tw / 2;

  left = Math.max(8, Math.min(window.innerWidth - tw - 8, left));
  top = Math.max(8, Math.min(window.innerHeight - th - 8, top));

  tip.classList.toggle('below', !above);
  tip.classList.toggle('above', above);
  tip.style.transformOrigin = above ? '50% 100%' : '50% 0%';

  // Point the speech-bubble tail at the middle of the element, even after the
  // note has been nudged back inside the viewport. Kept inside the note's
  // rounded corners so the tail never floats off the edge.
  const anchorX = r.left + r.width / 2;
  const tail = Math.round(Math.max(14, Math.min(tw - 14, anchorX - left)));
  tip.style.setProperty('--arrow-x', `${tail}px`);

  const nextLeft = `${Math.round(left)}px`;
  const nextTop = `${Math.round(top)}px`;
  if (tip.style.left !== nextLeft) tip.style.left = nextLeft;
  if (tip.style.top !== nextTop) tip.style.top = nextTop;
}

function anchorOnScreen(el) {
  if (!el || !el.isConnected) return false;
  const r = el.getBoundingClientRect();
  return r.bottom > -20 && r.top < window.innerHeight + 20 && r.right > -20 && r.left < window.innerWidth + 20;
}

// Continuous frame-by-frame loop that keeps tooltip glued to the element
function startLoop() {
  if (loopRaf) return;
  const tick = () => {
    const target = tipTarget || activeAnchor;
    if (!target || !tipEl || (!tipEl.classList.contains('show') && !tipEl.classList.contains('out'))) {
      loopRaf = 0;
      return;
    }

    const leaving = tipEl.classList.contains('out');

    // Stay glued to the element for the whole life of the note, including the
    // out-bounce, so the note never detaches and jumps while it fades away.
    if (target.isConnected && (leaving || anchorOnScreen(target))) place(target);

    if (!target.isConnected || (!leaving && !anchorOnScreen(target))) {
      if (!leaving) hide();
      loopRaf = 0;
      return;
    }

    loopRaf = requestAnimationFrame(tick);
  };
  loopRaf = requestAnimationFrame(tick);
}

function stopLoop() {
  if (loopRaf) {
    cancelAnimationFrame(loopRaf);
    loopRaf = 0;
  }
}

function show(el) {
  // The walkthrough has its own annotations; don't stack tooltips on top of it.
  if (document.querySelector('.sketch-tour-overlay')) return;
  const text = el.getAttribute('data-tip') || el.getAttribute('title');
  if (!text || !text.trim()) return;

  if (el.hasAttribute('title')) {
    el.dataset.tipSaved = el.getAttribute('title');
    el.removeAttribute('title');
  }

  tipTarget = el;
  activeAnchor = el;
  const tip = ensureTip();
  clearTimeout(hideTimer);

  tip.classList.remove('show', 'out');
  tip.textContent = text;

  // Position at current element position before showing
  place(el);
  void tip.offsetWidth;
  tip.classList.add('show');
  playTip(TIP_IN_FRAMES, TIP_IN_MS, 'cubic-bezier(0.55, 0.085, 0.68, 0.53)', TIP_IN_REDUCED);

  startLoop();
}

function hide() {
  clearTimeout(showTimer);
  if (tipTarget?.dataset?.tipSaved != null) {
    tipTarget.setAttribute('title', tipTarget.dataset.tipSaved);
    delete tipTarget.dataset.tipSaved;
  }
  tipTarget = null;

  if (!tipEl) return;
  // If already playing out animation, don't interrupt and restart it
  if (tipEl.classList.contains('out')) return;
  if (!tipEl.classList.contains('show')) {
    activeAnchor = null;
    stopLoop();
    return;
  }

  tipEl.classList.remove('show');
  void tipEl.offsetWidth;
  tipEl.classList.add('out');
  playTip(TIP_OUT_FRAMES, TIP_OUT_MS, 'cubic-bezier(0.4, 0, 1, 1)', TIP_OUT_REDUCED);

  // Stop the placement loop immediately on hide so it doesn't thrash layout during fade-out
  stopLoop();

  clearTimeout(hideTimer);
  hideTimer = setTimeout(() => {
    if (tipEl?.classList.contains('out')) {
      tipEl.classList.remove('out');
    }
    if (tipAnim) {
      tipAnim.cancel();
      tipAnim = null;
    }
    activeAnchor = null;
    stopLoop();
  }, TIP_OUT_MS + 20);
}

export function initTooltips() {
  if (typeof document === 'undefined') return;

  const markScrollOrWheel = () => {
    lastScrollTime = performance.now();
    isScrolling = true;
    clearTimeout(scrollEndTimer);
    scrollEndTimer = setTimeout(() => {
      isScrolling = false;
    }, 280);
    startLoop();
  };

  // Listen across the window for scrolls, wheel interactions, and touch scrolls
  window.addEventListener('scroll', markScrollOrWheel, { passive: true, capture: true });
  window.addEventListener('wheel', markScrollOrWheel, { passive: true, capture: true });
  window.addEventListener('touchmove', markScrollOrWheel, { passive: true, capture: true });
  window.addEventListener('resize', () => {
    const target = tipTarget || activeAnchor;
    if (target) place(target);
  });

  document.addEventListener('pointerover', (e) => {
    if (e.pointerType === 'touch') return;
    const el = e.target.closest?.('[data-tip], [title]');
    if (!el || el.closest('.gs-tip')) return;
    if (el === tipTarget && tipEl?.classList.contains('show')) return;
    clearTimeout(showTimer);
    showTimer = setTimeout(() => show(el), 120);
  });

  document.addEventListener('pointerout', (e) => {
    // If the user is actively scrolling/wheeling, the element moves under a stationary mouse.
    // Do NOT dismiss the tooltip! It should stay attached and scroll with its element!
    if (isScrolling || (performance.now() - lastScrollTime < 320)) return;

    if (tipTarget) {
      if (e.target !== tipTarget && !tipTarget.contains(e.target)) return;
      if (e.relatedTarget && (tipTarget.contains(e.relatedTarget) || e.relatedTarget.closest?.('.gs-tip'))) return;
      hide();
      return;
    }
    clearTimeout(showTimer);
  });

  document.addEventListener('pointermove', (e) => {
    lastPointerX = e.clientX;
    lastPointerY = e.clientY;

    // While user is scrolling or immediately after, don't dismiss on cursor displacement
    if (isScrolling || (performance.now() - lastScrollTime < 320) || !tipTarget) return;

    const r = tipTarget.getBoundingClientRect();
    const pad = 12;
    const isOverTarget = (
      e.clientX >= r.left - pad &&
      e.clientX <= r.right + pad &&
      e.clientY >= r.top - pad &&
      e.clientY <= r.bottom + pad
    );
    if (!isOverTarget) {
      hide();
    }
  });

  document.addEventListener('focusin', (e) => {
    const el = e.target.closest?.('[data-tip], [title]');
    if (!el) return;
    clearTimeout(showTimer);
    showTimer = setTimeout(() => show(el), 120);
  });

  document.addEventListener('focusout', (e) => {
    if (e.target === tipTarget) hide();
  });

  document.addEventListener('pointerdown', (e) => {
    if (!e.target.closest?.('.gs-tip')) hide();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') hide();
  });
}

// ---------------------------------------------------------------------------
// Themed confirm sheet (replaces window.confirm)
// ---------------------------------------------------------------------------
export function askConfirm({
  title = 'Are you sure?',
  message = '',
  confirmText = 'Yes',
  cancelText = 'Cancel',
  danger = false,
} = {}) {
  return new Promise((resolve) => {
    const overlay = document.createElement('div');
    overlay.className = 'gs-confirm-overlay';
    overlay.innerHTML = `
      <div class="gs-confirm-card" role="dialog" aria-modal="true" aria-label="${title.replace(/"/g, '&quot;')}">
        <div class="gs-confirm-tape" aria-hidden="true"></div>
        <h3 class="gs-confirm-title">${title}</h3>
        ${message ? `<p class="gs-confirm-msg">${message}</p>` : ''}
        <div class="gs-confirm-actions">
          <button type="button" class="gs-confirm-btn" data-confirm="no">${cancelText}</button>
          <button type="button" class="gs-confirm-btn primary${danger ? ' danger' : ''}" data-confirm="yes">${confirmText}</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    const yes = overlay.querySelector('[data-confirm="yes"]');
    const no = overlay.querySelector('[data-confirm="no"]');

    const close = (value) => {
      document.removeEventListener('keydown', onKey);
      overlay.remove();
      resolve(value);
    };
    const onKey = (e) => {
      if (e.key === 'Escape') { e.preventDefault(); close(false); }
      if (e.key === 'Enter' && document.activeElement === yes) { e.preventDefault(); close(true); }
    };

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) close(false);
      if (e.target.closest('[data-confirm="yes"]')) close(true);
      if (e.target.closest('[data-confirm="no"]')) close(false);
    });
    document.addEventListener('keydown', onKey);
    setTimeout(() => (danger ? no : yes).focus(), 30);
  });
}
