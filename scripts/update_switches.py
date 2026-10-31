theme_path = r'C:\Users\hmmm\goalstar-recall\js\theme.js'
with open(theme_path, 'r', encoding='utf-8') as f:
    t = f.read()

switch_code = """
    const sw = document.getElementById('themeSwitch');
    if (sw) {
      sw.classList.toggle('active', isDark);
    }
"""

if 'themeSwitch' not in t:
    t = t.replace("document.body.dataset.paper = isDark ? 'night' : 'lined';", "document.body.dataset.paper = isDark ? 'night' : 'lined';" + switch_code)
    t = t.replace("btns.forEach(btn => {", "document.querySelectorAll('#themeSwitch, .theme-switch').forEach(sw => sw.addEventListener('click', (e) => { e.stopPropagation(); this.toggle(); }));\n    btns.forEach(btn => {")
    with open(theme_path, 'w', encoding='utf-8') as f:
        f.write(t)
    print('Updated theme.js for engraved switch')
else:
    print('theme.js already updated')

sound_path = r'C:\Users\hmmm\goalstar-recall\js\sound.js'
with open(sound_path, 'r', encoding='utf-8') as f:
    s = f.read()

sound_switch_code = """
    const sw = document.getElementById('soundSwitch');
    if (sw) {
      sw.classList.toggle('active', this.enabled);
    }
"""

if 'soundSwitch' not in s:
    s = s.replace("this.updateUI();\n    return this.enabled;", "this.updateUI();" + sound_switch_code + "\n    return this.enabled;")
    s = s.replace("btns.forEach(btn => {", "document.querySelectorAll('#soundSwitch, .sound-switch').forEach(sw => sw.addEventListener('click', (ev) => { ev.stopPropagation(); this.toggle(); }));\n    btns.forEach(btn => {")
    with open(sound_path, 'w', encoding='utf-8') as f:
        f.write(s)
    print('Updated sound.js for engraved switch')
else:
    print('sound.js already updated')
