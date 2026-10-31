const fs = require('fs');
const path = require('path');

const ROOT = 'C:/Users/hmmm/goalstar-recall';
const tourPath = path.join(ROOT, 'js/tour.js');
let content = fs.readFileSync(tourPath, 'utf8');

// Build replacement for renderDom in SketchTour
const newRenderDom = `  renderDom(step) {
    if (!this.overlay) {
      this.overlay = document.createElement('div');
      this.overlay.className = 'sketch-tour-overlay';
      document.body.appendChild(this.overlay);
    }

    const cardW = 380;
    const cardH = 305; // Conservative measured upper bound for card height

    let targetEl = null;
    if (typeof step.targetSelector === 'function') {
      try { targetEl = step.targetSelector(); } catch(e) {}
    } else if (step.targetSelector) {
      targetEl = document.querySelector(step.targetSelector);
    }

    // Topbar, sidebar, or inspector context detection
    const isTopBar = targetEl && (targetEl.closest('header') || targetEl.closest('nav') || targetEl.id === 'dreamBtn' || targetEl.id === 'newGoalBtn' || targetEl.id === 'searchBtn');
    const isSidebar = (targetEl && targetEl.closest('.side')) || step.id === 'best-path' || step.id === 'walrus-memory';
    const isInspector = (targetEl && targetEl.closest('#inspector')) || step.id === 'action-checklist' || step.id === 'inspector-notes' || step.id === 'sui-inspector';

    const isValidRect = (r) => r && (r.width > 4 || r.height > 4) && (r.bottom > 8) && (r.right > 16);
    let tr = targetEl ? targetEl.getBoundingClientRect() : null;

    if (!tr || !isValidRect(tr)) {
      if (step.onEnter) { try { step.onEnter(); } catch(e) {} }
      tr = targetEl ? targetEl.getBoundingClientRect() : null;
    }

    let targetRect = (tr && isValidRect(tr)) ? tr : {
      left: Math.max(340, window.innerWidth / 2 - 100),
      top: 240,
      width: 200,
      height: 70,
      right: Math.max(540, window.innerWidth / 2 + 100),
      bottom: 310
    };

    const spotPad = isTopBar ? 5 : 8;
    const minSpotY = isTopBar ? 4 : 70;
    const spotX = Math.max(12, Math.min(window.innerWidth - 60, targetRect.left - spotPad));
    const spotY = Math.max(minSpotY, Math.min(window.innerHeight - 50, targetRect.top - spotPad));
    const spotW = Math.max(34, Math.min(window.innerWidth - spotX - 12, targetRect.width + spotPad * 2));
    const spotH = Math.max(26, Math.min(window.innerHeight - spotY - 12, targetRect.height + spotPad * 2));
    const spotRight = spotX + spotW;
    const spotBottom = spotY + spotH;

    // Viewport bounds for card (Guaranteed zero clipping)
    const minCardLeft = 16;
    const maxCardLeft = Math.max(16, window.innerWidth - cardW - 16);
    const minCardTop = 60;
    const maxCardTop = Math.max(60, window.innerHeight - cardH - 25);

    const spaceBelow = window.innerHeight - spotBottom;
    const spaceAbove = spotY - minCardTop;
    const spaceLeft = spotX - minCardLeft;
    const spaceRight = window.innerWidth - spotRight;

    let cardPos = { left: 40, top: 120 };
    let arrow = null;

    if (isTopBar) {
      // Topbar element (like #dreamBtn): place card below with arrow pointing UP
      cardPos.left = Math.max(minCardLeft, Math.min(maxCardLeft, spotX + (spotW - cardW) / 2));
      cardPos.top = Math.max(minCardTop, Math.min(maxCardTop, spotBottom + 16));
      arrow = {
        from: { x: cardPos.left + cardW / 2, y: cardPos.top },
        to: { x: spotX + spotW / 2, y: spotBottom + 4 },
        ctrl: { x: (cardPos.left + cardW / 2 + spotX + spotW / 2) / 2, y: (cardPos.top + spotBottom) / 2 },
        color: '#059669'
      };
    } else if (isSidebar) {
      // Left sidebar: place to right of sidebar with direct arrow pointing left
      cardPos.left = Math.min(maxCardLeft, spotRight + 20);
      cardPos.top = Math.max(minCardTop, Math.min(maxCardTop, spotY + 5));
      arrow = {
        from: { x: cardPos.left, y: cardPos.top + 45 },
        to: { x: spotRight + 4, y: spotY + Math.min(30, spotH / 2) },
        ctrl: { x: (cardPos.left + spotRight) / 2 - 10, y: cardPos.top + 40 },
        color: '#059669'
      };
    } else if (isInspector) {
      // Right inspector panel: place to left on desktop, or above on mobile
      if (window.innerWidth > 900) {
        cardPos.left = Math.max(minCardLeft, spotX - cardW - 20);
        cardPos.top = Math.max(minCardTop, Math.min(maxCardTop, spotY - 40));
        arrow = {
          from: { x: cardPos.left + cardW, y: cardPos.top + 45 },
          to: { x: spotX - 4, y: spotY + Math.min(25, spotH / 2) },
          ctrl: { x: (cardPos.left + cardW + spotX) / 2 + 10, y: cardPos.top + 40 },
          color: '#059669'
        };
      } else {
        cardPos.left = Math.max(minCardLeft, Math.min(maxCardLeft, (window.innerWidth - cardW) / 2));
        cardPos.top = Math.max(minCardTop, spotY - cardH - 16);
        arrow = {
          from: { x: cardPos.left + cardW / 2, y: cardPos.top + cardH },
          to: { x: spotX + spotW / 2, y: spotY - 3 },
          ctrl: { x: cardPos.left + cardW / 2, y: (cardPos.top + cardH + spotY) / 2 },
          color: '#059669'
        };
      }
    } else {
      // Canvas targets: choose direction with plenty of breathing room
      if (spaceBelow >= cardH + 35) {
        cardPos.left = Math.max(minCardLeft, Math.min(maxCardLeft, spotX + (spotW - cardW) / 2));
        cardPos.top = Math.min(maxCardTop, spotBottom + 16);
        arrow = {
          from: { x: cardPos.left + cardW / 2, y: cardPos.top },
          to: { x: spotX + spotW / 2, y: spotBottom + 3 },
          ctrl: { x: (cardPos.left + cardW / 2 + spotX + spotW / 2) / 2, y: (cardPos.top + spotBottom) / 2 },
          color: '#059669'
        };
      } else if (spaceAbove >= cardH + 35) {
        cardPos.left = Math.max(minCardLeft, Math.min(maxCardLeft, spotX + (spotW - cardW) / 2));
        cardPos.top = Math.max(minCardTop, spotY - cardH - 16);
        arrow = {
          from: { x: cardPos.left + cardW / 2, y: cardPos.top + cardH },
          to: { x: spotX + spotW / 2, y: spotY - 3 },
          ctrl: { x: (cardPos.left + cardW / 2 + spotX + spotW / 2) / 2, y: (cardPos.top + cardH + spotY) / 2 },
          color: '#059669'
        };
      } else if (spaceLeft >= cardW + 30) {
        cardPos.left = Math.max(minCardLeft, spotX - cardW - 20);
        cardPos.top = Math.max(minCardTop, Math.min(maxCardTop, spotY - 20));
        arrow = {
          from: { x: cardPos.left + cardW, y: cardPos.top + 45 },
          to: { x: spotX - 3, y: spotY + Math.min(30, spotH / 2) },
          ctrl: { x: (cardPos.left + cardW + spotX) / 2 + 10, y: cardPos.top + 40 },
          color: '#059669'
        };
      } else {
        cardPos.left = Math.min(maxCardLeft, spotRight + 20);
        cardPos.top = Math.max(minCardTop, Math.min(maxCardTop, spotY - 20));
        arrow = {
          from: { x: cardPos.left, y: cardPos.top + 45 },
          to: { x: spotRight + 3, y: spotY + Math.min(30, spotH / 2) },
          ctrl: { x: (cardPos.left + spotRight) / 2 - 10, y: cardPos.top + 40 },
          color: '#059669'
        };
      }
    }`;

// Find start and end of renderDom setup
const startMarker = '  renderDom(step) {';
const startIdx = content.indexOf(startMarker);
const endMarker = '    cardPos.left = Math.max(minCardLeft, Math.min(maxCardLeft, cardPos.left));';
const endIdx = content.indexOf(endMarker);

if (startIdx !== -1 && endIdx !== -1) {
  content = content.slice(0, startIdx) + newRenderDom + '\n\n' + content.slice(endIdx);
  fs.writeFileSync(tourPath, content, 'utf8');
  console.log('Successfully patched renderDom in tour.js');
} else {
  console.error('Could not find renderDom boundary markers in tour.js', { startIdx, endIdx });
}
