import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

script_start = text.find('<script type="module">')
script_content = text[script_start:]

for term in ['theme', 'dark', 'sound', 'audio', 'switch', 'localStorage']:
    matches = [line.strip() for line in script_content.splitlines() if term in line.lower()]
    print(f"Term '{term}': {len(matches)} lines found")
    for m in matches[:3]:
        print("   ", m[:100])
