import re

p = r"C:\Users\hmmm\goalstar-recall\css\style.css"
with open(p, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Crunchy input[type='range']
css = re.sub(
    r"input\[type='range'\]\s*\{[^}]*\}",
    """input[type='range'] {
  -webkit-appearance: none;
  appearance: none;
  height: 8px;
  background: var(--paper);
  border: 1.5px solid var(--ink);
  border-radius: 2px;
  box-shadow: 1px 1px 0 var(--ink);
  outline: none;
  padding: 0;
}
input[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 15px;
  height: 15px;
  border-radius: 2px;
  background: var(--gold);
  border: 2px solid var(--ink);
  box-shadow: 1.5px 1.5px 0 var(--ink);
  cursor: pointer;
}""",
    css
)

# 2. Crunchy .pbar and .pbar i
css = re.sub(
    r"\.pbar\s*\{[^}]*\}",
    """.pbar {
  height: 12px;
  border-radius: 2px;
  background: var(--paper);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  overflow: hidden;
  padding: 1px;
}""",
    css
)

css = re.sub(
    r"\.pbar i\s*\{[^}]*\}",
    """.pbar i {
  display: block;
  height: 100%;
  border-radius: 1px;
  background: var(--green);
  background-image: repeating-linear-gradient(
    -45deg,
    var(--green),
    var(--green) 4px,
    #15803d 4px,
    #15803d 8px
  );
  transition: width 0.6s cubic-bezier(0.2, 1.2, 0.4, 1);
}""",
    css
)

# 3. Crunchy .timeline and .timeline span
css = re.sub(
    r"\.timeline\s*\{[^}]*\}",
    """.timeline {
  display: flex;
  height: 18px;
  border-radius: 2px;
  overflow: hidden;
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  background: var(--paper);
}""",
    css
)

css = re.sub(
    r"\.timeline span\s*\{[^}]*\}",
    """.timeline span {
  min-width: 3px;
  display: grid;
  place-items: center;
  font-size: 11px;
  font-weight: 700;
  font-family: var(--hand, 'Patrick Hand', cursive);
  color: var(--ink);
  border-right: 1.5px solid var(--ink);
}""",
    css
)

# 4. Crunchy .near and .near i
css = re.sub(
    r"\.near\s*\{[^}]*\}",
    """.near {
  flex: 1;
  height: 7px;
  border-radius: 2px;
  background: var(--paper);
  border: 1.5px solid var(--ink);
  box-shadow: 1px 1px 0 var(--ink);
  overflow: hidden;
  min-width: 30px;
}""",
    css
)

css = re.sub(
    r"\.near i\s*\{[^}]*\}",
    """.near i {
  display: block;
  height: 100%;
  border-radius: 0;
  background: var(--accent);
  background-image: repeating-linear-gradient(
    -45deg,
    var(--accent),
    var(--accent) 3px,
    #1d4ed8 3px,
    #1d4ed8 6px
  );
  transition: width 0.4s;
}""",
    css
)

# 5. Crunchy .chart rect
if ".chart rect" not in css:
    css = css.replace(
        ".chart.anim rect {",
        ".chart rect { stroke: var(--ink); stroke-width: 1.5px; rx: 1px; }\n.chart.anim rect {"
    )

# 6. Crunchy .tuesday-banner
css = re.sub(
    r"\.tuesday-banner\s*\{[^}]*\}",
    """.tuesday-banner {
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
}""",
    css
)

# 7. Crunchy .mini-btn
css = re.sub(
    r"\.mini-btn\s*\{[^}]*\}",
    """.mini-btn {
  background: #f59e0b;
  color: #fff;
  border: 1.5px solid var(--ink);
  border-radius: 3px;
  padding: 4px 10px;
  font-size: 11.5px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 1.5px 1.5px 0 var(--ink);
  transition: all 0.1s ease;
}
.mini-btn:hover {
  transform: translate(-1px, -1px);
  box-shadow: 2px 2px 0 var(--ink);
}
.mini-btn:active {
  transform: translate(1px, 1px);
  box-shadow: 0.5px 0.5px 0 var(--ink);
}""",
    css
)

# 8. Crunchy .telemetry-box and .telemetry-pill
css = re.sub(
    r"\.telemetry-box\s*\{[^}]*\}",
    """.telemetry-box {
  background: var(--paper);
  border: 2px solid var(--ink);
  border-radius: 4px;
  box-shadow: 2px 2px 0 var(--ink);
  padding: 10px 12px;
  margin-top: 14px;
}""",
    css
)

css = re.sub(
    r"\.telemetry-pill\s*\{[^}]*\}",
    """.telemetry-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  background: var(--card);
  border: 1.5px solid var(--ink-soft);
  border-radius: 2px;
  box-shadow: 1px 1px 0 var(--ink-soft);
  font-size: 11.5px;
  margin-bottom: 6px;
}""",
    css
)

with open(p, "w", encoding="utf-8") as f:
    f.write(css)

print("Applied all crunchy styles successfully!")
