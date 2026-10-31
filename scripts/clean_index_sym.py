import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('⟳ Sync now', 'Sync now')
with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Sanitized index.html")
