import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

cards = re.findall(r'<div[^>]*class="[^"]*uc-card[^"]*"[^>]*>', text)
print("Found cards count:", len(cards))
for c in cards:
    print("CARD:", c)

# Check useCasesSection
print("useCasesSection in text:", 'id="useCasesSection"' in text or 'id="use-cases"' in text)
sec_match = re.findall(r'<section[^>]*id="[^"]*"[^>]*>', text)
for s in sec_match:
    print("SECTION:", s)
