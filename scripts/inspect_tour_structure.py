import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\js\tour.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(15, min(100, len(lines))):
    print(lines[i].rstrip())
