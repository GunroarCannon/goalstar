import re

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('=== home.html switches ===')
for m in re.finditer(r'<div class="engraved-switch[\s\S]*?</div>\s*</div>', text):
    print(m.group(0))
    print('---')

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'r', encoding='utf-8') as f:
    text2 = f.read()

print('=== index.html switches ===')
for m in re.finditer(r'<div class="engraved-switch[\s\S]*?</div>\s*</div>', text2):
    print(m.group(0))
    print('---')
