import sys

with open(r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the progress calculation in Section 6
old_sec6 = """          const startOffset = winH * 0.5;
          const endBtn = document.getElementById('card5LaunchBtn') || document.getElementById('card5');
          const er = endBtn ? endBtn.getBoundingClientRect() : tr;
          const totalDist = er.top + er.height / 2 - tr.top;
          const currentScroll = startOffset - tr.top;
          const progress = Math.max(0, Math.min(1, currentScroll / Math.max(1, totalDist)));"""

new_sec6 = """          const card1El = document.getElementById('card1');
          const card5El = document.getElementById('card5');
          const endBtn = document.getElementById('card5LaunchBtn') || card5El;
          const c1r = card1El ? card1El.getBoundingClientRect() : tr;
          const er = endBtn ? endBtn.getBoundingClientRect() : tr;

          // Track journey: from card 1 appearing in mid-viewport to card 5 button appearing in viewport
          const startScrollY = window.scrollY + c1r.top - winH * 0.65;
          const endScrollY = window.scrollY + er.top - winH * 0.55;
          let progress = 0;
          if (endScrollY > startScrollY) {
            progress = Math.max(0, Math.min(1, (window.scrollY - startScrollY) / (endScrollY - startScrollY)));
          }
          if (er.top <= winH * 0.7) {
            // Once the button is comfortably on screen, guarantee it snaps to 100%
            const snapProgress = Math.min(1, Math.max(0, 1 - (er.top - winH * 0.45) / (winH * 0.25)));
            progress = Math.max(progress, snapProgress);
          }
          if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 60) {
            progress = 1.0;
          }"""

assert old_sec6 in code, "old_sec6 target string not found in generate_final_home.py!"
code = code.replace(old_sec6, new_sec6)

with open(r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated generate_final_home.py successfully!")
