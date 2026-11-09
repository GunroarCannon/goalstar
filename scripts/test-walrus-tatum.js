// Integration test against the real Walrus Memory relayer and Tatum on Sui mainnet.
// Exits non-zero if anything fails. Pass --seal to also store one new certificate
// on Walrus through Tatum and verify it end to end (takes about two minutes).
import 'dotenv/config';
import { MemWal } from '@mysten-incubation/memwal';
import * as tatum from '../lib/tatum.js';
import { buildCertificate, verifyCertificate, storageEvent } from '../lib/certificate.js';
import { WalrusMemoryBridge } from '../js/walrus-memory.js';
import { assessMemory, scoreStep, frictionForSteps } from '../lib/friction.js';
import { astar } from '../js/astar.js';
import { WorkflowWatchdog } from '../js/watchdog.js';
import { getStarterBoard } from '../js/model.js';

const results = [];

async function test(name, fn) {
  try {
    const detail = await fn();
    results.push(true);
    console.log(`PASS  ${name}${detail ? `\n      ${detail}` : ''}`);
  } catch (err) {
    results.push(false);
    console.error(`FAIL  ${name}\n      ${err.message}`);
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

await test('Walrus Memory relayer is reachable', async () => {
  const mw = MemWal.create({
    key: process.env.MEMWAL_PRIVATE_KEY,
    accountId: process.env.MEMWAL_ACCOUNT_ID,
    serverUrl: process.env.MEMWAL_SERVER_URL || 'https://relayer.memory.walrus.xyz',
    namespace: 'goalstar-test',
  });
  const health = await mw.health();
  return `status: ${health.status || 'ok'}`;
});

let head;
await test('Tatum gRPC returns the live mainnet head', async () => {
  head = await tatum.getChainHead({ fresh: true });
  assert(head.network === 'mainnet', `unexpected network ${head.network}`);
  assert(/^\d+$/.test(head.checkpoint), `bad checkpoint ${head.checkpoint}`);
  assert(head.digest, 'checkpoint has no digest');
  assert(Date.now() - head.timestampMs < 120000, 'head is more than two minutes old');
  return `checkpoint #${head.checkpoint}, digest ${head.digest}`;
});

await test('Reading a checkpoint by number returns the same digest', async () => {
  const again = await tatum.getCheckpoint(head.checkpoint);
  assert(again.digest === head.digest, 'digest mismatch');
});

await test('Tatum storage API lists uploads', async () => {
  const uploads = await tatum.listUploads();
  assert(Array.isArray(uploads), 'expected an array');
  return `${uploads.length} upload(s)`;
});

await test('A certificate anchors to live chain data and is self-hashing', async () => {
  const cert = await buildCertificate({ milestoneId: 't', milestoneLabel: 'Test (not uploaded)' });
  assert(cert.chainAnchor.digest && /^[a-f0-9]{64}$/.test(cert.sha256), 'missing anchor or hash');
});

await test('Memories are read for what they say, not just what they mention', () => {
  const kind = (text, label) => assessMemory(text, label).kind;
  assert(kind('Spent 3 hours debugging Docker configs, exhausted.') === 'blocker', 'missed a plain blocker');
  assert(kind('Docker deployment went smoothly and finished quickly.') === 'win', 'read a win as a blocker');
  assert(kind('No blockers on the Docker work today.') === 'neutral', 'ignored the negation');
  const split = 'Docker configs failed for 4 hours; switching to PaaS worked';
  assert(kind(split, 'Setup Docker cluster') === 'blocker', 'wrong clause for the failing tool');
  assert(kind(split, 'Deploy to PaaS') === 'win', 'wrong clause for the working tool');
  const small = assessMemory('Blocked on Docker.').severity;
  const large = assessMemory('Blocked on Docker for 14 hours and completely exhausted.').severity;
  assert(large > small, 'severity ignores how bad it was');
});

await test('Penalties scale with relevance, and a newer win cancels an old blocker', () => {
  const blocker = { text: 'Spent 4 hours fighting Docker, exhausted.', distance: 0.4, created_at: '2026-11-01T00:00:00Z', blob_id: 'a' };
  const label = 'Setup Docker cluster';
  const now = Date.parse('2026-11-02T00:00:00Z');
  const close = scoreStep(label, [blocker], now);
  assert(close.penalty > 2, `expected a large penalty, got ${close.penalty}`);
  assert(close.because.blob === 'a', 'penalty does not cite its memory');
  assert(scoreStep(label, [{ ...blocker, distance: 0.9 }], now).penalty === 0, 'unrelated memory changed the cost');
  const win = { text: 'Docker setup finished smoothly this time.', distance: 0.4, created_at: '2026-11-01T12:00:00Z', blob_id: 'b' };
  assert(scoreStep(label, [blocker, win], now).penalty < close.penalty, 'newer win did not reduce the penalty');
  assert(scoreStep(label, [{ text: '[BLOB 12] board "Docker failed" {}', distance: 0.1 }], now).penalty === 0, 'a stored document counted as a memory');
});

await test('The watchdog flags only the overdue next step on the route', () => {
  const board = getStarterBoard();
  const route = astar(board, { time: 1, money: 1, effort: 1, risk: 1 }).edges;
  const watchdog = new WorkflowWatchdog();
  assert(watchdog.evaluateEscalation(board, route).length === 0, 'flagged a brand new board');
  board.created = Date.now() - 72 * 3600000;
  const stalled = watchdog.evaluateEscalation(board, route);
  assert(stalled.length === 1 && stalled[0].edgeId === 'e2_devops', `expected only the next step, got ${JSON.stringify(stalled)}`);
  board.edges.e2_devops.touchedAt = Date.now();
  assert(watchdog.evaluateEscalation(board, route).length === 0, 'recent progress should clear the stall');
});

const namespace = process.env.MEMWAL_NAMESPACE || 'goalstar-workflows';
const memwal = MemWal.create({
  key: process.env.MEMWAL_PRIVATE_KEY,
  accountId: process.env.MEMWAL_ACCOUNT_ID,
  serverUrl: process.env.MEMWAL_SERVER_URL || 'https://relayer.memory.walrus.xyz',
  namespace,
});

await test('At least 10 memories are stored on Mainnet', async () => {
  const { namespaces } = await memwal.listNamespaces();
  const count = namespaces.find((n) => n.name === namespace)?.memory_count ?? 0;
  assert(count >= 10, `only ${count} in ${namespace}`);
  return `${count} memories in ${namespace}`;
});

await test('Real Mainnet memories move the route on the starter board', async () => {
  const board = getStarterBoard();
  const weights = { time: 1, money: 1, effort: 1, risk: 1 };
  const labels = Object.values(board.edges).map((e) => e.label);
  const steps = await frictionForSteps(memwal, labels, namespace, { fresh: true });
  const bridge = new WalrusMemoryBridge();
  for (const [label, value] of Object.entries(steps)) bridge.friction.set(label, value);

  const before = astar(board, weights);
  const after = astar(board, weights, { frictionFn: (l) => bridge.getFrictionPenalty(l) });
  assert(before.found && after.found, 'no route');
  assert(before.edges.includes('e2_devops'), 'starter route should begin on the Docker step');
  assert(after.edges.includes('e3_paas') && !after.edges.includes('e2_devops'), 'route did not move off the Docker step');
  const docker = steps['Setup Docker cluster and k8s config'];
  return `Docker step +${docker.penalty}, because "${docker.because.text.slice(0, 70)}"; cost ${before.cost} -> ${after.cost}`;
});

await test('Unrelated goals are left alone', async () => {
  const labels = ['Learn Spanish basics', 'Book flights to Lisbon', 'Cook dinner at home on weekdays'];
  const steps = await frictionForSteps(memwal, labels, namespace, { fresh: true });
  for (const label of labels) assert(steps[label].penalty === 0, `${label} got ${steps[label].penalty} from: ${steps[label].because?.text}`);
});

await test('The newest stored certificate verifies end to end', async () => {
  const uploads = await tatum.listUploads();
  const newest = uploads
    .filter((u) => u.status === 'CERTIFIED' && String(u.filename).startsWith('certificate-'))
    .sort((a, b) => b.createdAt - a.createdAt)[0];
  if (!newest) return 'skipped: no certificates stored yet (run with --seal)';
  const report = await verifyCertificate(newest.jobId);
  assert(report.verdict === 'verified', JSON.stringify(report.checks));
  return `job ${newest.jobId}, tx ${storageEvent(newest, 'certified')?.txDigest}`;
});

if (process.argv.includes('--seal')) {
  await test('Seal a new certificate and verify it on chain', async () => {
    const cert = await buildCertificate({
      milestoneId: 'pipeline-check',
      milestoneLabel: 'Proof pipeline live check',
      goal: 'GoalStar integration test',
    });
    const job = await tatum.uploadJson(JSON.stringify(cert), `certificate-${cert.sha256.slice(0, 8)}.json`);
    assert(job.jobId, `no job id: ${JSON.stringify(job)}`);
    console.log(`      uploaded, job ${job.jobId}, waiting for Walrus certification...`);

    const deadline = Date.now() + 5 * 60 * 1000;
    let report;
    do {
      await new Promise((resolve) => setTimeout(resolve, 8000));
      report = await verifyCertificate(job.jobId);
    } while (report.verdict === 'pending' && Date.now() < deadline);

    for (const check of report.checks) console.log(`      [${check.status}] ${check.label}: ${check.detail}`);
    assert(report.verdict === 'verified', `verdict was ${report.verdict}`);
    return `job ${job.jobId}`;
  });
}

const passed = results.filter(Boolean).length;
console.log(`\nSummary: ${passed}/${results.length} tests passed.`);
process.exit(passed === results.length ? 0 : 1);
