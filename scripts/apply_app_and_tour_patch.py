import os
import re

print("Patching style.css, app.js, and tour.js...")

# -------------------------------------------------------------
# 1. Update css/style.css
# -------------------------------------------------------------
css_path = r"C:\Users\hmmm\goalstar-recall\css\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Add transition to .near i if not present
if "transition: width" not in css:
    css = css.replace(
        "  background-image: repeating-linear-gradient(\n    -45deg,\n    var(--accent),\n    var(--accent) 3px,\n    #1d4ed8 3px,\n    #1d4ed8 6px\n  );\n}",
        "  background-image: repeating-linear-gradient(\n    -45deg,\n    var(--accent),\n    var(--accent) 3px,\n    #1d4ed8 3px,\n    #1d4ed8 6px\n  );\n  transition: width 0.35s cubic-bezier(0.2, 0.8, 0.2, 1);\n}"
    )

extra_css = """
/* Card Step Badge on Milestones */
.card-step-badge {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-size: 11px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 4px;
  background: rgba(42, 45, 62, 0.08);
  color: var(--ink);
  border: 1px solid rgba(42, 45, 62, 0.2);
  display: inline-flex;
  align-items: center;
  margin-right: 4px;
}
body[data-paper='night'] .card-step-badge {
  background: rgba(245, 158, 11, 0.15);
  color: #f1f5f9;
  border-color: rgba(245, 158, 11, 0.35);
}

/* Clear Linking Banner */
.link-banner {
  position: fixed;
  top: 72px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  background: #1e293b;
  color: #f8fafc;
  padding: 10px 20px;
  border-radius: 24px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13.5px;
  font-weight: 600;
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  gap: 14px;
}
.link-banner button {
  background: rgba(255,255,255,0.2);
  border: 1px solid rgba(255,255,255,0.3);
  color: #fff;
  padding: 3px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}
.link-banner button:hover {
  background: rgba(255,255,255,0.35);
}

/* Sui Proof Box */
.sui-box {
  margin-top: 14px;
  padding: 12px 14px;
  border-radius: 10px;
  background: var(--panel-card, rgba(0,0,0,0.03));
  border: 1.5px solid var(--card-border, rgba(42, 45, 62, 0.15));
}
"""

if ".card-step-badge" not in css:
    css += extra_css

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
print("Updated css/style.css")

# -------------------------------------------------------------
# 2. Update js/app.js
# -------------------------------------------------------------
app_path = r"C:\Users\hmmm\goalstar-recall\js\app.js"
with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

# Update renderProgress to reflect checklist steps
old_rp = """function renderProgress(b, r, w) {
  const goalDone = b.nodes[b.goalId].done;
  const full = astar(b, w, { fromStart: true });
  let pct = goalDone ? 100 : r.found && full.found && full.cost > 0 ? Math.round(Math.max(0, Math.min(1, 1 - r.cost / full.cost)) * 100) : 0;
  if (!r.found && !goalDone) pct = 0;
  $('#progress').innerHTML = `
    <div class="pbar"><i style="width:${pct}%"></i></div>
    <div class="pmeta"><b>${pct}%</b> of the way${r.found && !goalDone ? ` · <span title="estimated from the time ratings">${esc(fmtDays(r.edges.reduce((s, id) => s + timeToDays(b.edges[id].cost?.time), 0)))} to go</span>` : ''}</div>`;
}"""

