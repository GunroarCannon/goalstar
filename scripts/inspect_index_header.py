import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<header>')
end_idx = text.find('</header>')
print(text[idx:end_idx+9])
