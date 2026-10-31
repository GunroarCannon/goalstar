import re

# 1. Update css/style.css
css_path = r"C:\Users\hmmm\goalstar-recall\css\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Replace sketchPop animation without transform
css = css.replace(
    "@keyframes sketchPop {\n  0% { transform: scale(0.96) translateY(4px); opacity: 0; }\n  100% { transform: scale(1) translateY(0); opacity: 1; }\n}",
    "@keyframes sketchPop {\n  0% { opacity: 0; }\n  100% { opacity: 1; }\n}"
)
css = css.replace("animation: sketchPop 0.22s cubic-bezier(0.16, 1, 0.3, 1);", "animation: sketchPop 0.15s ease-out;")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
print("Updated css/style.css")

# 2. Update js/tour.js
tour_path = r"C:\Users\hmmm\goalstar-recall\js\tour.js"
with open(tour_path, "r", encoding="utf-8") as f:
    tour = f.read()

tour = tour.replace("const cardH = 265;", "const cardH = 305;")
tour = tour.replace("const cardH = 295;", "const cardH = 305;")
tour = tour.replace(
    "const maxCardTop = Math.max(75, window.innerHeight - cardH - 24);",
    "const maxCardTop = Math.max(75, window.innerHeight - cardH - 30);"
)

old_clamp_pattern = r"    const containerEl = this\.overlay\.querySelector\('\.sketch-card-container'\);[\s\S]*?if \(r\.left < 16\) \{\s*containerEl\.style\.left = '16px';\s*\}"

new_clamp_code = """    const containerEl = this.overlay.querySelector('.sketch-card-container');
    if (containerEl) {
      const r = containerEl.getBoundingClientRect();
      if (r.bottom > window.innerHeight - 25) {
        const shift = r.bottom - (window.innerHeight - 25);
        containerEl.style.top = Math.max(75, r.top - shift) + 'px';
      }
      if (parseFloat(containerEl.style.top) < 75) {
        containerEl.style.top = '75px';
      }
      if (r.right > window.innerWidth - 16) {
        const shift = r.right - (window.innerWidth - 16);
        containerEl.style.left = Math.max(16, r.left - shift) + 'px';
      }
      if (r.left < 16) {
        containerEl.style.left = '16px';
      }
    }"""

if re.search(old_clamp_pattern, tour):
    tour = re.sub(old_clamp_pattern, new_clamp_code, tour, count=1)
    print("Replaced post-DOM clamp in js/tour.js")
else:
    print("Warning: regex did not match clamp in js/tour.js")

with open(tour_path, "w", encoding="utf-8") as f:
    f.write(tour)
print("Updated js/tour.js")
