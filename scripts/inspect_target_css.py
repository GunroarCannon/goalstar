import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.card5-target-')
print(text[idx:idx+800])
