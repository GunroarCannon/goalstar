import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.sec-header')
print(text[idx:idx+800])
