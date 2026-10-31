import sys

with open(r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.traveling-arrow {')
print(text[idx:idx+400])
