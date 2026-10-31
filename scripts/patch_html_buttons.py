import re

p = r"C:\Users\hmmm\goalstar-recall\index.html"
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

# Replace tour button in header
html = re.sub(
    r'<button id="tourBtn"[^>]*>.*?</button>',
    '<button id="tourBtn" class="tour-nav-btn" title="Replay Walkthrough Tour">🎓 Walkthrough Tour</button>',
    html
)

# Add sideTourBtn
if 'id="sideTourBtn"' not in html:
    html = html.replace(
        '<section class="danger-zone">',
        '<section class="tour-resee-box">\n        <button id="sideTourBtn" class="tour-side-btn">🎓 Replay Product Tour</button>\n      </section>\n      <section class="danger-zone">'
    )

with open(p, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html successfully!")
