import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

scripts = re.findall(r'<script[\s\S]*?</script>', text)
print(f"Total script blocks in home.html: {len(scripts)}")
for idx, s in enumerate(scripts):
    first_line = s.splitlines()[0]
    last_line = s.splitlines()[-1]
    print(f"Script {idx}: len={len(s)}, start={first_line}, end={last_line}")
