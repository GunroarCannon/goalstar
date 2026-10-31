import re

home_path = r'C:\Users\hmmm\goalstar-recall\home.html'

with open(home_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove unused sculpture & thinker CSS
old_sculpture_css = r'/\* Paper Cutout Head Sculpture \(Reference 1 & 2\) \*/[\s\S]*?/\* Live Interactive Simulator Widget \*/'
new_sim_css = '/* Live Interactive Simulator Widget */'
text = re.sub(old_sculpture_css, new_sim_css, text)

# Remove unused thinker overlay CSS
old_thinker_css = r'\.sculpture-switch-row[\s\S]*?@keyframes fadeIn[\s\S]*?\}'
text = re.sub(old_thinker_css, '', text)

# Remove unused thinker JS listener
old_thinker_js = r'// Thinker Statue Toggle[\s\S]*?}\s*}\s*'
text = re.sub(old_thinker_js, '', text)

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('[OK] Cleaned up unused sculpture and thinker code from home.html!')
