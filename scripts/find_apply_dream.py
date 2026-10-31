import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\js\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
while True:
    pos = text.find('applyDream', idx)
    if pos == -1: break
    print("MATCH at", pos)
    print(text[max(0, pos-100):min(len(text), pos+200)])
    idx = pos + 1
