#!/usr/bin/env node
// A guided tour of GoalStar's important features, built around real situations.
// Each scenario tells you what to expect, runs it for real, and reports pass or fail.
//
//   npm run try                  every scenario (start the app first with: npm start)
//   npm run try -- astar         one scenario: astar, memory, privacy, proof, browser
//   npm run try -- --auto        accept defaults and skip the checks that need your eyes
//
// The memory scenario writes one memory to Walrus Mainnet. It uses a throwaway ID
// unless you set GOALSTAR_MEMORY_ID.
import 'dotenv/config';
import crypto from 'node:crypto';
import readline from 'node:readline/promises';
import { astar, edgeCost } from '../js/astar.js';
import { scoreStep } from '../lib/friction.js';

const API = process.env.API_BASE || 'http://localhost:8000';
const args = process.argv.slice(2);
const AUTO = args.includes('--auto');
const picked = args.filter((a) => !a.startsWith('--'));
const rl = AUTO ? null : readline.createInterface({ input: process.stdin, output: process.stdout });

const tally = { pass: 0, fail: 0, skip: 0 };
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const newId = () => crypto.randomBytes(24).toString('hex');
let memoryId = process.env.GOALSTAR_MEMORY_ID || '';

function heading(title, why) {
  console.log(`\n${'='.repeat(70)}\n${title}\n${'='.repeat(70)}\n${why}\n`);
}

