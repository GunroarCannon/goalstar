import fs from 'node:fs';

let html = fs.readFileSync('index.html', 'utf8');

// Replace the rogue banner + canvas with canvas-col wrapper
const oldPattern = /<div id="lastTuesdayBanner"[\s\S]*?<div id="canvas" class="canvas"><\/div>/;

const replacement = `<div class="canvas-col">
      <div id="lastTuesdayBanner" class="tuesday-banner">
        <div class="tuesday-icon">🧠</div>
        <div class="tuesday-body">
          <span class="tuesday-tag">Walrus Memory on Mainnet</span>
          <div id="tuesdayText" class="tuesday-text">Recalling past session context...</div>
          <div id="tuesdayRule" class="tuesday-sub">A* path dynamically modulated by your historical friction patterns.</div>
        </div>
        <div class="tuesday-actions">
          <button id="seedMemoriesBtn" class="mini-btn">Seed 10 Memories</button>
          <button id="addMemoryBtn" class="mini-btn secondary">+ Log Progress</button>
        </div>
      </div>
      <div id="canvas" class="canvas"></div>
    </div>`;

html = html.replace(oldPattern, replacement);
fs.writeFileSync('index.html', html, 'utf8');
console.log('✓ Successfully wrapped canvas-col');
