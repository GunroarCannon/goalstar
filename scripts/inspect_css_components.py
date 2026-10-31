import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\css\style.css', 'r', encoding='utf-8') as f:
    text = f.read()

for term in ['sui-stamp-btn', 'walrus-banner', 'walrus-panel', 'path-profile']:
    idx = text.find(term)
    if idx != -1:
        print(f"=== {term} ===")
        print(text[idx-20:idx+300])