function check(name, ok, detail = '') {
  tally[ok ? 'pass' : 'fail']++;
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? `\n        ${detail}` : ''}`);
}

async function ask(question, fallback) {
  if (AUTO) return fallback;
  const answer = (await rl.question(`  ${question}${fallback ? ` [${fallback}]` : ''}: `)).trim();
  return answer || fallback;
}

// A check only a person can make: what's on the screen.
async function look(instructions, expected) {
  console.log(`\n  DO THIS:  ${instructions}\n  EXPECT:   ${expected}`);
  if (AUTO) {
    tally.skip++;
    console.log('  SKIP  needs your eyes');
    return;
  }
  const answer = (await rl.question('  Did that happen? (y/n/s to skip): ')).trim().toLowerCase();
  if (answer.startsWith('s')) {
    tally.skip++;
    return;
  }
  check(expected, answer.startsWith('y'));
}

async function call(path, { body, id, method } = {}) {
  const res = await fetch(`${API}${path}`, {
    method: method || (body ? 'POST' : 'GET'),
    headers: { 'Content-Type': 'application/json', ...(id ? { 'X-GoalStar-Memory': id } : {}) },
    body: body ? JSON.stringify(body) : undefined,
  });
  return { status: res.status, data: await res.json().catch(() => null) };
}

async function serverIsUp() {
  try {
    return (await fetch(`${API}/api/memory/stats`)).ok;
  } catch {
    return false;
  }
}

// ---- A*: no network, just the planner ------------------------------------------
function jobAbroadBoard() {
  const step = (id, from, to, label, [time, money, effort, risk]) => ({ id, from, to, label, cost: { time, money, effort, risk } });
  const nodes = {
    start: { id: 'start', kind: 'start', label: 'Mid-level designer, employed locally', h: 6, done: true },
    apply: { id: 'apply', kind: 'state', label: 'Interviews booked abroad', h: 3 },
    agency: { id: 'agency', kind: 'state', label: 'Signed with a recruiter', h: 2 },
    masters: { id: 'masters', kind: 'state', label: 'Admitted to a master\'s abroad', h: 1.5 },
    goal: { id: 'goal', kind: 'goal', label: 'Working abroad on a sponsored visa', h: 0 },
  };
  const list = [
    step('a1', 'start', 'apply', 'Apply directly to companies abroad', [5, 1, 6, 6]),
    step('a2', 'apply', 'goal', 'Win an offer with visa sponsorship', [4, 2, 4, 5]),
    step('b1', 'start', 'agency', 'Hire a recruiter agency', [3, 4, 2, 3]),
    step('b2', 'agency', 'goal', 'Get placed by the recruiter', [3, 5, 2, 4]),
    step('c1', 'start', 'masters', 'Enroll in a master\'s degree abroad', [9, 9, 7, 2]),
    step('c2', 'masters', 'goal', 'Convert a student visa to a work visa', [3, 2, 3, 1]),
  ];
  return { nodes, edges: Object.fromEntries(list.map((e) => [e.id, e])), startId: 'start', goalId: 'goal' };
}

async function scenarioAstar() {
  heading(
    'A* PATHFINDING: why a route wins',
    'Situation: you want to work abroad, and there are three real ways to get there.\n'
    + 'GoalStar treats that as a map. Milestones are places, actions are roads, and each\n'
    + 'road costs time, money, effort and risk. A* finds the cheapest way to the goal.\n'
    + 'At each turn it opens the milestone with the lowest f = g + h, where g is the cost\n'
    + 'so far and h is the estimate of what remains.',
  );
  const board = jobAbroadBoard();
  const even = { time: 1, money: 1, effort: 1, risk: 1 };
  const first = (r) => r.edges[0];
  const describe = (r) => r.edges.map((id) => board.edges[id].label).join(' -> ');

  const base = astar(board, even);
  console.log('  How A* searched, in the order it opened milestones:');
  for (const id of base.explored) {
    const g = base.g.get(id), h = board.nodes[id].h;
    console.log(`    ${board.nodes[id].label.padEnd(38)} g ${g.toFixed(2).padStart(5)}  h ${h.toFixed(2).padStart(5)}  f ${(g + h).toFixed(2).padStart(5)}`);
  }
  console.log(`\n  Best route: ${describe(base)} (cost ${base.cost.toFixed(2)})\n`);
  check('With balanced priorities, the recruiter wins', first(base) === 'b1');

  const broke = astar(board, { ...even, money: 5 });
  check('If money is tight, applying directly wins', first(broke) === 'a1', describe(broke));

  const careful = astar(board, { ...even, risk: 5 });
  check('If you can\'t afford risk, the degree wins', first(careful) === 'c1', describe(careful));

  const memory = { text: 'Two recruiter agencies ghosted me for 3 weeks. Wasted money and frustrated.', distance: 0.4, created_at: new Date().toISOString(), blob_id: 'example' };
  const scored = scoreStep('Hire a recruiter agency', [memory]);
  const remembered = astar(board, even, { frictionFn: (label) => (label === 'Hire a recruiter agency' ? scored.penalty : 0) });
  console.log(`\n  Now suppose you remember: "${memory.text}"`);
  console.log(`  That adds +${scored.penalty} to "Hire a recruiter agency": cost ${edgeCost(board.edges.b1, even).toFixed(2)} becomes ${edgeCost(board.edges.b1, even, () => scored.penalty).toFixed(2)}.\n`);
  check('A remembered bad experience moves the route', first(remembered) === 'a1', describe(remembered));
}

// ---- Learning from a real blocker ------------------------------------------------
async function scenarioMemory() {
  heading(
    'MEMORY: a bad day changes tomorrow\'s plan',
    'Situation: a task went badly. You log it from the terminal, as you would mid-work.\n'
    + 'Walrus stores it on Mainnet and GoalStar raises the cost of related steps. Other\n'
    + 'steps stay untouched. Indexing takes about 30 seconds.',
  );
  if (!memoryId) {
    memoryId = newId();
    console.log('  Using a throwaway memory ID, so your own memory stays clean.\n');
  }
  const step = await ask('A step you\'re planning', 'Set up Docker for my app');
  const blocker = await ask('What went wrong last time', 'Spent 4 hours fighting Docker configs and the k8s cluster, exhausted.');
  const other = await ask('A step that has nothing to do with it', 'Book flights to Lisbon');

  const priced = async () => (await call('/api/memory/friction', { body: { labels: [step, other], fresh: true }, id: memoryId })).data.steps;
  const before = (await priced())[step];
  console.log(`\n  Before: "${step}" has ${before.penalty > 0 ? '+' : ''}${before.penalty} from memory.`);

  const saved = await call('/api/memory/remember', { body: { text: blocker, category: 'try_script' }, id: memoryId });
  check('Written to Walrus Mainnet', saved.data?.mode === 'walrus_mainnet', saved.data?.error);
  if (saved.data?.mode !== 'walrus_mainnet') return;

  process.stdout.write('  Waiting for Walrus to index it');
  const deadline = Date.now() + 180000;
  let steps = await priced();
  while (steps[step].penalty === before.penalty && Date.now() < deadline) {
    process.stdout.write('.');
    await sleep(6000);
    steps = await priced();
  }
  console.log('');
  const after = steps[step];
  check('The related step now costs more', after.penalty > before.penalty, `+${after.penalty}, because: "${after.because?.text}"`);
  check('The unrelated step is untouched', steps[other].penalty === 0, `"${other}": ${steps[other].penalty}`);
}

// ---- One person's memory stays theirs -------------------------------------------
async function scenarioPrivacy() {
  heading(
    'PRIVACY: your memory is yours',
    'Situation: two people use the same deployment. Neither should see the other\'s\n'
    + 'blockers, and nobody should be able to reach another namespace on the account.',
  );
  const stranger = newId();
  const ownerView = memoryId ? await call('/api/memory/recall', { body: { query: 'what went wrong', limit: 5 }, id: memoryId }) : null;
  const strangerView = await call('/api/memory/recall', { body: { query: 'what went wrong', limit: 5 }, id: stranger });
  if (ownerView) check('You can read your own memory', ownerView.data.results.length > 0, `${ownerView.data.results.length} found`);
  check('A stranger reads nothing', strangerView.data.results.length === 0, `${strangerView.data.results.length} found`);

  const forced = await call('/api/memory/recall', { body: { query: 'anything', namespace: 'some-other-project', limit: 1 } });
  check('Asking for another namespace is ignored', forced.data.namespace !== 'some-other-project', `served: ${forced.data.namespace}`);
  check('Writing without a memory ID is refused', (await call('/api/memory/remember', { body: { text: 'anonymous' } })).status === 401);
  check('A malformed memory ID is refused', (await call('/api/memory/recall', { body: { query: 'x' }, id: 'short' })).status === 400);
}

// ---- Proof ----------------------------------------------------------------------
async function scenarioProof() {
  heading(
    'PROOF: check a certificate against the chain',
    'Situation: you tell a mentor or funder you hit a milestone, and they want to check.\n'
    + 'GoalStar re-reads Walrus and Sui through Tatum and reports each check.',
  );
  const head = await call('/api/tatum/sui-status');
  check('Live Sui checkpoint through Tatum gRPC', head.data?.live === true, `#${head.data?.checkpoint}`);
  await sleep(4000);
  const later = await call('/api/tatum/sui-status');
  check('The chain moved while we waited, so the data is live', Number(later.data?.checkpoint) > Number(head.data?.checkpoint), `#${later.data?.checkpoint}`);

  const { data } = await call('/api/tatum/walrus-uploads');
  const newest = (data?.uploads || [])
    .filter((u) => u.status === 'CERTIFIED' && String(u.filename).startsWith('certificate-'))
    .sort((a, b) => b.createdAt - a.createdAt)[0];
  if (!newest) {
    tally.skip++;
    console.log('  SKIP  no certificates yet. Seal one in the app first.');
    return;
  }
  const report = (await call(`/api/tatum/verify/${newest.jobId}`)).data;
  for (const c of report.checks) console.log(`    [${c.status}] ${c.label}: ${c.detail}`);
  check('The certificate verifies end to end', report.verdict === 'verified', `job ${newest.jobId}`);
}

