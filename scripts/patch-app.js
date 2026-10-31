import fs from 'node:fs';

let code = fs.readFileSync('js/app.js', 'utf8');

// 1. Add imports at top
const importsToAdd = `import { walrusMemory } from './walrus-memory.js';
import { tatumSui } from './tatum-sui.js';
import { WorkflowWatchdog } from './watchdog.js';
`;
code = importsToAdd + code;

// 2. Initialize watchdog
code = code.replace("const data = loadData();", `const data = loadData();
const watchdog = new WorkflowWatchdog(walrusMemory);
const frictionFn = (lbl) => walrusMemory.getFrictionPenalty(lbl);`);

// 3. Update astar calls to include frictionFn
code = code.replace(/astar\(b, w\)/g, "astar(b, w, { frictionFn })");
code = code.replace(/astar\(b, settings\(\)\.weights\)/g, "astar(b, settings().weights, { frictionFn })");

// 4. Add UI banner & telemetry update function
const walrusUiWiring = `
// ---------- Walrus Memory & Tatum Sui Wiring ----------
async function updateWalrusTelemetry() {
  const stats = await walrusMemory.checkStatus();
  const memories = await walrusMemory.recall();
  const countBadge = $('#walrusCountBadge');
  if (countBadge) {
    countBadge.textContent = stats.enabled 
      ? \`Mainnet (\${memories.length} memories)\`
      : \`Local Pending (\${memories.length})\`;
  }

  const insight = watchdog.generateLastTuesdayInsight();
  const textEl = $('#tuesdayText');
  const ruleEl = $('#tuesdayRule');
  if (textEl && ruleEl) {
    textEl.textContent = insight.text;
    ruleEl.textContent = insight.ruleApplied;
  }

  refresh({ inspector: false });
}

async function updateTatumTelemetry() {
  const sui = await tatumSui.checkStatus();
  const badge = $('#tatumRpcBadge');
  if (badge) {
    if (sui && sui.checkpoint) {
      badge.textContent = \`Sui #\${sui.checkpoint}\`;
    } else {
      badge.textContent = 'Gateway Ready';
    }
  }
}

// Modal & button wiring
$('#seedMemoriesBtn')?.addEventListener('click', async () => {
  const btn = $('#seedMemoriesBtn');
  btn.textContent = 'Seeding...';
  btn.disabled = true;
  await walrusMemory.seedTenMemories();
  await updateWalrusTelemetry();
  btn.textContent = '✓ 10 Stored';
  setTimeout(() => { btn.textContent = 'Seed 10 Memories'; btn.disabled = false; }, 3000);
});

$('#addMemoryBtn')?.addEventListener('click', () => {
  const modal = $('#memoryModal');
  if (modal) modal.hidden = false;
});

$('#cancelMemoryBtn')?.addEventListener('click', () => {
  const modal = $('#memoryModal');
  if (modal) modal.hidden = true;
});

$('#saveMemoryBtn')?.addEventListener('click', async () => {
  const input = $('#memoryInput');
  const text = (input?.value || '').trim();
  if (!text) return;

  const btn = $('#saveMemoryBtn');
  btn.textContent = 'Writing to Mainnet...';
  btn.disabled = true;

  await walrusMemory.remember(text, 'user_update');
  input.value = '';
  $('#memoryModal').hidden = true;
  btn.textContent = 'Save to Walrus Mainnet';
  btn.disabled = false;

  await updateWalrusTelemetry();
});

// Sui Onchain Proof in Inspector
document.addEventListener('click', async (e) => {
  const suiBtn = e.target.closest('[data-act=\"sui-stamp\"]');
  if (suiBtn) {
    const nodeId = suiBtn.dataset.nodeid;
    const b = board();
    const node = b?.nodes[nodeId];
    if (!node) return;

    suiBtn.textContent = 'Verifying on Sui...';
    suiBtn.disabled = true;

    const res = await tatumSui.stampMilestone(node.id, node.label);
    if (res && res.onchainProof) {
      suiBtn.replaceWith(Object.assign(document.createElement('div'), {
        className: 'sui-proof-card',
        innerHTML: \`<b>✓ Verified on Sui Mainnet</b><br>
          Checkpoint: #\${res.onchainProof.checkpoint}<br>
          <span class=\"code\">Digest: \${res.onchainProof.proofDigest}</span>\`
      }));
    } else {
      suiBtn.textContent = 'Verification Failed';
    }
  }

  const escBtn = e.target.closest('[data-act=\"auto-decompose\"]');
  if (escBtn) {
    const nodeId = escBtn.dataset.nodeid;
    const b = board();
    if (b && b.nodes[nodeId]) {
      escBtn.textContent = 'Decomposing into 15m steps...';
      select({ type: 'node', id: nodeId });
      // trigger dreamer breakdown / next states
      const dreamBtn = $('.ins-head + label + label + div + div button.dream');
      if (dreamBtn) dreamBtn.click();
    }
  }
});
`;

// Append telemetry wiring before boot section
code = code.replace("// ---------- boot ----------", walrusUiWiring + "\n// ---------- boot ----------");

// Add telemetry updates to boot
code += `
updateWalrusTelemetry();
updateTatumTelemetry();
`;

// Inject Sui Stamp & Escalation button inside renderInspector()
const inspectorTarget = "${outs.length ? `<h4>From here (${outs.length})</h4><ul class=\"rel\">${outs.map((e) => edgeRow(b, e, 'out')).join('')}</ul>` : ''}";
const inspectorAugment = `\${outs.length ? \`<h4>From here (\${outs.length})</h4><ul class=\"rel\">\${outs.map((e) => edgeRow(b, e, 'out')).join('')}</ul>\` : ''}
      \${n.done ? \`<button class=\"sui-stamp-btn\" data-act=\"sui-stamp\" data-nodeid=\"\${n.id}\">🔗 Verify Milestone on Sui (Tatum RPC)</button>\` : ''}
      \${!n.done && n.kind === 'state' ? \`<button class=\"mini-btn\" style=\"width: 100%; margin-top: 10px; background: #6366f1;\" data-act=\"auto-decompose\" data-nodeid=\"\${n.id}\">⚡ Apply Learned Escalation: Decompose</button>\` : ''}`;

code = code.replace(inspectorTarget, inspectorAugment);

fs.writeFileSync('js/app.js', code, 'utf8');
console.log('Successfully patched js/app.js');
