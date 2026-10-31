import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1035, 1145):
    if i < len(lines):
        line = lines[i].encode('ascii', errors='backslashreplace').decode('ascii')
        print(f"{i+1}: {line}", end='')
