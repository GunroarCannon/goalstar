with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_css = """.landing-main {
      position: relative;
      z-index: 1;
      max-width: 1200px;
      margin: 0 auto;
    }"""

new_css = """main.landing-main {
      display: block !important;
      position: relative !important;
      z-index: 1 !important;
      max-width: 1200px !important;
      width: 100% !important;
      margin: 0 auto !important;
      box-sizing: border-box !important;
      overflow-x: hidden !important;
    }"""

assert old_css in c, "old_css not found"
c = c.replace(old_css, new_css)

with open('goalstar-recall/home.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Patched main.landing-main!")
