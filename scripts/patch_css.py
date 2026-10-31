import os

path = r"C:\Users\hmmm\goalstar-recall\css\style.css"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

norm_text = text.replace("\r\n", "\n")

target1 = """.sketch-card-container {
  position: absolute;
  width: 310px;
  max-width: calc(100vw - 24px);
  z-index: 10002;
  pointer-events: auto;
  animation: sketchPop 0.2s ease-out;
  transition: top 0.2s cubic-bezier(0.16, 1, 0.3, 1), left 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes sketchPop {
  0% { transform: scale(0.95) rotate(-0.6deg); opacity: 0; }
  100% { transform: scale(1) rotate(0); opacity: 1; }
}

.sketch-card {
  background: var(--paper);
  border: 2px solid var(--ink);
  border-radius: 160px 12px 140px 12px/12px 140px 12px 160px;
  padding: 11px 14px 10px;
  box-shadow: 3px 4px 0px rgba(42, 45, 62, 0.85), 0 8px 20px rgba(0,0,0,0.2);
  position: relative;
  font-family: inherit;
}

.sketch-pin {
  position: absolute;
  top: -9px;
  left: 12px;
  font-size: 15px;
  transform: rotate(-15deg);
}

.sketch-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3px;
}

.sketch-badge {
  font-family: var(--hand, 'Patrick Hand', cursive);
  font-size: 11px;
  font-weight: 700;
  color: #a87500;
  background: #fef3c7;
  border: 1px dashed #d97706;
  padding: 1px 6px;
  border-radius: 8px;
}

.sketch-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--muted);
  line-height: 1;
}
.sketch-close:hover {
  color: var(--ink);
}

.sketch-title {
  font-family: 'Caveat', cursive, sans-serif;
  font-size: 17px;
  font-weight: 700;
  color: var(--ink);
  margin: 2px 0 4px;
  line-height: 1.15;
}

.sketch-text {
  font-family: 'Patrick Hand', cursive, sans-serif;
  font-size: 13px;
  line-height: 1.38;
  color: var(--ink-soft);
  margin-bottom: 8px;
}

.sketch-text code {
  background: #fef08a;
  padding: 1px 4px;
  border-radius: 3px;
  font-family: monospace;
  font-size: 11.5px;
  border: 1px solid #eab308;
}

.sketch-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px dashed var(--border);
  padding-top: 8px;
}

.sketch-link {
  background: none;
  border: none;
  color: var(--muted);
  font-family: 'Patrick Hand', cursive;
  font-size: 11.5px;
  cursor: pointer;
  text-decoration: underline;
}
.sketch-link:hover {
  color: var(--ink);
}

.sketch-nav {
  display: flex;
  gap: 8px;
}

.sketch-btn {
  font-family: 'Patrick Hand', cursive;
  font-size: 13px;
  font-weight: 700;
  padding: 3px 12px;
  border-radius: 120px 8px 110px 8px/8px 110px 8px 120px;
  border: 1.5px solid var(--ink);
  cursor: pointer;
  transition: transform 0.1s ease;
}
.sketch-btn:hover {
  transform: translateY(-1.5px);
}
.sketch-btn.primary {
  background: #f59e0b;
  color: #fff;
  box-shadow: 2px 2px 0 var(--ink);
}
.sketch-btn.secondary {
  background: #fff;
  color: var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
}"""

repl1 = """.sketch-card-container {
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
}

.sketch-pin {
  position: absolute;
  top: -10px;
  left: 18px;
  font-size: 16px;
  transform: rotate(-12deg);
}

.sketch-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.sketch-badge {
  font-family: 'Space Grotesk', system-ui, -apple-system, sans-serif;
  font-size: 11.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #b45309;
  background: #fef3c7;
  border: 1px solid #f59e0b;
  padding: 3px 9px;
  border-radius: 6px;
}

.sketch-close {
  background: none;
  border: none;
  font-size: 22px;
  font-weight: 600;
  cursor: pointer;
  color: var(--muted, #64748b);
  line-height: 1;
  padding: 0 4px;
  border-radius: 4px;
  transition: color 0.15s ease;
}
.sketch-close:hover {
  color: var(--ink, #0f172a);
}

.sketch-title {
  font-family: 'Newsreader', Georgia, serif;
  font-size: 21px;
  font-weight: 800;
  color: var(--ink, #1c1917);
  margin: 4px 0 8px;
  line-height: 1.25;
  letter-spacing: -0.01em;
}

.sketch-text {
  font-family: 'Space Grotesk', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 15.5px;
  line-height: 1.55;
  font-weight: 500;
  color: var(--ink, #1c1917);
  margin-bottom: 14px;
}

.sketch-text code {
  background: #fef08a;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 13.5px;
  font-weight: 700;
  border: 1px solid #eab308;
  color: #854d0e;
}

.sketch-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px dashed var(--border, #cbd5e1);
  padding-top: 12px;
}

.sketch-link {
  background: none;
  border: none;
  color: var(--muted, #64748b);
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.sketch-link:hover {
  color: var(--ink, #0f172a);
}

.sketch-nav {
  display: flex;
  gap: 10px;
}

.sketch-btn {
  font-family: 'Space Grotesk', system-ui, sans-serif;
  font-size: 14px;
  font-weight: 700;
  padding: 7px 18px;
  border-radius: 8px;
  border: 1.5px solid var(--ink, #1c1917);
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.sketch-btn:hover {
  transform: translateY(-1.5px);
}
.sketch-btn.primary {
  background: var(--accent, #059669);
  color: #fff;
  border-color: #047857;
  box-shadow: 2px 2px 0 var(--ink, #1c1917);
}
.sketch-btn.secondary {
  background: #fff;
  color: var(--ink, #1c1917);
  box-shadow: 2px 2px 0 var(--ink, #1c1917);
}

@keyframes tourSpotlightPulse {
  0% { stroke-opacity: 0.95; stroke-width: 2.5px; }
  50% { stroke-opacity: 0.45; stroke-width: 3.5px; }
  100% { stroke-opacity: 0.95; stroke-width: 2.5px; }
}
.tour-spotlight-ring {
  animation: tourSpotlightPulse 1.8s infinite ease-in-out;
}"""

assert target1 in norm_text, "target1 not found in style.css"
norm_text = norm_text.replace(target1, repl1)

with open(path, "w", encoding="utf-8") as f:
    f.write(norm_text)
print("Updated css/style.css successfully")
