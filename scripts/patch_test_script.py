import sys

with open(r'C:\Users\hmmm\goalstar-recall\scripts\test_final_experience.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_scroll = "page.evaluate(\"() => { const el = document.getElementById('card5'); el.scrollIntoView({behavior: 'smooth'}); }\")"
new_scroll = "page.evaluate(\"() => { const el = document.getElementById('card5LaunchBtn'); el.scrollIntoView({behavior: 'smooth', block: 'center'}); }\")"

assert old_scroll in code, "old_scroll not found!"
code = code.replace(old_scroll, new_scroll)

with open(r'C:\Users\hmmm\goalstar-recall\scripts\test_final_experience.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated test_final_experience.py successfully!")
