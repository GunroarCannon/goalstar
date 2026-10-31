import { createBoard, applyDream } from '../js/model.js';

const b = createBoard('Test Goal', 'start', 'goal');
const dummyResult = {
  states: [
    { key: 's1', label: 'Draft Prototype', note: 'Wire up UI', h: 3 },
    { key: 's2', label: 'Deploy Staging', note: 'Run tests', h: 1 }
  ],
  actions: [
    { from: 'START', to: 's1', label: 'Create components', time: 2, money: 0, effort: 3, risk: 1 },
    { from: 's1', to: 's2', label: 'Push to Vercel', time: 1, money: 0, effort: 1, risk: 1 },
    { from: 's2', to: 'GOAL', label: 'Verify production', time: 1, money: 0, effort: 1, risk: 1 }
  ]
};

const added = applyDream(b, dummyResult, { by: 'test' });
console.log('applyDream returned:', added);
if (!added || !Array.isArray(added.nodes) || !Array.isArray(added.edges)) {
  console.error('FAILED: added does not have nodes and edges arrays!');
  process.exit(1);
}
console.log('SUCCESS: applyDream correctly returned created nodes and edges:', added.nodes.length, 'nodes,', added.edges.length, 'edges');