new_rp = """function renderProgress(b, r, w) {
  const goalDone = b.nodes[b.goalId].done;
  const full = astar(b, w, { fromStart: true });

  const stateNodes = Object.values(b.nodes).filter(n => n.kind === 'state');
  const doneStates = stateNodes.filter(n => n.done).length;
  const allEdges = Object.values(b.edges);
  const totalSteps = allEdges.reduce((sum, e) => sum + (e.steps?.length || 0), 0);
  const doneSteps = allEdges.reduce((sum, e) => sum + (e.steps?.filter(s => s.done).length || 0), 0);

  let pct = 0;
  if (goalDone) {
    pct = 100;
  } else if (stateNodes.length > 0) {
    const stateRatio = doneStates / stateNodes.length;
    const stepRatio = totalSteps > 0 ? (doneSteps / totalSteps) : stateRatio;
    const pathRatio = r.found && full.found && full.cost > 0 ? Math.max(0, Math.min(1, 1 - r.cost / full.cost)) : 0;
    pct = Math.round((stateRatio * 0.4 + stepRatio * 0.35 + pathRatio * 0.25) * 100);
    pct = Math.max(0, Math.min(99, pct));
  } else {
    pct = r.found && full.found && full.cost > 0 ? Math.round(Math.max(0, Math.min(1, 1 - r.cost / full.cost)) * 100) : 0;
  }
  if (!r.found && !goalDone && doneStates === 0 && doneSteps === 0) pct = 0;

  $('#progress').innerHTML = `
    <div class="pbar"><i style="width:${pct}%"></i></div>
    <div class="pmeta"><b>${pct}%</b> of the way${r.found && !goalDone ? ` · <span title="estimated from the time ratings">${esc(fmtDays(r.edges.reduce((s, id) => s + timeToDays(b.edges[id].cost?.time), 0)))} to go</span>` : ''}</div>`;
}"""

if old_rp in app_code:
    app_code = app_code.replace(old_rp, new_rp)
    print("Updated renderProgress in js/app.js")

# Update checklist ticking handler
old_ck_handler = "else if (t.dataset.step != null) { obj.steps[t.dataset.step].done = t.checked; full = true; }"
new_ck_handler = """else if (t.dataset.step != null) {
    const sIdx = Number(t.dataset.step);
    if (obj.steps && obj.steps[sIdx]) {
      obj.steps[sIdx].done = t.checked;
      full = true;
      if (t.checked) sound.play('pop');
      const toNode = b.nodes[obj.to];
      if (toNode) {
        const allDone = obj.steps.length > 0 && obj.steps.every(s => s.done);
        if (allDone && !toNode.done) {
          toNode.done = true;
          canvas.burst(toNode.id, 16);
          sound.play('ding');
        } else if (!allDone && toNode.done) {
          toNode.done = false;
        }
      }
    }
  }"""

if old_ck_handler in app_code:
    app_code = app_code.replace(old_ck_handler, new_ck_handler)
    print("Updated checklist handler in js/app.js")

# Add link banner helper and selectFirstEdge helper in js/app.js
helpers_code = """
function updateLinkBanner(fromId) {
  let bEl = document.getElementById('linkBanner');
  if (!fromId) {
    if (bEl) bEl.hidden = true;
    return;
  }
  if (!bEl) {
    bEl = document.createElement('div');
    bEl.id = 'linkBanner';
    bEl.className = 'link-banner';
    bEl.innerHTML = `<span id="linkBannerText"></span><button id="cancelLinkBtn">Cancel</button>`;
    document.body.appendChild(bEl);
    bEl.querySelector('#cancelLinkBtn').addEventListener('click', () => {
      canvas.setLinkMode(null);
      updateLinkBanner(null);
      toast('Connect cancelled');
    });
  }
  const b = board();
  const name = b?.nodes[fromId]?.label || 'Milestone';
  bEl.querySelector('#linkBannerText').textContent = `Connecting from "${name}": Click any destination milestone card (or Esc)`;
  bEl.hidden = false;
}

window.selectFirstEdge = () => {
  const b = board();
  if (!b) return;
  const firstEid = (lastPath?.edges && lastPath.edges[0]) || Object.keys(b.edges)[0];
  if (firstEid) {
    select({ type: 'edge', id: firstEid });
    if (window.canvas) window.canvas.centerOnEdge(firstEid, false);
  }
};
"""

