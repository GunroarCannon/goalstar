index_path = r'C:\Users\hmmm\goalstar-recall\js\app.js'

with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add imports at the top
old_import = "import * as gist from './sync.js';"
new_import = """import * as gist from './sync.js';
import { sound } from './sound.js';
import { theme } from './theme.js';
import { auth } from './auth.js';"""

if old_import in code and 'import { sound }' not in code:
    code = code.replace(old_import, new_import, 1)

# 2. Expose window.toast
old_toast = """function toast(msg, kind = '') {
  const t = $('#toast');"""
new_toast = """function toast(msg, kind = '') {
  window.toast = toast;
  const t = $('#toast');"""

if old_toast in code and 'window.toast = toast;' not in code:
    code = code.replace(old_toast, new_toast, 1)

# 3. Add theme.init(), sound.attachListeners(), auth.init() at boot
old_boot = "applyDisplay();"
new_boot = """theme.init();
sound.attachListeners();
auth.init();
window.toast = toast;
applyDisplay();"""

if old_boot in code and 'theme.init();' not in code:
    code = code.replace(old_boot, new_boot, 1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated js/app.js successfully')
