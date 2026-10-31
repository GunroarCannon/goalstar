css_path = r'C:\Users\hmmm\goalstar-recall\css\style.css'

engraved_css = """
/* =======================================================
   ENGRAVED / DEBOSSED BUTTONS & SWITCHES (FRONTEND-DESIGN)
   Inspired by Reference Images 0, 1, 2, 3
   ======================================================= */

/* Engraved Recessed Switches (Reference Image 0) */
.engraved-switch {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  font-family: 'Space Grotesk', system-ui, sans-serif;
  text-decoration: none;
}
.switch-track {
  position: relative;
  width: 96px;
  height: 32px;
  background: #e8e3d5;
  border-radius: 99px;
  border: 2px solid var(--ink);
  box-shadow: 
    inset 2.5px 3.5px 6px rgba(0, 0, 0, 0.28),
    inset -2px -2px 4px rgba(255, 255, 255, 0.75),
    0 1.5px 0 rgba(255, 255, 255, 0.4);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px;
  box-sizing: border-box;
  transition: all 0.2s ease;
}
body[data-paper='night'] .switch-track,
.dark-mode .switch-track {
  background: #111622;
  border-color: #f59e0b;
  box-shadow: 
    inset 3px 4px 7px rgba(0, 0, 0, 0.75),
    inset -1.5px -1.5px 3px rgba(255, 255, 255, 0.08),
    0 1px 0 rgba(255, 255, 255, 0.05);
}
.track-label {
  font-size: 9.5px;
  font-weight: 900;
  letter-spacing: 1.2px;
  color: var(--ink-soft);
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.8), 0 -1px 0 rgba(0, 0, 0, 0.25);
  pointer-events: none;
  z-index: 1;
}
body[data-paper='night'] .track-label,
.dark-mode .track-label {
  text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.9), 0 1px 0 rgba(255, 255, 255, 0.1);
  color: #94a3b8;
}
.switch-knob {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffffff 0%, #ded7c3 100%);
  border: 1.5px solid var(--ink);
  box-shadow: 
    2px 3px 5px rgba(0, 0, 0, 0.25),
    -1px -1px 2px rgba(255, 255, 255, 0.9),
    inset 0 1px 0 #ffffff;
  transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 2;
}
body[data-paper='night'] .switch-knob,
.dark-mode .switch-knob {
  background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
  border-color: #0b0d14;
  box-shadow: 
    2px 3px 6px rgba(0, 0, 0, 0.6),
    -1px -1px 2px rgba(255, 255, 255, 0.15),
    inset 0 1px 0 #fde68a;
}
.engraved-switch.active .switch-knob {
  transform: translateX(64px);
}

/* Tactile Engraved Buttons (Reference Image 3) */
.engraved-btn, .launch-btn, .login-btn, .tour-nav-btn {
  background: linear-gradient(180deg, #fdfbf7 0%, #ebe3cf 100%) !important;
  color: #1a1b1e !important;
  border: 2px solid var(--ink) !important;
  border-radius: 4px !important;
  box-shadow: 
    inset 0 1.5px 0 rgba(255, 255, 255, 0.9),
    inset 0 -2px 0 rgba(0, 0, 0, 0.15),
    0 3.5px 0 var(--ink),
    0 5px 8px rgba(0, 0, 0, 0.15) !important;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.8), 0 -1px 0 rgba(0, 0, 0, 0.15);
  font-family: 'Patrick Hand', var(--ui) !important;
  font-weight: 700 !important;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.12s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.engraved-btn:hover, .launch-btn:hover, .login-btn:hover, .tour-nav-btn:hover {
  transform: translateY(-1.5px);
  box-shadow: 
    inset 0 1.5px 0 rgba(255, 255, 255, 0.9),
    inset 0 -2px 0 rgba(0, 0, 0, 0.15),
    0 5px 0 var(--ink),
    0 8px 14px rgba(0, 0, 0, 0.2) !important;
}
.engraved-btn:active, .launch-btn:active, .login-btn:active, .tour-nav-btn:active {
  transform: translateY(3.5px) !important;
  box-shadow: 
    inset 0 2px 4px rgba(0, 0, 0, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    0 0 0 var(--ink),
    0 1px 2px rgba(0, 0, 0, 0.15) !important;
  text-shadow: 0 -1px 0 rgba(255, 255, 255, 0.3) !important;
}

/* Gold Accent on Launch Button */
.launch-btn {
  background: linear-gradient(180deg, #fef08a 0%, #f59e0b 100%) !important;
  color: #1a1b1e !important;
}
body[data-paper='night'] .engraved-btn,
body[data-paper='night'] .launch-btn,
body[data-paper='night'] .login-btn,
body[data-paper='night'] .tour-nav-btn,
.dark-mode .engraved-btn,
.dark-mode .launch-btn,
.dark-mode .login-btn,
.dark-mode .tour-nav-btn {
  background: linear-gradient(180deg, #253147 0%, #171f2e 100%) !important;
  color: #f3efe6 !important;
  border-color: #f59e0b !important;
  box-shadow: 
    inset 0 1px 0 rgba(255, 255, 255, 0.15),
    inset 0 -2px 0 rgba(0, 0, 0, 0.6),
    0 3.5px 0 #0b0d14,
    0 5px 8px rgba(0, 0, 0, 0.4) !important;
  text-shadow: 0 1px 0 #000;
}

/* Recessed Card Bay (Things Clicking into Place) */
.card-bay {
  position: relative;
  background: rgba(42, 45, 62, 0.04);
  border: 2px dashed rgba(42, 45, 62, 0.3);
  border-radius: 6px;
  box-shadow: 
    inset 3px 3px 8px rgba(0, 0, 0, 0.12),
    inset -2px -2px 6px rgba(255, 255, 255, 0.6);
  padding: 6px;
  margin-bottom: 50px;
  transition: all 0.3s ease;
}
body[data-paper='night'] .card-bay,
.dark-mode .card-bay {
  background: rgba(0, 0, 0, 0.3);
  border-color: rgba(245, 158, 11, 0.25);
  box-shadow: 
    inset 3px 3px 10px rgba(0, 0, 0, 0.7),
    inset -1px -1px 4px rgba(255, 255, 255, 0.05);
}
.card-bay.docked {
  border-style: solid;
  border-color: #10b981;
}

/* Card Docking Physics */
.uc-card {
  transform: translateY(30px) scale(0.96) rotate(-1.5deg);
  opacity: 0.55;
  transition: 
    transform 0.45s cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 0.3s ease,
    opacity 0.3s ease;
}
.uc-card.docked-in {
  transform: translateY(0) scale(1) rotate(0deg) !important;
  opacity: 1 !important;
  border-color: #10b981 !important;
  box-shadow: 5px 5px 0 var(--ink) !important;
}

/* Traveling Kinetic SVG Arrow Across Screen */
.traveling-arrow-group {
  filter: drop-shadow(2px 3px 2px rgba(0, 0, 0, 0.3));
  transition: transform 0.08s linear;
}
"""

with open(css_path, 'a', encoding='utf-8') as f:
    f.write(engraved_css)

print('Appended engraved button & switch styles successfully')
