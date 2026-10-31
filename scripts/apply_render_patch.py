import re

print("Applying patches to goalstar-recall...")

# 1. Patch js/render.js
render_path = r"C:\Users\hmmm\goalstar-recall\js\render.js"
with open(render_path, "r", encoding="utf-8") as f:
    render_code = f.read()

# Replace cardHtml
old_card_pattern = r"  cardHtml\(n, o, show, hMax\) \{[\s\S]*?return `[\s\S]*?`\s*;\s*\}"

new_card_code = """  cardHtml(n, o, show, hMax) {
    const kindTag = n.kind === 'goal' ? 'Goal' : n.kind === 'start' ? 'You are here' : '';
    const g = o.g?.get(n.id);
    const h = n.kind === 'goal' ? 0 : n.h;

    // Check incoming actions leading to this node
    const incoming = this.board ? Object.values(this.board.edges).filter(e => e.to === n.id) : [];
    const totalSteps = incoming.reduce((sum, e) => sum + (e.steps?.length || 0), 0);
    const doneSteps = incoming.reduce((sum, e) => sum + (e.steps?.filter(s => s.done).length || 0), 0);

    let progress = null;
    let titleHint = 'Closeness to the goal';

    if (n.kind === 'start') {
      progress = 0;
    } else if (n.done) {
      progress = 1.0;
      titleHint = 'Milestone achieved (100%)';
    } else if (totalSteps > 0) {
      // Checklist completion directly drives progress!
      progress = doneSteps / totalSteps;
      titleHint = `${doneSteps}/${totalSteps} checklist steps completed (${Math.round(progress * 100)}%)`;
    } else if (n.kind === 'goal') {
      progress = 0;
    } else if (Number.isFinite(h) && hMax > 0) {
      progress = Math.max(0, Math.min(1, 1 - h / hMax));
      titleHint = `Heuristic progress (${Math.round(progress * 100)}%)`;
    }

    const pct = progress != null ? Math.round(progress * 100) : 0;
    const stepBadge = totalSteps > 0 ? `<span class="card-step-badge" title="${doneSteps} of ${totalSteps} checklist steps completed">${doneSteps}/${totalSteps}</span>` : '';
    const nums = show.numbers !== false && n.kind !== 'start'
      ? `<span>h ${fmt(h)}</span>${g != null && g > 0 ? `<span>g ${fmt(g)}</span>` : ''}` : '';

    return `
      ${n.kind === 'start' ? '' : `<button class="tick" title="${n.done ? 'Achieved — click to undo' : 'Mark as achieved'}">${n.done ? 'Done' : ''}</button>`}
      ${kindTag ? `<div class="nk">${kindTag}</div>` : ''}
      <div class="nl">${esc(n.label)}</div>
      ${show.notes !== false && n.note && n.kind !== 'start' ? `<div class="nn">${esc(n.note)}</div>` : ''}
      ${nums || progress != null ? `<div class="nm">${nums}${stepBadge}${progress != null && n.kind === 'state' ? `<span class="near" title="${esc(titleHint)}"><i style="width:${pct}%"></i></span>` : ''}</div>` : ''}`;
  }"""

if re.search(old_card_pattern, render_code):
    render_code = re.sub(old_card_pattern, new_card_code, render_code, count=1)
    with open(render_path, "w", encoding="utf-8") as f:
        f.write(render_code)
    print("Successfully patched js/render.js")
else:
    print("Warning: could not find cardHtml in js/render.js")

