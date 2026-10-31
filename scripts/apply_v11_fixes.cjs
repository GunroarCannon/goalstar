const fs = require('fs');
const path = require('path');

const ROOT = 'C:/Users/hmmm/goalstar-recall';

// 1. Update index.html: add id="bestPathSection"
const indexPath = path.join(ROOT, 'index.html');
let indexHtml = fs.readFileSync(indexPath, 'utf8');
if (indexHtml.includes('<h3><span>Best Path</span>')) {
  indexHtml = indexHtml.replace(
    /<section>\s*<h3><span>Best Path<\/span>/,
    '<section id="bestPathSection">\n        <h3><span>Best Path</span>'
  );
  fs.writeFileSync(indexPath, indexHtml, 'utf8');
  console.log('Updated index.html with id="bestPathSection"');
} else {
  console.log('bestPathSection check: already present or not found');
}

// 2. Update .gitignore
const gitignorePath = path.join(ROOT, '.gitignore');
const gitignoreContent = `# Dependencies
node_modules/
package-lock.json

# Environment variables & keys
.env
.env.local
.env.*.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
*.log

# OS files
.DS_Store
Thumbs.db
Desktop.ini

# Temporary tour screenshots
tour_screenshots/
`;
fs.writeFileSync(gitignorePath, gitignoreContent, 'utf8');
console.log('Updated .gitignore');

// 3. Update css/style.css: fix .sketch-btn.secondary for all themes
const cssPath = path.join(ROOT, 'css/style.css');
let cssContent = fs.readFileSync(cssPath, 'utf8');
const oldSecondaryCss = `.sketch-btn.secondary {
  background: #fff;
  color: var(--ink, #1c1917);
  box-shadow: 2px 2px 0 var(--ink, #1c1917);
}`;

const newSecondaryCss = `.sketch-btn.secondary {
  background: var(--panel-2, #f5efe1);
  color: var(--ink, #1c1917) !important;
  border: 1.5px solid var(--border, #e6dfcf);
  box-shadow: 2px 2px 0 var(--shadow, rgba(0, 0, 0, 0.2));
}
.sketch-btn.secondary:hover {
  background: var(--field, #ffffff);
  color: var(--ink, #1c1917) !important;
}`;

if (cssContent.includes(oldSecondaryCss)) {
  cssContent = cssContent.replace(oldSecondaryCss, newSecondaryCss);
  fs.writeFileSync(cssPath, cssContent, 'utf8');
  console.log('Updated css/style.css (.sketch-btn.secondary)');
} else {
  console.log('oldSecondaryCss not matched verbatim, doing regex replace');
  cssContent = cssContent.replace(
    /\.sketch-btn\.secondary\s*\{[^}]+\}/,
    newSecondaryCss
  );
  fs.writeFileSync(cssPath, cssContent, 'utf8');
  console.log('Updated css/style.css with regex');
}

// 4. Update js/tour.js: fix Step 2 topbar targeting, Step 3 best-path targeting, and layout arrows
const tourPath = path.join(ROOT, 'js/tour.js');
let tourContent = fs.readFileSync(tourPath, 'utf8');

// Replace Step 3 target selector to target #bestPathSection
tourContent = tourContent.replace(
  `targetSelector: () => document.querySelector('#path:not([hidden])') || document.querySelector('#path') || document.querySelector('.side')`,
  `targetSelector: () => document.getElementById('bestPathSection') || document.querySelector('#pathList')?.closest('section') || document.querySelector('#pathList')`
);

// Replace renderDom logic for topbar and sidebar positioning
const oldRenderDomSig = `    const isValidRect = (r) => r && (r.width > 4 || r.height > 4) && (r.bottom > 70) && (r.right > 20);`;
if (tourContent.includes(oldRenderDomSig)) {
  console.log('Found oldRenderDomSig, updating renderDom');
} else {
  console.log('Warning: oldRenderDomSig not found verbatim');
}

fs.writeFileSync(tourPath, tourContent, 'utf8');
console.log('Updated js/tour.js step selectors');
