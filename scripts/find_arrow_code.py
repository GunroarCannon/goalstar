import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find where travelingArrow is updated
idx = text.find('travelingArrow')
while idx != -1:
    print("--- OCCURRENCE ---")
    start = max(0, idx - 200)
    end = min(len(text), idx + 400)
    print(text[start:end])
    idx = text.find('travelingArrow', idx + 1)
