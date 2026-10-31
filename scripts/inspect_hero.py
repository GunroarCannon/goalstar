import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<section class="hero-sec">')
end_idx = text.find('<!-- Live Route Simulator')
print('=== HERO HTML ===')
print(text[idx:end_idx])
