import sys, re

sys.stdout.reconfigure(encoding='utf-8')

replacements = {
    '🎉': '',
    '🔗': '',
    '🚀': '',
    '✦': '*',
    '✧': '*',
    '★': '*',
    '✓': 'Done',
    '☑': '',
    '●': '',
    '⚡': '',
}

target_files = [
    r'C:\Users\hmmm\goalstar-recall\js\app.js',
    r'C:\Users\hmmm\goalstar-recall\js\model.js',
    r'C:\Users\hmmm\goalstar-recall\js\render.js',
    r'C:\Users\hmmm\goalstar-recall\js\dreamers\offline.js',
    r'C:\Users\hmmm\goalstar-recall\server.js',
]

for fpath in target_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    # Specific targeted replacements for cleaner UI
    content = content.replace('🎉 Goal achieved!', 'Goal achieved!')
    content = content.replace('<b>✦ Dream map</b> or <b>★ Search</b>', '<b>Dream map</b> or <b>Search</b>')
    content = content.replace('★ Goal', 'Goal')
    content = content.replace('★ goal', 'Goal')
    content = content.replace('● you are here', 'You are here')
    content = content.replace('🔗 Verify Milestone on Sui', 'Verify Milestone on Sui')
    content = content.replace('✓ All steps done — mark reached', 'All steps done — mark reached')
    content = content.replace('✓ I did this', 'I did this')
    content = content.replace('✓ 10 Stored', '10 Stored')
    content = content.replace('<b>✓ Verified on Sui Mainnet</b>', '<b>Verified on Sui Mainnet</b>')
    content = content.replace('Synced ✓', 'Synced')
    content = content.replace('1–3★', '1-3 star')
    content = content.replace('🚀 GoalStar Total Recall Edition running at:', 'GoalStar Total Recall Edition running at:')
    content = content.replace('✓ Walrus Memory connected', '[OK] Walrus Memory connected')
    content = content.replace('★ Search', 'Search')
    content = content.replace('✦ Add detail', 'Add detail')
    content = content.replace('★ Path found:', 'Path found:')
    content = content.replace('★ bridging', '[Search] bridging')
    content = content.replace('★ expanding', '[Search] expanding')
    content = content.replace('toast(n.kind === \'goal\' ? \'🎉 Goal achieved!\' : `✓ ${n.label}`);', 'toast(n.kind === \'goal\' ? \'Goal achieved!\' : `Done: ${n.label}`);')
    
    # Generic loop for any remnants
    for char, rep in replacements.items():
        content = content.replace(char, rep)
        
    if content != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Sanitized: {fpath}')
    else:
        print(f'No change: {fpath}')

# Final scan across these files
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf]')
total = 0
for fpath in target_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        matches = emoji_pattern.findall(f.read())
        total += len(matches)
        if matches:
            print(f'Remaining in {fpath}: {matches}')
print(f'Total remaining emojis in target JS files: {total}')
