import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\js\tour.js', 'r', encoding='utf-8') as f:
    text = f.read()

print(f"tour.js length: {len(text)}")
print(text[:1500])
