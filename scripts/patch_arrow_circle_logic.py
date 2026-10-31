import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

gen_path = r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py'
with open(gen_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the progress calculation and arrow animation block
old_arrow_section_pattern = r'const endBtn = document\.getElementById\(\'card5LaunchBtn\'\)[\s\S]*?if \(targetRing\) \{\s*targetRing\.style\.opacity = progress >= 0\.96 \? \'1\' : \'0\';\s*\}'

new_arrow_section = """const endBtn = document.getElementById('card5LaunchBtn') || card5El;
          const terminalTarget = document.getElementById('terminalCircleTarget');
          const c1r = card1El ? card1El.getBoundingClientRect() : tr;
          const er = endBtn ? endBtn.getBoundingClientRect() : tr;
          const ter = terminalTarget ? terminalTarget.getBoundingClientRect() : er;

          // Track journey: from Card 1 all the way down to centered terminal
          const startScrollY = window.scrollY + c1r.top - winH * 0.65;
          const endScrollY = window.scrollY + ter.top - winH * 0.65;
          let progress = 0;
          if (endScrollY > startScrollY) {
            progress = Math.max(0, Math.min(1, (window.scrollY - startScrollY) / (endScrollY - startScrollY)));
          }
          if (ter.top <= winH * 0.8) {
            // Once the terminal target is comfortably on screen, guarantee it snaps to 100%
            const snapProgress = Math.min(1, Math.max(0, 1 - (ter.top - winH * 0.55) / (winH * 0.25)));
            progress = Math.max(progress, snapProgress);
          }
          if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 50) {
            progress = 1.0;
          }

          const currentLen = progress * pathLen;
          if (activePath) {
            activePath.style.strokeDasharray = `${currentLen} ${pathLen}`;
            activePath.style.strokeDashoffset = '0';
          }

          const pt = svgPath.getPointAtLength(currentLen);
          travelingArrow.style.left = `${pt.x}px`;
          travelingArrow.style.top = `${pt.y}px`;

          // TURN INTO A CIRCLE IN THE MIDDLE X POSITION AT THE BOTTOM
          if (progress >= 0.92) {
            travelingArrow.classList.add('is-circle');
            travelingArrow.style.transform = `translate(-50%, -50%) scale(1.18)`;
            if (terminalTarget) terminalTarget.classList.add('arrived');
          } else {
            travelingArrow.classList.remove('is-circle');
            if (terminalTarget) terminalTarget.classList.remove('arrived');
            const pBefore = svgPath.getPointAtLength(Math.max(0, currentLen - 2));
            const pAfter = svgPath.getPointAtLength(Math.min(pathLen, currentLen + 2));
            const angle = Math.atan2(pAfter.y - pBefore.y, pAfter.x - pBefore.x) * (180 / Math.PI);
            travelingArrow.style.transform = `translate(-50%, -50%) rotate(${angle + 90}deg)`;
          }

          // Highlight target arrival ring at Card 5
          const targetRing = document.getElementById('card5TargetRing');
          if (targetRing) {
            targetRing.style.opacity = progress >= 0.82 ? '1' : '0';
          }"""

m = re.search(old_arrow_section_pattern, text)
if m:
    print("Found old arrow section! Replacing...")
    text = text[:m.start()] + new_arrow_section + text[m.end():]
    with open(gen_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched generate_final_home.py!")
else:
    print("ERROR: old_arrow_section_pattern not found!")
    sys.exit(1)
