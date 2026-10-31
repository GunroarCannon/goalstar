import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\home.html', 'r', encoding='utf-8') as f:
    text = f.read()

count = text.count('openFullPlannerBtn')
print(f"openFullPlannerBtn appears {count} times")
idx = 0
for i in range(count):
    idx = text.find('openFullPlannerBtn', idx)
    print(f"Occurrence {i}: pos={idx}")
    print(text[max(0, idx-50):min(len(text), idx+150)])
    idx += 1
