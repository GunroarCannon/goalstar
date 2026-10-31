import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]')

matches = []
for idx, line in enumerate(text.splitlines(), 1):
    found = emoji_pattern.findall(line)
    if found:
        hex_codes = [hex(ord(c)) for c in found]
        matches.append((idx, hex_codes, line.strip()))

print(f"Total lines with emojis in home.html: {len(matches)}")
for idx, codes, line in matches:
    safe_line = line.encode('ascii', errors='backslashreplace').decode('ascii')
    print(f"L{idx} {codes}: {safe_line[:80]}")
