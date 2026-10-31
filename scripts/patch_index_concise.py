import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add tour-bounce-btn to tourBtn
text = re.sub(r'id="tourBtn" class="([^"]*)"', r'id="tourBtn" class="\1 tour-bounce-btn"', text)

# 2. Add tour-bounce-btn to launchTourFromGuideBtn
text = re.sub(r'id="launchTourFromGuideBtn" class="([^"]*)"', r'id="launchTourFromGuideBtn" class="\1 tour-bounce-btn"', text)

# 3. Shorten text in uiGuideDlg
old_guide_body_pattern = r'<div style="padding: 20px 24px; max-height: 70vh; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; font-size: 13.5px; line-height: 1.5;">[\s\S]*?</div>\s*</div>\s*<div style="padding: 14px 24px;'

new_guide_body = """<div style="padding: 18px 24px; max-height: 70vh; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; font-size: 13.5px; line-height: 1.4;">
      
      <div style="padding: 9px 12px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">1. Goal Selector:</b>
        <span style="color:var(--ink-soft); margin-left:6px;">Select active goals, track progress percent, and see days remaining.</span>
      </div>

      <div style="padding: 9px 12px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">2. 4-Bar Friction Profile:</b>
        <span style="color:var(--ink-soft); margin-left:6px;">Balances cognitive and physical friction across Time, Money, Effort, and Risk.</span>
      </div>

      <div style="padding: 9px 12px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">3. Best Path Checklist:</b>
        <span style="color:var(--ink-soft); margin-left:6px;">The lowest-resistance sequence of actions to reach your destination.</span>
      </div>

      <div style="padding: 9px 12px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">4. Dream &amp; Search:</b>
        <span style="color:var(--ink-soft); margin-left:6px;">AI brainstorms intermediate milestones, and A* computes the optimal route.</span>
      </div>

      <div style="padding: 9px 12px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">5. Interactive Canvas:</b>
        <span style="color:var(--ink-soft); margin-left:6px;">Drag to organize nodes, click to inspect, or pan and zoom the live graph.</span>
      </div>

      <div style="padding: 9px 12px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">6. State Inspector:</b>
        <span style="color:var(--ink-soft); margin-left:6px;">Review checklists, take notes, and dream outward actions from this milestone.</span>
      </div>

      <div style="padding: 9px 12px; background: var(--field); border: 1px solid var(--border); border-radius: 8px;">
        <b style="color:var(--accent);">7. Sui &amp; Walrus Proof:</b>
        <span style="color:var(--ink-soft); margin-left:6px;">Syncs memory blobs to Walrus and stamps milestone verification on Sui.</span>
      </div>

    </div>
    <div style="padding: 14px 24px;"""

m = re.search(old_guide_body_pattern, text)
if m:
    text = text[:m.start()] + new_guide_body + text[m.end():]
    print("SUCCESS: Shortened uiGuideDlg text!")
else:
    print("Warning: old_guide_body_pattern not matched directly")

with open(r'C:\Users\hmmm\goalstar-recall\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated index.html!")
