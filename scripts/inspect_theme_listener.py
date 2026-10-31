import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'themeSwitch.*?addEventListener.*?\n.*?\n.*?\n.*?\n.*?\n', text)
if match:
    print("Event listener found:\n", match.group(0))
else:
    # Search where themeSwitch is referenced
    for line in text.splitlines():
        if 'themeSwitch' in line:
            print("LINE:", line)
