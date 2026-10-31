import re

home_path = r'C:\Users\hmmm\goalstar-recall\home.html'

with open(home_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Ensure landing-html class on html tag
html = html.replace('<html lang="en">', '<html lang="en" class="landing-html">', 1)

# Fix landing body layout so hero and use cases stack vertically
old_css = """.landing-body {
      overflow-x: hidden;
      min-height: 100vh;
      background: var(--paper);
      color: var(--ink);
      font-family: 'Patrick Hand', var(--ui);
    }"""

new_css = """html.landing-html, body.landing-body {
      height: auto !important;
      min-height: 100vh;
      display: block !important;
      overflow-x: hidden !important;
      overflow-y: auto !important;
    }
    .landing-body {
      background: var(--paper);
      color: var(--ink);
      font-family: 'Patrick Hand', var(--ui);
    }
    .landing-body main {
      display: block !important;
      min-height: auto !important;
      height: auto !important;
      flex: none !important;
    }"""

if old_css in html:
    html = html.replace(old_css, new_css, 1)

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated home.html layout styles successfully')
