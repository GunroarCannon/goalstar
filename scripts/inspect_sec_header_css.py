import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\.sec-header[\s\S]*?\{[\s\S]*?\}', text)
for m in matches:
    print(m)
