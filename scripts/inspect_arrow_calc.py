import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('// 6. Precision Traveling Arrow')
print(text[idx:idx+1200])
