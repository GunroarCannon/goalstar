import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Has overcomeHeaderBox:', 'id="overcomeHeaderBox"' in text)
print('Has overcome-header-box CSS:', '.overcome-header-box' in text)
print('Has zoom in script:', 'overcomeBox.style.transform' in text)

emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf]')
emojis = emoji_pattern.findall(text)
print('Emoji count:', len(emojis))