if "function updateLinkBanner" not in app_code:
    app_code = app_code.replace("// ---------- boot ----------", helpers_code + "\n// ---------- boot ----------")
    print("Added link banner & selectFirstEdge helpers to js/app.js")

# Update setLinkMode calls to notify link banner
app_code = app_code.replace("canvas.setLinkMode(null); toast('Link cancelled');", "canvas.setLinkMode(null); updateLinkBanner(null); toast('Connect cancelled');")
app_code = app_code.replace("canvas.setLinkMode(null);", "canvas.setLinkMode(null); updateLinkBanner(null);")
app_code = app_code.replace("canvas.setLinkMode(id); toast('Click the state this leads to (click paper to cancel)');", "canvas.setLinkMode(id); updateLinkBanner(id); toast('Click destination milestone to connect');")

# Improve Inspector connect & sui UI
old_ins_btns = """        ${n.kind === 'goal' ? '' : '<button data-act="link">Link → state</button>'}
        ${n.kind === 'goal' ? '' : '<button data-act="child">+ Next state</button>'}'"""

new_ins_btns = """        ${n.kind === 'goal' ? '' : '<button data-act="link" title="Draw an action connector from this milestone to another">Connect to Milestone →</button>'}
        ${n.kind === 'goal' ? '' : '<button data-act="child" title="Add a connected milestone next in sequence">+ Next Milestone</button>'}'"""

app_code = app_code.replace("<button data-act=\"link\">Link → state</button>", "<button data-act=\"link\" title=\"Draw an action connector to another milestone\">Connect to Milestone →</button>")
app_code = app_code.replace("<button data-act=\"child\">+ Next state</button>", "<button data-act=\"child\" title=\"Add a new milestone linked after this one\">+ Next Milestone</button>")

# Add resource link template button handler
link_template_handler = """    if (act === 'add-link-template') {
      const ta = $('#inspector textarea[data-f="note"]');
      if (ta && obj) {
        const cur = ta.value.trim();
        ta.value = cur ? `${cur}\\n[Resource / Document](https://example.com)` : `[Resource / Document](https://example.com)`;
        obj.note = ta.value;
        persist();
        refresh({ inspector: false });
        ta.focus();
        toast('Resource link template added to Notes');
      }
      return;
    }"""

if "act === 'add-link-template'" not in app_code:
    app_code = app_code.replace("if (act === 'close') return select(null);", "if (act === 'close') return select(null);\n" + link_template_handler)
    print("Added add-link-template handler to js/app.js")

# Improve sui stamp box in inspector
old_sui_btn = """${n.kind === 'state' ? `<button class="sui-stamp-btn" data-act="sui-stamp" data-nodeid="${n.id}">${n.done ? 'Verify Milestone on Sui (Tatum RPC)' : 'Record Milestone Hash on Sui'}</button>` : ''}"""
new_sui_box = """${n.kind === 'state' ? `
      <div class="sui-box">
        <div style="font-family:'Space Grotesk',sans-serif; font-size:13px; font-weight:700; color:var(--ink); display:flex; align-items:center; justify-content:space-between;">
          <span>Cryptographic Proof</span>
          <span style="font-size:10px; font-weight:700; text-transform:uppercase; color:var(--muted); background:rgba(0,0,0,0.06); padding:1px 6px; border-radius:4px;">Optional</span>
        </div>
        <div style="font-size:11.5px; color:var(--muted); line-height:1.4; margin:5px 0 8px;">
          Optional: Record immutable cryptographic proof on Sui Mainnet via Tatum RPC. Perfect for client sign-offs or hackathons.
        </div>
        <button class="sui-stamp-btn" data-act="sui-stamp" data-nodeid="${n.id}" style="width:100%;">${n.done ? 'Stamp Verified Milestone on Sui (Tatum)' : 'Stamp Milestone Hash on Sui (Optional)'}</button>
      </div>` : ''}"""

