import os

path = r"C:\Users\hmmm\goalstar-recall\js\app.js"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

norm_text = text.replace("\r\n", "\n")

# 1. Update Sui button in inspector
t1 = """      ${n.done ? `<button class="sui-stamp-btn" data-act="sui-stamp" data-nodeid="${n.id}">Verify Milestone on Sui (Tatum RPC)</button>` : ''}"""
r1 = """      ${n.kind === 'state' ? `<button class="sui-stamp-btn" data-act="sui-stamp" data-nodeid="${n.id}">${n.done ? 'Verify Milestone on Sui (Tatum RPC)' : 'Record Milestone Hash on Sui'}</button>` : ''}"""

assert t1 in norm_text, "t1 not found"
norm_text = norm_text.replace(t1, r1)

# 2. Add canvas and window helper bindings
t2 = """window.addEventListener('resize', () => board() && canvas.drawMinimapSoon());
window.selectNode = (id) => select({ type: 'node', id });
window.selectFirstStateNode = () => {
  const b = board();
  if (!b) return null;
  const stateNode = Object.values(b.nodes).find(n => n.kind === 'state') || Object.values(b.nodes)[0];
  if (stateNode) {
    select({ type: 'node', id: stateNode.id });
    return stateNode.id;
  }
  return null;
};
window.clearSelect = () => select(null);"""

r2 = """window.addEventListener('resize', () => board() && canvas.drawMinimapSoon());
window.canvas = canvas;
window.centerNode = (id, anim) => canvas.centerOn(id, anim);
window.centerEdge = (id, anim) => canvas.centerOnEdge(id, anim);
window.selectNode = (id) => select({ type: 'node', id });
window.selectFirstStateNode = () => {
  const b = board();
  if (!b) return null;
  const stateNode = Object.values(b.nodes).find(n => n.kind === 'state') || Object.values(b.nodes)[0];
  if (stateNode) {
    select({ type: 'node', id: stateNode.id });
    return stateNode.id;
  }
  return null;
};
window.clearSelect = () => select(null);

function stopTourBounce() {
  try {
    localStorage.setItem('goalstar_tour_clicked', 'true');
  } catch (e) {}
  document.querySelectorAll('.tour-bounce-btn').forEach(btn => btn.classList.remove('tour-bounce-btn'));
}
window.stopTourBounce = stopTourBounce;
if (localStorage.getItem('goalstar_tour_clicked') === 'true' || localStorage.getItem('goalstar_walkthrough_completed') === 'true') {
  stopTourBounce();
}"""

assert t2 in norm_text, "t2 not found"
norm_text = norm_text.replace(t2, r2)

# 3. Attach stopTourBounce on tour buttons at end of file
t3 = """  document.getElementById('launchTourFromGuideBtn')?.addEventListener('click', () => {
    if (guideDlg && typeof guideDlg.close === 'function') guideDlg.close();
    else if (guideDlg) guideDlg.removeAttribute('open');
    sound.play('click');
    if (window.tour && typeof window.tour.start === 'function') window.tour.start(true);
  });"""

r3 = """  document.getElementById('launchTourFromGuideBtn')?.addEventListener('click', () => {
    stopTourBounce();
    if (guideDlg && typeof guideDlg.close === 'function') guideDlg.close();
    else if (guideDlg) guideDlg.removeAttribute('open');
    sound.play('click');
    if (window.tour && typeof window.tour.start === 'function') window.tour.start(true);
  });
  document.getElementById('tourBtn')?.addEventListener('click', () => {
    stopTourBounce();
  });
  document.getElementById('sideTourBtn')?.addEventListener('click', () => {
    stopTourBounce();
  });"""

assert t3 in norm_text, "t3 not found"
norm_text = norm_text.replace(t3, r3)

with open(path, "w", encoding="utf-8") as f:
    f.write(norm_text)
print("Updated js/app.js successfully")
