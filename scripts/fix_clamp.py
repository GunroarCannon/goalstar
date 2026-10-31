print("Updating card clamping in tour.js and style.css...")

tour_path = r"C:\Users\hmmm\goalstar-recall\js\tour.js"
with open(tour_path, "r", encoding="utf-8") as f:
    tour = f.read()

# Update cardH to 295 and sui-inspector top calculation
tour = tour.replace("const cardH = 265;", "const cardH = 295;")
tour = tour.replace(
    "cardPos.top = Math.max(minCardTop, Math.min(maxCardTop, spotY - 30));",
    "cardPos.top = Math.max(minCardTop, Math.min(maxCardTop, spotY - 80));"
)

# Improve post-DOM clamp
old_clamp = """    const containerEl = this.overlay.querySelector('.sketch-card-container');
    if (containerEl) {
      const r = containerEl.getBoundingClientRect();
      if (r.bottom > window.innerHeight - 18) {
        const shift = r.bottom - (window.innerHeight - 18);
        containerEl.style.top = Math.max(75, r.top - shift) + 'px';
      }
      if (r.top < 75) {
        containerEl.style.top = '75px';
      }
      if (r.right > window.innerWidth - 16) {
        containerEl.style.left = Math.max(16, window.innerWidth - cardW - 16) + 'px';
      }
    }"""

new_clamp = """    const containerEl = this.overlay.querySelector('.sketch-card-container');
    if (containerEl) {
      const r = containerEl.getBoundingClientRect();
      const actualH = r.height || 280;
      if (r.bottom > window.innerHeight - 20) {
        const correctTop = Math.max(75, window.innerHeight - actualH - 24);
        containerEl.style.top = `${correctTop}px`;
      }
      if (parseFloat(containerEl.style.top) < 75) {
        containerEl.style.top = '75px';
      }
      if (r.right > window.innerWidth - 16) {
        containerEl.style.left = Math.max(16, window.innerWidth - cardW - 16) + 'px';
      }
    }"""

tour = tour.replace(old_clamp, new_clamp)

with open(tour_path, "w", encoding="utf-8") as f:
    f.write(tour)
print("Updated js/tour.js")

css_path = r"C:\Users\hmmm\goalstar-recall\css\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Remove transition from .sketch-card-container so it snaps instantly without lag
css = css.replace(
    "  transition: top 0.18s cubic-bezier(0.16, 1, 0.3, 1), left 0.18s cubic-bezier(0.16, 1, 0.3, 1);\n",
    ""
)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
print("Updated css/style.css")