if old_sui_btn in app_code:
    app_code = app_code.replace(old_sui_btn, new_sui_box)
    print("Updated sui proof box in js/app.js")

# Add link template button to inspector notes
old_state_notes = "<label>Notes <textarea data-f=\"note\" rows=\"4\" placeholder=\"Details, links, numbers…\">${esc(n.note)}</textarea></label>"
new_state_notes = """<label>Notes & Resources <span class="muted small">(links, attachments, contacts)</span> <textarea data-f="note" rows="3" placeholder="Details, links, numbers…">${esc(n.note)}</textarea></label>
      <div style="margin-top:-4px; margin-bottom:8px;"><button type="button" class="mini-add-link-btn" data-act="add-link-template" style="font-size:11px; padding:2px 8px; border-radius:4px; border:1px dashed var(--ink); background:transparent; cursor:pointer; color:var(--ink);">+ Add Resource Link</button></div>"""

if old_state_notes in app_code:
    app_code = app_code.replace(old_state_notes, new_state_notes)

old_edge_notes = "<label>Notes <textarea data-f=\"note\" rows=\"3\" placeholder=\"How, where, who, links…\">${esc(e.note)}</textarea></label>"
new_edge_notes = """<label>Notes & Resources <span class="muted small">(how, where, who, links)</span> <textarea data-f="note" rows="3" placeholder="How, where, who, links…">${esc(e.note)}</textarea></label>
      <div style="margin-top:-4px; margin-bottom:8px;"><button type="button" class="mini-add-link-btn" data-act="add-link-template" style="font-size:11px; padding:2px 8px; border-radius:4px; border:1px dashed var(--ink); background:transparent; cursor:pointer; color:var(--ink);">+ Add Resource Link</button></div>"""

if old_edge_notes in app_code:
    app_code = app_code.replace(old_edge_notes, new_edge_notes)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_code)
print("Updated js/app.js successfully")

# -------------------------------------------------------------
# 3. Update js/tour.js (8 Bulletproof, Clear Steps)
# -------------------------------------------------------------
tour_path = r"C:\Users\hmmm\goalstar-recall\js\tour.js"
with open(tour_path, "r", encoding="utf-8") as f:
    tour_code = f.read()