// ---- The real app ---------------------------------------------------------------
async function scenarioBrowser() {
  heading(
    'THE APP: the full loop, by hand',
    `Open ${API} in a private window so you start fresh, and sign in as a guest.`,
  );
  await look('Stay on the sample goal and wait a few seconds.', 'The route moves off Docker, and the banner says "Memory moved your route" and quotes a sample memory');
  await look('Click a step with a red "+ memory" chip.', 'The side panel shows the memory behind the cost and its blob id');
  await look('Tick the next step in "Do next", then wait about 30 seconds.', 'The Walrus count goes from "0 yours" to "1 yours"');
  await look('Add a memory about something you got stuck on, then wait about 30 seconds.', 'Related steps gain a chip, with no reload');
  await look('Create a new goal related to that memory and let it dream a map.', 'A message says "Planning with N of your memories" while the map is drawn');
  await look(`Open ${API}/?staleHours=0.01 and wait about a minute.`, 'A "Watchdog: step stalled" banner appears, and "Break into small steps" splits the step');
  await look('Select a finished milestone and click "Seal certificate on Walrus + Sui". This uses your Tatum key.', 'About a minute later, all six checks are green');
  await look('Open the certificate share link in another private window.', 'It verifies without signing in');
}

const SCENARIOS = { astar: scenarioAstar, memory: scenarioMemory, privacy: scenarioPrivacy, proof: scenarioProof, browser: scenarioBrowser };
const NEEDS_SERVER = new Set(['memory', 'privacy', 'proof', 'browser']);

async function main() {
  const unknown = picked.filter((name) => !SCENARIOS[name]);
  if (unknown.length) throw new Error(`Unknown scenario: ${unknown.join(', ')}. Choose from: ${Object.keys(SCENARIOS).join(', ')}`);
  const names = picked.length ? picked : Object.keys(SCENARIOS);
  if (names.some((n) => NEEDS_SERVER.has(n)) && !(await serverIsUp())) {
    throw new Error(`GoalStar isn't running at ${API}. Start it with: npm start`);
  }
  for (const name of names) await SCENARIOS[name]();
  console.log(`\n${tally.pass} passed, ${tally.fail} failed, ${tally.skip} skipped.\n`);
  rl?.close();
  process.exit(tally.fail ? 1 : 0);
}

main().catch((err) => {
  console.error(`\n${err.message}\n`);
  process.exit(1);
});
