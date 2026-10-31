import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="settingsDlg"')
print(text[idx:idx+1000])