# Replace this.steps array
new_steps_code = """    this.steps = [
      {
        id: 'node-card',
        title: 'Step 1: Milestone Cards & Progress',
        text: 'Each card is a milestone. The striped progress bar moves dynamically as you check off subtasks, or turns solid when achieved.',
        onEnter: () => {
          window.clearSelect?.();
          const node = findTargetMilestone();
          if (node?.dataset?.id && window.canvas) {
            window.canvas.centerOn(node.dataset.id, false);
          }
        },
        targetSelector: () => findTargetMilestone()
      },
      {
        id: 'dream-button',
        title: 'Step 2: Dream with AI (Brainstorm & Branch)',
        text: 'Click "Dream" to let AI brainstorm and generate realistic milestones and connecting actions between where you are and your goal, so you never start with a blank canvas.',
        onEnter: () => {
          window.clearSelect?.();
        },
        targetSelector: () => document.getElementById('dreamBtn')
      },
      {
        id: 'best-path',
        title: 'Step 3: Best Path (A* Optimal Route)',
        text: 'The Best Path is the algorithm\\'s optimal calculated route. It shows the exact sequence of actions with the lowest combined friction (Time, Money, Effort, Risk) to reach your goal fastest.',
        onEnter: () => {
          document.body.classList.add('side-open');
          const p = document.getElementById('path');
          if (p) {
            p.removeAttribute('hidden');
            p.scrollIntoView?.({ behavior: 'auto', block: 'nearest' });
          }
        },
        targetSelector: () => document.querySelector('#path:not([hidden])') || document.querySelector('#path') || document.querySelector('.side')
      },
      {
        id: 'action-cost',
        title: 'Step 4: Action Connectors & Friction Costs',
        text: 'Connectors represent actions. The green pill (e.g. 1.4) is the friction cost combining Time, Money, Effort, and Risk. You also see estimated calendar time and subtask count.',
        onEnter: () => {
          window.clearSelect?.();
          const { edgeId } = findTargetEdgeAndCost();
          if (edgeId && window.canvas) {
            window.canvas.centerOnEdge(edgeId, false);
          } else if (window.canvas?.board) {
            const firstEdge = Object.values(window.canvas.board.edges)[0];
            if (firstEdge) window.canvas.centerOnEdge(firstEdge.id, false);
          }
        },
        targetSelector: () => findTargetEdgeAndCost().labelEl || findTargetEdgeAndCost().costEl
      },
      {
        id: 'action-checklist',
        title: 'Step 5: Checklist & Subtasks in Inspector',
        text: 'Break any action into concrete steps. Checking off items here directly moves the milestone\\'s progress bar on the board, keeping your momentum tangible.',
        onEnter: () => {
          if (window.selectFirstEdge) window.selectFirstEdge();
          const ins = document.getElementById('inspector');
          if (ins) {
            ins.hidden = false;
            const ck = ins.querySelector('.checklist');
            ck?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
          }
        },
        targetSelector: () => document.querySelector('#inspector .checklist') || document.querySelector('#inspector')
      },
      {
        id: 'inspector-notes',
        title: 'Step 6: Notes & Resources (Context)',
        text: 'Attach links, documents, contacts, and personal context directly to any milestone or action so everything you need stays together.',
        onEnter: () => {
          const ins = document.getElementById('inspector');
          if (ins) {
            ins.hidden = false;
            const note = ins.querySelector('textarea[data-f="note"]');
            note?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
          }
        },
        targetSelector: () => document.querySelector('#inspector textarea[data-f="note"]') || document.querySelector('#inspector')
      },
      {
        id: 'walrus-memory',
        title: 'Step 7: Walrus Portable Memory',
        text: 'Walrus stores your habits, past bottlenecks, and stamina rules decentralized on Walrus storage so GoalStar permanently remembers how you work across all devices.',
        onEnter: () => {
          document.body.classList.add('side-open');
          const w = document.getElementById('walrusTelemetry') || document.querySelector('.telemetry-box') || document.querySelector('.telemetry-pill');
          w?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
        },
        targetSelector: () => document.getElementById('walrusTelemetry') || document.querySelector('.telemetry-pill') || document.querySelector('.telemetry-box') || document.querySelector('.side')
      },
      {
        id: 'sui-inspector',
        title: 'Step 8: Optional Cryptographic Proof',
        text: 'When you finish a major deliverable, click here to stamp an immutable hash on Sui Mainnet via Tatum RPC. Perfect for client sign-offs or hackathons, but 100% optional for personal goals.',
        onEnter: () => {
          if (window.selectFirstStateNode) {
            window.selectFirstStateNode();
          }
          const ins = document.getElementById('inspector');
          if (ins) {
            ins.hidden = false;
            const suiBtn = ins.querySelector('.sui-box') || ins.querySelector('[data-act="sui-stamp"]') || ins.querySelector('.ins-head');
            suiBtn?.scrollIntoView?.({ behavior: 'auto', block: 'center' });
          }
        },
        targetSelector: () => document.querySelector('.sui-box') || document.querySelector('[data-act="sui-stamp"]') || document.querySelector('.ins-head') || document.querySelector('#inspector')
      }
    ];"""

steps_regex = r"    this\.steps = \[[\s\S]*?\n    \];"
if re.search(steps_regex, tour_code):
    tour_code = re.sub(steps_regex, new_steps_code, tour_code, count=1)
    print("Replaced this.steps in js/tour.js")
else:
    print("Warning: could not find this.steps in js/tour.js")

with open(tour_path, "w", encoding="utf-8") as f:
    f.write(tour_code)
print("Updated js/tour.js successfully")
