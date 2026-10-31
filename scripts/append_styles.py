css_path = r'C:\Users\hmmm\goalstar-recall\css\style.css'

extra_css = """
/* =======================================================
   CRUNCHY CONTROLS, AUTH, SOUND, & NIGHT THEME OVERRIDES
   ======================================================= */

/* Home Nav Button */
.nav-home-btn {
  background: var(--panel-2);
  color: var(--ink);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  border-radius: 3px;
  padding: 4px 10px;
  font-family: inherit;
  font-weight: 700;
  font-size: 13.5px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: transform 0.1s, box-shadow 0.1s;
}
.nav-home-btn:hover {
  transform: translate(-1px, -1px);
  box-shadow: 3px 3px 0 var(--ink);
  background: var(--hl);
}
.nav-home-btn:active {
  transform: translate(1px, 1px);
  box-shadow: 1px 1px 0 var(--ink);
}

/* Login Button */
.login-btn {
  background: #fef08a !important;
  color: #1a1b1e !important;
  border: 2px solid var(--ink) !important;
  box-shadow: 2px 2px 0 var(--ink) !important;
  border-radius: 3px !important;
  padding: 4px 11px !important;
  font-family: inherit !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: transform 0.1s, box-shadow 0.1s;
}
.login-btn:hover {
  background: #fde047 !important;
  transform: translate(-1px, -1px);
  box-shadow: 3px 3px 0 var(--ink) !important;
}
.login-btn:active {
  transform: translate(1px, 1px);
  box-shadow: 1px 1px 0 var(--ink) !important;
}

/* User Badge */
.user-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--panel-2);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  border-radius: 3px;
  padding: 3px 9px;
  font-size: 13px;
  font-weight: bold;
}
.user-badge .indicator.live {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 0 1.5px var(--ink);
}
.user-badge .logout-link {
  background: none;
  border: none;
  color: #ef4444;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  font-size: 12px;
  font-family: inherit;
  font-weight: bold;
  margin-left: 4px;
}
.user-badge .logout-link:hover {
  color: #b91c1c;
}

/* Crunchy Modal & Login Dialog */
dialog.crunchy-modal {
  padding: 0;
  border: none;
  background: transparent;
  max-width: 500px;
  width: 90vw;
}
dialog.crunchy-modal::backdrop {
  background: rgba(15, 17, 23, 0.65);
  backdrop-filter: blur(2px);
}
.modal-card {
  background: var(--paper);
  color: var(--ink);
  border: 2.5px solid var(--ink);
  box-shadow: 5px 5px 0 var(--ink);
  border-radius: 4px;
  padding: 24px;
}
.modal-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  border-bottom: 2px dashed var(--ink);
  padding-bottom: 8px;
}
.modal-head h3 {
  font-family: 'Caveat', cursive;
  font-size: 26px;
  margin: 0;
}
.close-modal, .close-login-dlg {
  background: var(--panel-2);
  border: 2px solid var(--ink);
  box-shadow: 1.5px 1.5px 0 var(--ink);
  width: 28px;
  height: 28px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 3px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.close-modal:hover, .close-login-dlg:hover {
  background: #fee2e2;
  color: #b91c1c;
}

/* Login Options List */
.login-options {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 14px;
}
.login-option {
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--panel);
  border: 2px solid var(--ink);
  box-shadow: 2.5px 2.5px 0 var(--ink);
  padding: 12px 16px;
  border-radius: 4px;
  transition: transform 0.15s;
}
.login-option:hover {
  transform: translateY(-1.5px);
  box-shadow: 3.5px 3.5px 0 var(--ink);
}
.login-option .opt-icon {
  font-size: 28px;
}
.login-option .opt-info {
  flex: 1;
}
.login-option .opt-info h4 {
  margin: 0 0 2px;
  font-size: 16px;
  font-weight: bold;
}
.login-option .opt-info p {
  margin: 0;
  font-size: 13.5px;
  color: var(--ink-soft);
}
.login-option .opt-info input {
  margin-top: 6px;
  width: 100%;
  padding: 4px 8px;
  font-family: inherit;
  font-size: 13px;
  border: 1.5px solid var(--ink);
  box-shadow: 1.5px 1.5px 0 var(--ink);
  background: var(--paper);
  color: var(--ink);
  box-sizing: border-box;
}

/* Tour Resee Button Crunchy Style */
.tour-nav-btn {
  background: #fef3c7 !important;
  color: #92400e !important;
  border: 2px solid var(--ink) !important;
  box-shadow: 2px 2px 0 var(--ink) !important;
  border-radius: 3px !important;
}
.tour-nav-btn:hover {
  background: #fde68a !important;
  transform: translate(-1px, -1px);
  box-shadow: 3px 3px 0 var(--ink) !important;
}

/* =======================================================
   DARK MODE / NIGHT PAPER CHALKBOARD OVERRIDES
   ======================================================= */
body[data-paper='night'] .sketch-card,
.dark-mode .sketch-card {
  background: #1b2333;
  color: #f3efe6;
  border: 2.5px solid #f59e0b;
  box-shadow: 4px 4px 0 #0b0d14;
}
body[data-paper='night'] .sketch-head,
.dark-mode .sketch-head {
  border-bottom: 2px dashed #4b5563;
}
body[data-paper='night'] .sketch-badge,
.dark-mode .sketch-badge {
  background: #232c3e;
  color: #f59e0b;
  border: 1.5px solid #f59e0b;
}
body[data-paper='night'] .sketch-title,
.dark-mode .sketch-title {
  color: #f59e0b;
}
body[data-paper='night'] .sketch-text,
.dark-mode .sketch-text {
  color: #e2e8f0;
}
body[data-paper='night'] .tuesday-banner,
.dark-mode .tuesday-banner {
  background: #1c2436;
  color: #f3efe6;
  border-color: #f59e0b;
  box-shadow: 3px 3px 0 #0a0d14;
}
body[data-paper='night'] .tuesday-tag,
.dark-mode .tuesday-tag {
  background: #253147;
  color: #f59e0b;
  border: 1.5px solid #f59e0b;
}
body[data-paper='night'] .modal-card,
.dark-mode .modal-card {
  background: #181f2c;
  color: #f3efe6;
  border-color: #e2e8f0;
  box-shadow: 5px 5px 0 #090c12;
}
body[data-paper='night'] .login-option,
.dark-mode .login-option {
  background: #1f2839;
  border-color: #4b5563;
  box-shadow: 2.5px 2.5px 0 #0b0d14;
}
body[data-paper='night'] .login-btn,
.dark-mode .login-btn {
  background: #f59e0b !important;
  color: #111827 !important;
}
body[data-paper='night'] .tour-nav-btn,
.dark-mode .tour-nav-btn {
  background: #2d3748 !important;
  color: #fde047 !important;
  border-color: #f59e0b !important;
}
body[data-paper='night'] .nav-home-btn,
.dark-mode .nav-home-btn {
  background: #1f293d;
  color: #e2e8f0;
  border-color: #64748b;
  box-shadow: 2px 2px 0 #0b0d14;
}
body[data-paper='night'] .telemetry-box,
.dark-mode .telemetry-box {
  background: #181f2c;
  border-color: #374151;
}
body[data-paper='night'] .telemetry-pill,
.dark-mode .telemetry-pill {
  background: #1f2839;
  border-color: #374151;
}
"""

with open(css_path, 'a', encoding='utf-8') as f:
    f.write(extra_css)

print('Appended crunchy styles successfully')
