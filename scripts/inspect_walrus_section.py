import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\css\style.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('/* ---- Total Recall: Walrus Memory & Tatum Sui Styles ---- */')
print(text[idx:idx+1500])
