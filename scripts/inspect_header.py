with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1018, 1075):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
