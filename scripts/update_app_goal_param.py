import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

pattern = re.compile(
    r'(if\s*\(\s*cId\s*\)\s*\{.*?else\s+toast\([^\)]+\);\s*\})',
    re.DOTALL
)

goal_block = """

    const goalParam = params.get('goal');
    if (goalParam && !bId && !cId) {
      const b = createBoard({
        goal: goalParam,
        context: params.get('context') || 'Starting from where I am right now',
        constraints: params.get('constraints') || '',
        timeframe: params.get('timeframe') || '',
        budget: params.get('budget') || '',
        detail: settings().detail || 'normal',
        routes: settings().routes || 'some',
      });
      data.boards[b.id] = b;
      data.currentId = b.id;
      sel = null;
      persist();
      refresh();
      canvas.fit(false);
      toast(`Created plan for: "${goalParam}"`);
      setTimeout(async () => {
        try {
          const added = await dream(request('dream'), {}, 'Dreaming realistic milestones...', b.startId);
          if (added) await afterDream(b);
        } catch (err) {
          console.warn('Auto-dream failed:', err);
        }
      }, 350);
    }"""

if pattern.search(js):
    js = pattern.sub(r'\1' + goal_block, js, count=1)
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("[OK] Updated js/app.js to support URL goal parameter!")
else:
    print("[ERR] pattern not found in js/app.js")

