import sys

with open(r'C:\Users\hmmm\goalstar-recall\js\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

guide_listener = """
  // UI Explainer Guide Modal handlers
  const guideDlg = document.getElementById('uiGuideDlg');
  document.getElementById('uiGuideBtn')?.addEventListener('click', () => {
    sound.play('pop');
    if (guideDlg && typeof guideDlg.showModal === 'function') guideDlg.showModal();
    else if (guideDlg) guideDlg.setAttribute('open', 'true');
  });
  document.querySelectorAll('#closeUiGuideBtn, #closeGuideDlgBtn').forEach(b => {
    b.addEventListener('click', () => {
      sound.play('click');
      if (guideDlg && typeof guideDlg.close === 'function') guideDlg.close();
      else if (guideDlg) guideDlg.removeAttribute('open');
    });
  });
  document.getElementById('launchTourFromGuideBtn')?.addEventListener('click', () => {
    if (guideDlg && typeof guideDlg.close === 'function') guideDlg.close();
    else if (guideDlg) guideDlg.removeAttribute('open');
    sound.play('click');
    if (window.tour && typeof window.tour.start === 'function') window.tour.start(true);
  });
"""

idx = text.rfind('// End of app')
if idx == -1:
    idx = len(text)

text = text[:idx] + guide_listener + text[idx:]

with open(r'C:\Users\hmmm\goalstar-recall\js\app.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added UI guide modal listeners to js/app.js!")
