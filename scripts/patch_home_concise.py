import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

gen_file = r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py'
with open(gen_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add bounce animation to CSS
bounce_css = """
    /* Interactive Tour Button Bounce Animation */
    @keyframes tourBounce {
      0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-6px); }
      60% { transform: translateY(-3px); }
    }
    .tour-bounce-btn {
      animation: tourBounce 2.2s infinite cubic-bezier(0.28, 0.84, 0.42, 1) !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
"""

if 'keyframes tourBounce' not in text:
    text = re.sub(r'(\.album-btn\s*\{[^}]*\})', r'\1' + bounce_css, text)

# 2. Add tour-bounce-btn to navTourBtn & heroTourBtn
text = re.sub(r'id="navTourBtn"', r'id="navTourBtn" class="tour-bounce-btn"', text)
text = re.sub(r'id="heroTourBtn" class="([^"]*)"', r'id="heroTourBtn" class="\1 tour-bounce-btn"', text)

# 3. Shorten tourSteps
old_steps_pattern = r'const tourSteps = \[[\s\S]*?\];\s*let currentHomeStep'
new_steps = """const tourSteps = [
      {
        title: '1. Portable Memory',
        body: 'Remembers your personal friction, stamina, and past progress across sessions.'
      },
      {
        title: '2. AI Roadmap',
        body: 'Dreams intermediate milestones between where you are and where you want to be.'
      },
      {
        title: '3. Dynamic A* Route',
        body: 'Calculates the lowest-friction path and reroutes around blockers in real time.'
      },
      {
        title: '4. Verifiable Sui Proof',
        body: 'Stamps finished milestones on Sui Mainnet with immutable cryptographic proof.'
      }
    ];

    let currentHomeStep"""

m = re.search(old_steps_pattern, text)
if m:
    text = text[:m.start()] + new_steps + text[m.end():]
    print("SUCCESS: Updated tourSteps in generate_final_home.py!")

with open(gen_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("generate_final_home.py updated!")
