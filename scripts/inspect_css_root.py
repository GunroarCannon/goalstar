import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\css\style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(min(120, len(lines))):
    print(lines[i].rstrip())
