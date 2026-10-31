import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\js\tour.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
step_titles = re.findall(r"title:\s*['\"]([^'\"]+)['\"]", text)
print("Tour step titles in tour.js:")
for idx, title in enumerate(step_titles):
    print(f"  {idx+1}: {title}")
