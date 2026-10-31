import re

style_path = r'C:\Users\hmmm\goalstar-recall\css\style.css'

with open(style_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .engraved-btn 3D styling with flat photo-album paper tag styling
old_btn_css = r'/\* Tactile Engraved Buttons \(Reference Image 3\) \*/[\s\S]*?body\[data-paper=\'night\'\] \.engraved-btn\.primary[\s\S]*?\}'

new_btn_css = '''/* Photo Album Paper Tag Buttons (Flat & Tactile, No 3D bevels) */
.engraved-btn, .launch-btn, .login-btn, .tour-nav-btn, .album-btn {
  background: #fffdf9 !important;
  color: #1a1b1e !important;
  border: 1.5px solid var(--ink) !important;
  border-radius: 4px !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04) !important;
  text-shadow: none !important;
  font-family: 'Space Grotesk', 'Patrick Hand', var(--ui) !important;
  font-weight: 700 !important;
  letter-spacing: 0.3px;
  cursor: pointer;
  padding: 7px 16px;
  transition: all 0.16s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}
.engraved-btn:hover, .launch-btn:hover, .login-btn:hover, .tour-nav-btn:hover, .album-btn:hover {
  transform: translateY(-2px) rotate(-0.5deg);
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.06) !important;
  background: #ffffff !important;
}
.engraved-btn:active, .launch-btn:active, .login-btn:active, .tour-nav-btn:active, .album-btn:active {
  transform: translateY(1px) rotate(0deg) !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

/* Primary Washi Tape Button */
.engraved-btn.primary, .album-btn.primary-tape, #heroLaunchBtn {
  background: #f59e0b !important;
  color: #111827 !important;
  border-color: #111827 !important;
}
.engraved-btn.primary:hover, .album-btn.primary-tape:hover, #heroLaunchBtn:hover {
  background: #fbbf24 !important;
  box-shadow: 0 6px 14px rgba(245, 158, 11, 0.28) !important;
}

/* Gold Tape Button */
.engraved-btn.gold {
  background: #fef3c7 !important;
  color: #92400e !important;
  border-color: #b45309 !important;
}
.engraved-btn.gold:hover {
  background: #fde68a !important;
}

/* Dark Mode Album Paper Tag Buttons */
body[data-paper='night'] .engraved-btn,
body[data-paper='night'] .launch-btn,
body[data-paper='night'] .login-btn,
body[data-paper='night'] .tour-nav-btn,
body[data-paper='night'] .album-btn,
.dark-mode .engraved-btn,
.dark-mode .launch-btn,
.dark-mode .login-btn,
.dark-mode .tour-nav-btn,
.dark-mode .album-btn {
  background: #1e293b !important;
  color: #f8fafc !important;
  border-color: rgba(245, 158, 11, 0.4) !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4) !important;
}
body[data-paper='night'] .engraved-btn:hover,
body[data-paper='night'] .album-btn:hover,
.dark-mode .engraved-btn:hover,
.dark-mode .album-btn:hover {
  border-color: #f59e0b !important;
  box-shadow: 0 5px 14px rgba(245, 158, 11, 0.2) !important;
}
body[data-paper='night'] .engraved-btn.primary,
body[data-paper='night'] .album-btn.primary-tape,
.dark-mode .engraved-btn.primary,
.dark-mode .album-btn.primary-tape {
  background: #d97706 !important;
  color: #ffffff !important;
  border-color: #f59e0b !important;
}'''

css = re.sub(old_btn_css, new_btn_css, css)

with open(style_path, 'w', encoding='utf-8') as f:
    f.write(css)

print('[OK] Updated style.css with flat photo album button styles!')
