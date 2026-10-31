with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = "body.landing-body {"
replacement = """html:has(body.landing-body), body.landing-body {
      height: auto !important;
      min-height: 100vh !important;
      overflow-x: hidden !important;
      overflow-y: auto !important;
    }
    body.landing-body {"""

assert target in c, "target not found"
c = c.replace(target, replacement)

with open('goalstar-recall/home.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated body.landing-body overflow to auto!")
