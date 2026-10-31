import { createBoard, applyDream } from '../js/model.js';
import { astar } from '../js/astar.js';
import offline from '../js/dreamers/offline.js';
import { buildUserPrompt } from '../js/dreamers/protocol.js';

console.log('--- TEST 1: applyDream auto-links leaf nodes ---');
const b = createBoard({ goal: 'Launch SaaS', context: 'Solo dev' });
// Simulate an AI response that only provided incoming actions (leaf nodes)
const leafResult = {
  states: [
    { key: 's1', label: 'Validate with 5 customers', note: 'Customer discovery', h: 4 },
    { key: 's2', label: 'Build minimal landing page', note: 'Pre-launch signups', h: 3 }
  ],
  actions: [
    { from: 'START', to: 's1', label: 'Conduct interviews', time: 2, money: 0, effort: 3, risk: 1 },
    { from: 'START', to: 's2', label: 'Deploy Carrd landing page', time: 1, money: 0, effort: 2, risk: 1 }
    // Intentionally omitting outgoing actions from s1 and s2
  ]
};

const added = applyDream(b, leafResult, { hereId: b.startId, by: 'test' });
console.log('Created nodes:', added.nodes.length, 'Created edges:', added.edges.length);

for (const nid of added.nodes) {
  const outs = Object.values(b.edges).filter(e => e.from === nid);
  if (outs.length === 0) {
    console.error(`FAILED: Node ${nid} is still a leaf node with 0 outgoing edges!`);
    process.exit(1);
  }
  console.log(`Node ${nid} (${b.nodes[nid].label}) has ${outs.length} outgoing edge(s) -> ${b.nodes[outs[0].to]?.label}`);
}

const r = astar(b, { time: 1, money: 1, effort: 1, risk: 1 });
if (!r.found) {
  console.error('FAILED: A* could not find a path to GOAL through the newly linked nodes!');
  process.exit(1);
}
console.log('SUCCESS: A* found path to goal with cost:', r.cost, 'Path nodes:', r.nodes.length);

console.log('--- TEST 2: offline expand returns connected actions ---');
const expandReq = {
  mode: 'expand',
  goal: { label: 'Move to Canada' },
  start: { label: 'Software dev in Lagos' },
  focus: { node: { id: b.startId, label: 'Where I am now', note: '', h: 10 } },
  existing: [{ id: b.startId, label: 'Where I am now', kind: 'start' }, { id: b.goalId, label: 'Move to Canada', kind: 'goal' }],
  params: { maxStates: 10, detail: 'detailed', routes: 'many', weights: { time: 1, money: 1, effort: 1, risk: 1 } }
};

const expandRes = await offline.generate(expandReq);
console.log('Offline expand states:', expandRes.states.length, 'actions:', expandRes.actions.length);
if (!expandRes.states.length || !expandRes.actions.length) {
  console.error('FAILED: offline expand returned empty states or actions!');
  process.exit(1);
}
// Verify actions connect beyond just HERE -> child
const outgoingFromChildren = expandRes.actions.filter(a => a.from !== 'HERE');
console.log('Actions leaving child states:', outgoingFromChildren.length);
if (outgoingFromChildren.length === 0) {
  console.error('FAILED: offline expand did not produce outgoing actions from children!');
  process.exit(1);
}
console.log('SUCCESS: offline expand provides downstream actions');

console.log('--- TEST 3: protocol prompt reinforces multi-path and no-leaf ---');
const dreamPrompt = buildUserPrompt({
  mode: 'dream',
  goal: { label: 'Run a Marathon' },
  start: { label: 'Couch potato' },
  params: { maxStates: 14, detail: 'detailed', routes: 'many' }
});

if (!dreamPrompt.includes('CRITICAL REQUIREMENT — MULTIPLE PARALLEL PATHS')) {
  console.error('FAILED: dream prompt does not contain multi-path requirement!');
  process.exit(1);
}

const expandPrompt = buildUserPrompt({
  mode: 'expand',
  goal: { label: 'Run a Marathon' },
  start: { label: 'Couch potato' },
  focus: { node: { id: 'n1', label: 'Ran 5k', note: '', h: 8 } },
  params: { maxStates: 8, detail: 'normal', routes: 'some' }
});

if (!expandPrompt.includes('NO DEAD-END LEAF NODES')) {
  console.error('FAILED: expand prompt does not contain no-leaf requirement!');
  process.exit(1);
}

console.log('SUCCESS: all prompt checks passed!');
console.log('ALL TESTS PASSED SUCCESSFULLY!');
