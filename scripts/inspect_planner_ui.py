import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('goalstar-recall/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Has WHERE YOU ARE:", "WHERE YOU ARE" in text or "where you are" in text.lower())
print("Has PATH PROFILE:", "PATH PROFILE" in text or "path profile" in text.lower())
print("Has BEST PATH:", "BEST PATH" in text or "best path" in text.lower())
print("Has Verified on Sui:", "Verified on Sui" in text or "verified on sui" in text.lower())
