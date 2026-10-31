import re

home_path = r'C:\Users\hmmm\goalstar-recall\home.html'

with open(home_path, 'r', encoding='utf-8') as f:
    content = f.read()

bg_humaaans_html = '''
  <!-- Background Parallax Humaaans Layer (Animated on Scroll) -->
  <div class="bg-humaaans-layer" id="bgHumaaansLayer" aria-hidden="true">
    <div class="bg-humaaan-item" id="bgHumaaan1" style="top: 140px; right: 2%;">
      <img src="assets/humaaans/webp/hu_sit_8.webp" alt="" class="bg-humaaan-img" />
    </div>
    <div class="bg-humaaan-item" id="bgHumaaan2" style="top: 900px; left: 1%;">
      <img src="assets/humaaans/webp/hu_stand_10.webp" alt="" class="bg-humaaan-img" />
    </div>
    <div class="bg-humaaan-item" id="bgHumaaan3" style="top: 1700px; right: 1%;">
      <img src="assets/humaaans/webp/hu_sit_3.webp" alt="" class="bg-humaaan-img" />
    </div>
    <div class="bg-humaaan-item" id="bgHumaaan4" style="top: 2500px; left: 2%;">
      <img src="assets/humaaans/webp/hu_stand_4.webp" alt="" class="bg-humaaan-img" />
    </div>
    <div class="bg-humaaan-item" id="bgHumaaan5" style="top: 3200px; right: 2%;">
      <img src="assets/humaaans/webp/hu_stand_14.webp" alt="" class="bg-humaaan-img" />
    </div>
  </div>
'''

if 'bg-humaaans-layer' not in content:
    content = re.sub(r'(<body[^>]*>)', r'\1' + bg_humaaans_html, content)

with open(home_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('[OK] Injected bg-humaaans-layer directly into home.html body!')
