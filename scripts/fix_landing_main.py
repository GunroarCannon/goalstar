path = r'C:\Users\hmmm\goalstar-recall\home.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

rule = """
    body.landing-body main,
    .landing-body main,
    main.landing-main {
      display: block !important;
      flex-direction: column !important;
      height: auto !important;
      min-height: auto !important;
      flex: none !important;
      overflow: visible !important;
    }
"""

c = c.replace('<main>', '<main class="landing-main">', 1)
target = 'overflow-y: auto !important;\n    }'
if target in c:
    c = c.replace(target, target + rule, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated main style in home.html successfully')
