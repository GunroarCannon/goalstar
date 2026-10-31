import fs from 'node:fs';

let html = fs.readFileSync('index.html', 'utf8');

const telemetrySection = `      <section class="telemetry-box">
        <h3>Protocol Telemetry</h3>
        <div class="telemetry-pill">
          <span class="indicator live"></span>
          <span class="lbl">Walrus Memory:</span>
          <span id="walrusCountBadge" class="val">Connecting...</span>
        </div>
        <div class="telemetry-pill">
          <span class="indicator live"></span>
          <span class="lbl">Tatum Sui RPC:</span>
          <span id="tatumRpcBadge" class="val">Connecting...</span>
        </div>
        <div class="telemetry-pill">
          <span class="indicator neutral"></span>
          <span class="lbl">Escalation Rule:</span>
          <span class="val">Auto-decompose &gt;48h</span>
        </div>
      </section>
`;

const bannerHtml = `    <div id="lastTuesdayBanner" class="tuesday-banner">
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
`;

const modalHtml = `  <div id="memoryModal" class="modal-overlay" hidden>
    <div class="modal-card">
      <h3>Log Workflow Update or Blocker</h3>
      <p class="muted small" style="margin-bottom: 8px;">Recorded to Walrus Memory on Mainnet. GoalStar will adjust your A* path in future sessions based on this update.</p>
      <textarea id="memoryInput" rows="4" placeholder="e.g. Spent 3 hours debugging Docker configs, got overwhelmed. Need smaller micro-steps."></textarea>
      <div class="modal-actions">
        <button id="cancelMemoryBtn" class="mini-btn secondary">Cancel</button>
        <button id="saveMemoryBtn" class="mini-btn">Save to Walrus Mainnet</button>
      </div>
    </div>
  </div>
`;

html = html.replace('<section class="danger-zone">', telemetrySection + '      <section class="danger-zone">');
html = html.replace('<div id="canvas" class="canvas"></div>', bannerHtml + '    <div id="canvas" class="canvas"></div>');
html = html.replace('</body>', modalHtml + '</body>');

fs.writeFileSync('index.html', html, 'utf8');
console.log('Successfully updated index.html');
