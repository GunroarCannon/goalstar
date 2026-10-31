import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
cards = re.findall(r'<div class="card-bay"[^>]*>.*?<\/div>\s*<\/div>\s*<\/div>', text, re.DOTALL)
print(f"Total card bays found: {len(cards)}")
for i, c in enumerate(cards, 1):
    print(f"--- CARD {i} ---")
    safe_c = c.encode('ascii', errors='backslashreplace').decode('ascii')
    for line in safe_c.splitlines()[:15]:
        print("  ", line)
