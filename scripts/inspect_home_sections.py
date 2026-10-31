import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines):
    if any(k in line for k in ['<header', '</header>', '<section', '</section>', '<main', '</main>', 'id="hero"', 'id="simulator"', 'id="usecases"', 'id="bgHumaaansLayer"', '<script>']):
        print(f"{idx+1}: {line.strip()[:100]}")
