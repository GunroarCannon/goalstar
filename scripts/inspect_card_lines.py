import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'uc-card-header' in line:
        for j in range(max(0, i-3), min(len(lines), i+5)):
            print(f"{j+1}: {lines[j].strip()}")
        print("-" * 40)
