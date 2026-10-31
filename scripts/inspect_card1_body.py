import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1880, 1912):
    print(f"{i+1}: {lines[i].strip()}")
