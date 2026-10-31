import os

# 1. Update css/style.css
css_path = r"C:\Users\hmmm\goalstar-recall\css\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css_text = f.read().replace("\r\n", "\n")

target_card_css = """.sketch-card-container {
  position: absolute;
  width: 400px;
  max-width: calc(100vw - 32px);
  z-index: 10002;
  pointer-events: auto;
  animation: sketchPop 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  transition: top 0.22s cubic-bezier(0.16, 1, 0.3, 1), left 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes sketchPop {
  0% { transform: scale(0.96) translateY(4px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}

.sketch-card {
  background: var(--panel, #ffffff);
  border: 2px solid var(--ink, #1c1917);
  border-radius: 16px;
  padding: 18px 22px 16px;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.22), 0 3px 8px rgba(0, 0, 0, 0.12), 4px 5px 0px rgba(42, 45, 62, 0.85);
  position: relative;
  font-family: inherit;
}"""

repl_card_css = """.sketch-card-container {
  position: absolute;
  width: 380px;
  max-width: calc(100vw - 28px);
  max-height: calc(100vh - 85px);
  z-index: 10002;
  pointer-events: auto;
  animation: sketchPop 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  transition: top 0.18s cubic-bezier(0.16, 1, 0.3, 1), left 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes sketchPop {
  0% { transform: scale(0.96) translateY(4px); opacity: 0; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}

.sketch-card {
  background: var(--panel, #ffffff);
  border: 2px solid var(--ink, #1c1917);
  border-radius: 14px;
  padding: 13px 18px 12px;
  max-height: calc(100vh - 90px);
  overflow-y: auto;
  box-sizing: border-box;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.22), 0 3px 8px rgba(0, 0, 0, 0.12), 4px 5px 0px rgba(42, 45, 62, 0.85);
  position: relative;
  font-family: inherit;
}"""

assert target_card_css in css_text, "target_card_css not found"
css_text = css_text.replace(target_card_css, repl_card_css)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_text)
print("Updated css/style.css card clipping safety")
