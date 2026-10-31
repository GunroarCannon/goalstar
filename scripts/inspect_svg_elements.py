import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="journeySvgPath"')
print(text[idx-200:idx+400])
