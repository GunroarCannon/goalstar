import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's verify structure
print("Length of home.html:", len(content))
