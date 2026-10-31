with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace engraved-btn in home.html with album-btn
text = text.replace('class="engraved-btn launch-btn"', 'class="album-btn primary-tape launch-btn"')
text = text.replace('class="engraved-btn scenario-launch-btn"', 'class="album-btn scenario-launch-btn"')
text = text.replace('class="engraved-btn"', 'class="album-btn secondary-tape"')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('[OK] Updated all buttons in home.html to photo album tape buttons!')
