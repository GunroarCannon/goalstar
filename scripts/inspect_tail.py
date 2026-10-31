import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(1368, len(lines)):
    line = lines[idx]
    if any(k in line for k in ['<footer', '</footer', '<div class="login-dialog', '<div class="home-tour', '<script', '</script', 'function ', 'window.addEventListener', 'document.getElementById']):
        print(f"{idx+1}: {line.strip()[:100]}")
