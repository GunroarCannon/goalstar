import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\css\style.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'[^\n]*walrus[^\n]*', text, re.IGNORECASE)
for m in matches[:15]:
    print(m)
