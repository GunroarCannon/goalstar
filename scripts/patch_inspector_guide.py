import os

# 1. Patch css/style.css
css_path = r"C:\Users\hmmm\goalstar-recall\css\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css_text = f.read().replace("\r\n", "\n")

target_css = """.inspector textarea[data-f='label'] { font-family: var(--hand); font-size: 19px; line-height: 1.2; }"""

repl_css = """.inspector textarea[data-f='label'] {
  font-family: 'Space Grotesk', system-ui, -apple-system, sans-serif;
  font-size: 16.5px;
  font-weight: 700;
  line-height: 1.35;
  color: var(--ink);
  border-radius: 8px;
  border: 1.5px solid var(--border);
  padding: 8px 10px;
}
.inspector textarea[data-f='label']:focus {
  border-color: var(--accent);
  outline: none;
  box-shadow: 0 0 0 2px rgba(5, 150, 105, 0.15);
}
.inspector textarea[data-f='note'] {
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 14px;
  line-height: 1.45;
  color: var(--ink);
  border-radius: 8px;
  border: 1.5px solid var(--border);
  padding: 8px 10px;
}
.inspector textarea[data-f='note']:focus {
  border-color: var(--accent);
  outline: none;
  box-shadow: 0 0 0 2px rgba(5, 150, 105, 0.15);
}
.inspector .ins-guide-btn:hover {
  background: var(--accent) !important;
  color: #fff !important;
}"""

assert target_css in css_text, "target_css not found"
css_text = css_text.replace(target_css, repl_css)
with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_text)
print("Updated css/style.css")

# 2. Patch js/app.js
app_path = r"C:\Users\hmmm\goalstar-recall\js\app.js"
with open(app_path, "r", encoding="utf-8") as f:
    app_text = f.read().replace("\r\n", "\n")

# Add guide button to inspector header
target_ins_head = """<div class="ins-head"><span class="kind k-${n.kind}">${n.kind === 'goal' ? 'Goal' : n.kind === 'start' ? ' Where you are' : 'State'}</span><button class="icon close" data-act="close" title="Close (Esc)">×</button></div>"""

repl_ins_head = """<div class="ins-head">
        <span class="kind k-${n.kind}">${n.kind === 'goal' ? 'Goal' : n.kind === 'start' ? ' Where you are' : 'State'}</span>
        <div style="display:flex; align-items:center; gap:8px;">
          <button class="ins-guide-btn" data-act="ins-guide" title="Show guide for this inspector" style="font-family:'Space Grotesk',sans-serif; font-size:12px; font-weight:700; padding:2px 8px; border-radius:6px; border:1px solid var(--accent); background:var(--panel-2); color:var(--accent); cursor:pointer;"><span style="color:var(--accent); font-weight:800;">?</span> Guide</button>
          <button class="icon close" data-act="close" title="Close (Esc)">×</button>
        </div>
      </div>"""

assert target_ins_head in app_text, "target_ins_head not found"
app_text = app_text.replace(target_ins_head, repl_ins_head)

# Add event listener for ins-guide in inspector click handler
target_click = """    if (act === 'center') canvas.centerOn(id);"""
repl_click = """    if (act === 'center') canvas.centerOn(id);
    if (act === 'ins-guide') {
      sound.play('pop');
      if (window.tour && typeof window.tour.goToStep === 'function') {
        window.tour.goToStep(5);
      } else if (window.tour && typeof window.tour.start === 'function') {
        window.tour.start(true);
      }
    }"""

assert target_click in app_text, "target_click not found"
app_text = app_text.replace(target_click, repl_click)

# Update uiGuideBtn click behavior
target_ui_guide = """  document.getElementById('uiGuideBtn')?.addEventListener('click', () => {
    sound.play('pop');
    if (guideDlg && typeof guideDlg.showModal === 'function') guideDlg.showModal();
    else if (guideDlg) guideDlg.setAttribute('open', 'true');
  });"""

repl_ui_guide = """  document.getElementById('uiGuideBtn')?.addEventListener('click', () => {
    stopTourBounce();
    sound.play('pop');
    if (!sel) {
      window.selectFirstStateNode?.();
    }
    if (window.tour && typeof window.tour.start === 'function') {
      if (sel && sel.type === 'node') {
        window.tour.goToStep?.(5);
      } else {
        window.tour.start(true);
      }
    } else if (guideDlg && typeof guideDlg.showModal === 'function') {
      guideDlg.showModal();
    }
  });"""

assert target_ui_guide in app_text, "target_ui_guide not found"
app_text = app_text.replace(target_ui_guide, repl_ui_guide)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_text)
print("Updated js/app.js")

# 3. Patch js/tour.js to add goToStep and improve Step 6
tour_path = r"C:\Users\hmmm\goalstar-recall\js\tour.js"
with open(tour_path, "r", encoding="utf-8") as f:
    tour_text = f.read().replace("\r\n", "\n")

target_tour_start = """  start(force = false) {
    if (!force && localStorage.getItem(this.storageKey)) return;
    window.stopTourBounce?.();
    sound.play('pop');
    this.currentStep = 0;
    this.render();
  }"""

repl_tour_start = """  start(force = false) {
    if (!force && localStorage.getItem(this.storageKey)) return;
    window.stopTourBounce?.();
    sound.play('pop');
    this.currentStep = 0;
    this.render();
  }

  goToStep(stepIndex) {
    window.stopTourBounce?.();
    sound.play('pop');
    this.currentStep = Math.max(0, Math.min(this.steps.length - 1, stepIndex));
    this.render();
  }"""

assert target_tour_start in tour_text, "target_tour_start not found"
tour_text = tour_text.replace(target_tour_start, repl_tour_start)

# In step 6 of tour:
target_sui_onenter = """        id: 'sui-inspector',
        title: 'Step 6: Inspector & Verifiable Proof',
        text: 'Take notes, check off steps, or click "Verify Milestone on Sui" for immutable blockchain proof via Tatum RPC.',
        onEnter: () => {
          if (window.selectFirstStateNode) {
            window.selectFirstStateNode();
          }
        },
        targetSelector: () => document.querySelector('[data-act="sui-stamp"]') || document.querySelector('#inspector:not([hidden])') || document.querySelector('.inspector')"""

repl_sui_onenter = """        id: 'sui-inspector',
        title: 'Step 6: Inspector & Verifiable Proof',
        text: 'The State Inspector lets you edit labels, track notes, and click "Verify Milestone on Sui" for cryptographic proof via Tatum RPC.',
        onEnter: () => {
          if (window.selectFirstStateNode) {
            window.selectFirstStateNode();
          }
          const ins = document.getElementById('inspector');
          if (ins) {
            ins.hidden = false;
            ins.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' });
          }
        },
        targetSelector: () => document.querySelector('[data-act="sui-stamp"]') || document.querySelector('.ins-head') || document.querySelector('#inspector:not([hidden])') || document.querySelector('.inspector')"""

assert target_sui_onenter in tour_text, "target_sui_onenter not found"
tour_text = tour_text.replace(target_sui_onenter, repl_sui_onenter)

with open(tour_path, "w", encoding="utf-8") as f:
    f.write(tour_text)
print("Updated js/tour.js")
