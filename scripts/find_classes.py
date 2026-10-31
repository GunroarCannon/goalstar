import re

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'class="[^"]*(?:cost|elabel|nm)[^"]*"', text)
print('Matches in index.html:', set(matches))
