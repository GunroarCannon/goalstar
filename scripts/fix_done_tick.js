const fs = require('fs');

// 1. Fix js/render.js: replace 'Done' with SVG checkmark
let renderCode = fs.readFileSync('C:/Users/hmmm/goalstar-recall/js/render.js', 'utf8');
const oldTickRender = "${n.kind === 'start' ? '' : `<button class=\"tick\" title=\"${n.done ? 'Achieved — click to undo' : 'Mark as achieved'}\">${n.done ? 'Done' : ''}</button>`}";
const newTickRender = "${n.kind === 'start' ? '' : `<button class=\"tick\" aria-label=\"${n.done ? 'Achieved — click to undo' : 'Mark as achieved'}\" title=\"${n.done ? 'Achieved — click to undo' : 'Mark as achieved'}\">${n.done ? '<svg class=\"tick-svg\" viewBox=\"0 0 12 12\" width=\"10\" height=\"10\" aria-hidden=\"true\"><path d=\"M2 6.2 L4.8 9 L10 3.2\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>' : ''}</button>`}";

if (renderCode.includes(oldTickRender)) {
  renderCode = renderCode.replace(oldTickRender, newTickRender);
  fs.writeFileSync('C:/Users/hmmm/goalstar-recall/js/render.js', renderCode, 'utf8');
  console.log('Successfully updated js/render.js');
} else {
  console.error('Failed to find oldTickRender in js/render.js');
}

// 2. Fix js/app.js: replace 'Done' in .tick-sm with SVG checkmark and remove stopwatch emoji
let appCode = fs.readFileSync('C:/Users/hmmm/goalstar-recall/js/app.js', 'utf8');
appCode = appCode.replace(
  '<button class=\"tick-sm\" data-done=\"${e.to}\" title=\"I did this\">Done</button>',
  '<button class=\"tick-sm\" data-done=\"${e.to}\" title=\"I did this\" aria-label=\"I did this\"><svg viewBox=\"0 0 12 12\" width=\"10\" height=\"10\" aria-hidden=\"true\"><path d=\"M2 6.2 L4.8 9 L10 3.2\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg></button>'
);
appCode = appCode.replaceAll('⏱ ', '');
fs.writeFileSync('C:/Users/hmmm/goalstar-recall/js/app.js', appCode, 'utf8');
console.log('Successfully updated js/app.js');

// 3. Fix css/style.css: ensure .tick and .tick-sm have crisp alignment and zero overflow
let cssCode = fs.readFileSync('C:/Users/hmmm/goalstar-recall/css/style.css', 'utf8');
const oldTickCss = `.tick {
  position: absolute; left: 9px; top: 11px;
  width: 18px; height: 18px; padding: 0;
  border: 1.5px solid var(--ink-soft); border-radius: 50%;
  background: var(--card); color: var(--green);
  font: 700 11px/1 var(--ui);
}
.tick:hover { background: var(--card-done); border-color: var(--green); }
.done .tick { background: var(--green); border-color: var(--green); color: #fff; animation: tickpop 0.35s cubic-bezier(0.2, 1.8, 0.4, 1); }`;

const newTickCss = `.tick {
  position: absolute; left: 9px; top: 11px;
  width: 18px; height: 18px; padding: 0;
  border: 1.5px solid var(--ink-soft); border-radius: 50%;
  background: var(--card); color: var(--green);
  display: inline-flex; align-items: center; justify-content: center;
  box-sizing: border-box; overflow: hidden;
  cursor: pointer;
}
.tick svg, .tick-svg {
  display: block; width: 10px; height: 10px;
  stroke: #ffffff; pointer-events: none;
}
.tick:hover { background: var(--card-done); border-color: var(--green); }
.done .tick { background: var(--green); border-color: var(--green); color: #fff; animation: tickpop 0.35s cubic-bezier(0.2, 1.8, 0.4, 1); }

.tick-sm {
  flex-shrink: 0; width: 22px; height: 22px; padding: 0; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--panel-2); border: 1.5px solid var(--border);
  color: var(--green); cursor: pointer;
}
.tick-sm svg { stroke: currentColor; pointer-events: none; }
.tick-sm:hover:not(:disabled) { background: var(--green); color: #fff; border-color: var(--green); }
.tick-sm:hover:not(:disabled) svg { stroke: #fff; }`;

if (cssCode.includes(oldTickCss)) {
  cssCode = cssCode.replace(oldTickCss, newTickCss);
  fs.writeFileSync('C:/Users/hmmm/goalstar-recall/css/style.css', cssCode, 'utf8');
  console.log('Successfully updated css/style.css');
} else {
  console.error('Failed to find oldTickCss in css/style.css');
}
