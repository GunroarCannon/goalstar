import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\scripts\test_final_experience.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(130, min(len(lines), 180)):
    print(f"{i+1}: {lines[i].rstrip()}")
