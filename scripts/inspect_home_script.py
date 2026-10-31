with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<script type="module">([\s\S]*?)</script>', text)
if m:
    print(m.group(1)[:1000])
