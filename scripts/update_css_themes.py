import sys, re

# =========================================================
# 1. UPDATE CSS/STYLE.CSS WITH 4 THEMES & HARMONIZED STYLES
# =========================================================
with open(r'C:\Users\hmmm\goalstar-recall\css\style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Replace root and night variables with 4 cohesive palettes
old_root_block = """:root {
  --paper: #fbf7ea;
  --line: #c9dbef;
  --margin: #e9a9a9;
  --ink: #2a2d3e;
  --ink-soft: #3d4260;
  --muted: #6d7184;
  --gold: #f2b705;
  --gold-ink: #a87500;
  --hl: rgba(255, 210, 0, 0.42);
  --panel: #fffdf6;
  --panel-2: #f6f0de;
  --field: #fff;
  --border: #e4dcc6;
  --accent: #3557c5;
  --green: #2f9e6a;
  --red: #c4483e;
  --card: #fff;
  --card-start: #e6f5eb;
  --card-goal: #fff3c4;
  --card-done: #eef8f0;
  --label-bg: rgba(251, 247, 234, 0.95);
  --shadow: rgba(42, 45, 62, 0.14);
  --mini-ink: #b9b3a0;
  --mini-card: #8d93a8;
  --done-mini: #9fd3b6;
  --c-time: #4c7bd9;
  --c-money: #2f9e6a;
  --c-effort: #e08a2e;
  --c-risk: #c4483e;
  --tl-0: #dbe5f6;
  --tl-1: #c2d3ef;
  --hand: 'Patrick Hand', 'Segoe Print', 'Comic Sans MS', cursive;
  --title: 'Caveat', 'Segoe Script', cursive;
  --ui: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  color-scheme: light;
}

body[data-paper='night'] {
  --paper: #1b2232;
  --line: rgba(140, 170, 220, 0.14);
  --margin: rgba(233, 120, 120, 0.4);
  --ink: #e9edf6;
  --ink-soft: #c5cde0;
  --muted: #9ba4ba;
  --gold-ink: #f2c84b;
  --hl: rgba(255, 200, 0, 0.25);
  --panel: #151b27;
  --panel-2: #1f2737;
  --field: #1d2535;
  --border: #2d384d;
  --accent: #7d9cff;
  --card: #232c3e;
  --card-start: #1d3a2d;
  --card-goal: #3b3216;
  --card-done: #1d3328;
  --label-bg: rgba(27, 34, 50, 0.95);
  --shadow: rgba(0, 0, 0, 0.35);
  --mini-ink: #46516a;
  --mini-card: #59657f;
  --done-mini: #2f6b4d;
  --tl-0: #2a3753;
  --tl-1: #344466;
  color-scheme: dark;
}"""

new_root_block = """:root {
  /* THEME 1: NOTEBOOK (Warm Ivory Paper - Default) */
  --paper: #faf7f0;
  --line: rgba(42, 45, 62, 0.08);
  --margin: rgba(217, 119, 6, 0.25);
  --ink: #1c1917;
  --ink-soft: #44403c;
  --muted: #78716c;
  --gold: #d97706;
  --gold-ink: #b45309;
  --hl: rgba(217, 119, 6, 0.18);
  --panel: #fffdf8;
  --panel-2: #f5efe1;
  --field: #ffffff;
  --border: #e6dfcf;
  --accent: #059669;
  --accent-hover: #047857;
  --green: #059669;
  --red: #dc2626;
  --card: #ffffff;
  --card-start: #e8f5e9;
  --card-goal: #fef3c7;
  --card-done: #e6f4ea;
  --label-bg: rgba(250, 247, 240, 0.95);
  --shadow: rgba(28, 25, 23, 0.10);
  --mini-ink: #a8a29e;
  --mini-card: #78716c;
  --done-mini: #a7f3d0;
  --c-time: #0284c7;
  --c-money: #059669;
  --c-effort: #d97706;
  --c-risk: #dc2626;
  --tl-0: #e0f2fe;
  --tl-1: #bae6fd;
  --hand: 'Patrick Hand', 'Segoe Print', cursive;
  --title: 'Caveat', cursive;
  --ui: 'Space Grotesk', system-ui, sans-serif;
  color-scheme: light;
}

/* THEME 2: CHALKBOARD NIGHT (Midnight Slate) */
body[data-paper='night'] {
  --paper: #0f172a;
  --line: rgba(255, 255, 255, 0.07);
  --margin: rgba(245, 158, 11, 0.25);
  --ink: #f8fafc;
  --ink-soft: #cbd5e1;
  --muted: #94a3b8;
  --gold: #f59e0b;
  --gold-ink: #fbbf24;
  --hl: rgba(245, 158, 11, 0.25);
  --panel: #0b0f19;
  --panel-2: #182234;
  --field: #1e293b;
  --border: rgba(245, 158, 11, 0.22);
  --accent: #10b981;
  --accent-hover: #059669;
  --green: #10b981;
  --red: #f87171;
  --card: #182234;
  --card-start: #064e3b;
  --card-goal: #78350f;
  --card-done: #065f46;
  --label-bg: rgba(15, 23, 42, 0.95);
  --shadow: rgba(0, 0, 0, 0.45);
  --mini-ink: #64748b;
  --mini-card: #94a3b8;
  --done-mini: #059669;
  --c-time: #38bdf8;
  --c-money: #10b981;
  --c-effort: #fbbf24;
  --c-risk: #f87171;
  --tl-0: #1e293b;
  --tl-1: #334155;
  color-scheme: dark;
}

/* THEME 3: BLUEPRINT TECHNICAL (Engineering Drafting Grid) */
body[data-paper='blueprint'], body[data-paper='grid'] {
  --paper: #0a192f;
  --line: rgba(100, 255, 218, 0.12);
  --margin: rgba(100, 255, 218, 0.35);
  --ink: #e6f1ff;
  --ink-soft: #ccd6f6;
  --muted: #8892b0;
  --gold: #ffd166;
  --gold-ink: #ffe082;
  --hl: rgba(100, 255, 218, 0.22);
  --panel: #06101e;
  --panel-2: #112240;
  --field: #172a45;
  --border: rgba(100, 255, 218, 0.26);
  --accent: #64ffda;
  --accent-hover: #52e3c2;
  --green: #64ffda;
  --red: #ff5c77;
  --card: #112240;
  --card-start: #0a3a40;
  --card-goal: #3d3714;
  --card-done: #0a3d36;
  --label-bg: rgba(10, 25, 47, 0.95);
  --shadow: rgba(2, 12, 27, 0.55);
  --mini-ink: #495670;
  --mini-card: #8892b0;
  --done-mini: #64ffda;
  --c-time: #48cae4;
  --c-money: #64ffda;
  --c-effort: #ffd166;
  --c-risk: #ff5c77;
  --tl-0: #172a45;
  --tl-1: #233554;
  color-scheme: dark;
}

/* THEME 4: MONOGRAPH (Vintage Antique Sepia) */
body[data-paper='monograph'], body[data-paper='dots'] {
  --paper: #f4eee0;
  --line: rgba(87, 83, 78, 0.12);
  --margin: rgba(194, 65, 12, 0.25);
  --ink: #292524;
  --ink-soft: #44403c;
  --muted: #78716c;
  --gold: #c2410c;
  --gold-ink: #9a3412;
  --hl: rgba(194, 65, 12, 0.18);
  --panel: #eae1cf;
  --panel-2: #ded3bd;
  --field: #fdfbf7;
  --border: rgba(87, 83, 78, 0.24);
  --accent: #2d6a4f;
  --accent-hover: #1b4332;
  --green: #2d6a4f;
  --red: #991b1b;
  --card: #fdfbf7;
  --card-start: #e2ece9;
  --card-goal: #faede8;
  --card-done: #d8eae3;
  --label-bg: rgba(244, 238, 224, 0.95);
  --shadow: rgba(41, 37, 36, 0.12);
  --mini-ink: #a8a29e;
  --mini-card: #78716c;
  --done-mini: #95d5b2;
  --c-time: #407ba7;
  --c-money: #2d6a4f;
  --c-effort: #c2410c;
  --c-risk: #991b1b;
  --tl-0: #e7dfcb;
  --tl-1: #dad0ba;
  color-scheme: light;
}"""

assert old_root_block in css_content, "old_root_block not found in css/style.css"
css_content = css_content.replace(old_root_block, new_root_block)

# Harmonize sui-stamp-btn
old_sui_btn = """.sui-stamp-btn {
  display: block;
  width: 100%;
  margin-top: 10px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
}
.sui-stamp-btn:hover {
  background: #2563eb;
}"""

new_sui_btn = """.sui-stamp-btn {
  display: block;
  width: 100%;
  margin-top: 10px;
  background: var(--accent);
  color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  text-align: center;
  box-shadow: 0 2px 4px var(--shadow);
  transition: all 0.2s ease;
}
.sui-stamp-btn:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
}"""

css_content = css_content.replace(old_sui_btn, new_sui_btn)

# Harmonize tuesday-banner
old_tuesday = """.tuesday-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fffbeb;
  border: 2px solid var(--ink);
  border-radius: 255px 8px 225px 8px/8px 225px 8px 255px;
  padding: 6px 12px;
  margin: 6px 12px 2px 12px;
  box-shadow: 2.5px 2.5px 0 var(--ink);
  font-family: inherit;
  z-index: 10;
  position: relative;
}"""

new_tuesday = """.tuesday-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--panel-2);
  border: 1.5px solid var(--border);
  border-radius: 8px;
  padding: 8px 14px;
  margin: 8px 12px 4px 12px;
  box-shadow: 0 2px 6px var(--shadow);
  font-family: inherit;
  z-index: 10;
  position: relative;
  color: var(--ink);
}"""

css_content = css_content.replace(old_tuesday, new_tuesday)

# Add theme-select and guide-btn styling
additional_nav_styles = """
/* Theme Select Dropdown & UI Guide Button */
.theme-select.engraved-select {
  background: var(--field);
  border: 1.5px solid var(--border);
  color: var(--ink);
  font-weight: 600;
  font-size: 12px;
  padding: 5px 8px;
  border-radius: 6px;
  cursor: pointer;
  max-width: 140px;
  height: 32px;
}
.guide-btn {
  background: var(--field);
  border: 1.5px solid var(--border);
  color: var(--ink);
  font-weight: 700;
  font-size: 12px;
  padding: 5px 10px;
  border-radius: 6px;
  cursor: pointer;
  height: 32px;
}
.guide-btn:hover {
  background: var(--panel-2);
  border-color: var(--accent);
}
"""

if '.theme-select.engraved-select' not in css_content:
    css_content += additional_nav_styles

with open(r'C:\Users\hmmm\goalstar-recall\css\style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Updated css/style.css with 4 themes & harmonious component tokens!")
