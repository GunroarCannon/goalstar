import fs from 'node:fs';

let html = fs.readFileSync('index.html', 'utf8');

// Add Tour button before Settings button in header
const tourButtonHtml = '<button id="tourBtn" class="icon" title="Guided Walkthrough Tour" style="width: auto; padding: 4px 10px; font-weight: 700; font-family: inherit;">🎓 Tour</button>\n    ';
html = html.replace('<button id="settingsBtn"', tourButtonHtml + '<button id="settingsBtn"');

// Add tour.js module script
html = html.replace('<script type="module" src="js/app.js"></script>', '<script type="module" src="js/app.js"></script>\n  <script type="module" src="js/tour.js"></script>');

fs.writeFileSync('index.html', html, 'utf8');
console.log('✓ Successfully patched index.html with Tour button & script');
