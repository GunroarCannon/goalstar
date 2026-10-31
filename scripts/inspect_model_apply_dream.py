import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\js\model.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('export function applyDream')
if idx == -1:
    idx = text.find('function applyDream')
print(text[idx:idx+2500])
