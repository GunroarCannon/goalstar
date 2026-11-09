import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import path from 'node:path';
import fs from 'node:fs';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { MemWal } from '@mysten-incubation/memwal';
import * as tatum from './lib/tatum.js';
import { buildCertificate, verifyCertificate, storageEvent, CERTIFICATE_VERSION } from './lib/certificate.js';
import { frictionForSteps, forgetCachedFriction } from './lib/friction.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());

// Landing page and root app routes
app.get(['/home', '/home.html'], (req, res) => {
  const p = path.join(__dirname, 'public', 'home.html');
  if (fs.existsSync(p)) return res.sendFile(p);
  res.sendFile(path.join(__dirname, 'home.html'));
});

app.get(['/', '/index.html'], (req, res) => {
  const p = path.join(__dirname, 'public', 'index.html');
  if (fs.existsSync(p)) return res.sendFile(p);
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(__dirname));

// ---- Walrus Memory Client ----
const DATA_DIR = process.env.VERCEL ? path.join('/tmp', 'data') : path.resolve(__dirname, 'data');
try { fs.mkdirSync(DATA_DIR, { recursive: true }); } catch (e) {}
const LOG_FILE = path.join(DATA_DIR, 'memory-log.jsonl');

const NAMESPACE = process.env.MEMWAL_NAMESPACE || 'goalstar-workflows';

let memwalClient = null;
const stats = { written: 0, failed: 0, recalls: 0, recallMs: 0 };
const pendingQueue = new Map(); // ns -> [{ text, at }]
const PENDING_WINDOW_MS = 3 * 60 * 1000;

function getMemwal() {
  if (!memwalClient && process.env.MEMWAL_PRIVATE_KEY && process.env.MEMWAL_ACCOUNT_ID) {
    try {
      memwalClient = MemWal.create({
        key: process.env.MEMWAL_PRIVATE_KEY,
        accountId: process.env.MEMWAL_ACCOUNT_ID,
        serverUrl: process.env.MEMWAL_SERVER_URL || 'https://relayer.memory.walrus.xyz',
        namespace: NAMESPACE,
      });
      console.log('[OK] Walrus Memory connected on Mainnet. Account:', process.env.MEMWAL_ACCOUNT_ID.slice(0, 10) + '...');
    } catch (err) {
      console.warn('! Failed to initialize Walrus Memory client:', err.message);
    }
  }
  return memwalClient;
}

function recordPending(ns, text) {
  const list = pendingQueue.get(ns) || [];
  list.push({ text, at: Date.now() });
  pendingQueue.set(ns, list.filter(item => Date.now() - item.at < PENDING_WINDOW_MS));
}

// ---- Walrus blobs: board snapshots, certificates, shared templates ----
// Everything published here is a JSON document with a content-addressed id.
// It goes to a real Walrus publisher when one is configured, and is always
// mirrored into Walrus Memory so any device on this account can read it back.
const BLOB_DIR = path.join(DATA_DIR, 'blobs');
fs.mkdirSync(BLOB_DIR, { recursive: true });
const BLOB_INDEX = path.join(DATA_DIR, 'blobs.json');
const TEMPLATE_FILE = path.join(DATA_DIR, 'templates.json');
const WALRUS_PUBLISHER = process.env.WALRUS_PUBLISHER_URL || '';
const WALRUS_AGGREGATOR = process.env.WALRUS_AGGREGATOR_URL || 'https://aggregator.walrus.space';

const readJsonFile = (f, d) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return d; } };
const writeJsonFile = (f, v) => fs.writeFileSync(f, JSON.stringify(v));
const blobIndex = () => readJsonFile(BLOB_INDEX, {});

async function publishBlob(payload, { kind = 'board', namespace = null, label = '' } = {}) {
  const json = JSON.stringify(payload);
  const id = crypto.createHash('sha256').update(json).digest('hex').slice(0, 32);
  const ns = namespace || NAMESPACE;
  const idx = blobIndex();
  if (!idx[id]) {
    idx[id] = { id, kind, label, namespace: ns, at: new Date().toISOString(), bytes: json.length, storage: 'local' };
    writeJsonFile(BLOB_INDEX, idx);
  }
  fs.mkdirSync(BLOB_DIR, { recursive: true }); // stays valid even if the cache dir is wiped
  fs.writeFileSync(path.join(BLOB_DIR, `${id}.json`), json);

  let storage = idx[id].storage || 'local';

  // Primary: Walrus storage through Tatum. Uploads certify asynchronously, so a
  // job id is the success signal; the blob id appears once the job completes.
  if (tatum.isConfigured() && !idx[id].tatumJobId) {
    try {
      const job = await tatum.uploadJson(json, `${kind}-${id.slice(0, 8)}.json`);
      idx[id] = { ...idx[id], storage: 'walrus_tatum', tatumJobId: job.jobId, blobId: job.blobId || null };
      writeJsonFile(BLOB_INDEX, idx);
      storage = 'walrus_tatum';
    } catch (e) {
      console.warn('[Tatum storage] upload failed:', e.message);
    }
  }

  // Fallback / Direct publisher if configured
  if (storage === 'local' && WALRUS_PUBLISHER) {
    try {
      const res = await fetch(`${WALRUS_PUBLISHER}/v1/blobs?epochs=5`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: json,
      });
      if (res.ok) {
        const j = await res.json();
        const blobId = j.newlyCreated?.blobObject?.blobId || j.alreadyCertified?.blobId;
        if (blobId) {
          idx[id] = { ...idx[id], storage: 'walrus_blob', blobId };
          writeJsonFile(BLOB_INDEX, idx);
          storage = 'walrus_blob';
        }
      }
    } catch (e) { console.warn('[Walrus] publisher unavailable:', e.message); }
  }

  // Always mirror into Memwal decentralized portable memory
  const mw = getMemwal();
  if (mw) {
    try {
      await mw.remember(`[BLOB ${id}] ${kind} "${label}" ${json}`, ns);
      if (storage === 'local') {
        idx[id] = { ...idx[id], storage: 'walrus_memory' };
        writeJsonFile(BLOB_INDEX, idx);
        storage = 'walrus_memory';
      }
    } catch (e) { console.warn('[Walrus] blob memory write failed:', e.message); }
  }

  return {
    id,
    kind,
    storage,
    label,
    blobId: idx[id]?.blobId || null,
    tatumJobId: idx[id]?.tatumJobId || null,
    at: idx[id].at,
    bytes: json.length,
    url: `/api/walrus/blob/${id}`
  };
}

async function readBlob(id) {
  if (!/^[a-f0-9]{8,64}$/.test(String(id || ''))) return null;
  const file = path.join(BLOB_DIR, `${id}.json`);
  if (fs.existsSync(file)) return JSON.parse(fs.readFileSync(file, 'utf8'));

  const meta = blobIndex()[id];
  // Tatum stores files as Walrus quilts, so read the individual file by patch id.
  if (meta?.tatumJobId) {
    try {
      const job = await tatum.getUpload(meta.tatumJobId);
      if (job.downloadUrlByQuiltPatchId) {
        const r = await fetch(job.downloadUrlByQuiltPatchId);
        if (r.ok) return await r.json();
      }
    } catch { /* fall through to the memory mirror */ }
  }

  if (meta?.blobId && meta.storage === 'walrus_blob') {
    try {
      const r = await fetch(`${WALRUS_AGGREGATOR}/v1/blobs/${meta.blobId}`);
      if (r.ok) return await r.json();
    } catch { /* fall through to the memory mirror */ }
  }

  const mw = getMemwal();
  if (mw) {
    try {
      const resp = await mw.recall({ query: `BLOB ${id}`, limit: 8, namespace: meta?.namespace || NAMESPACE });
      for (const item of resp.results || []) {
        const text = String(item.text || '');
        const at = text.indexOf(`[BLOB ${id}]`);
        if (at < 0) continue;
        const brace = text.indexOf('{', at);
        if (brace >= 0) return JSON.parse(text.slice(brace));
      }
    } catch (e) { console.warn('[Walrus] blob recall failed:', e.message); }
  }
  return null;
}

// ==========================================
//               API ROUTES
// ==========================================

// Health & System Info
app.get('/api/health', async (req, res) => {
  const mw = getMemwal();
  let mwStatus = 'unconfigured';
  if (mw) {
    try {
      const h = await mw.health();
      mwStatus = h.status || 'connected';
    } catch (e) {
      mwStatus = 'error: ' + e.message;
    }
  }

  let sui = null;
  try {
    sui = { live: true, ...(await tatum.getChainHead()) };
  } catch (e) {
    sui = { live: false, error: e.message };
  }

  res.json({
    status: 'ok',
    product: 'GoalStar Total Recall Edition',
    walrus: {
      enabled: !!mw,
      status: mwStatus,
      accountId: process.env.MEMWAL_ACCOUNT_ID ? `${process.env.MEMWAL_ACCOUNT_ID.slice(0, 10)}...` : null,
      namespace: NAMESPACE,
    },
    tatum: {
      gateway: tatum.GRPC_HOST,
      keyConfigured: tatum.isConfigured(),
      sui,
      rateLimitRps: tatum.RATE_LIMIT_RPS,
    },
  });
});

// What the browser needs to know about server-side configuration.
app.get('/api/config', (req, res) => {
  res.json({
    groq: { configured: !!process.env.GROQ_API_KEY, model: process.env.GROQ_MODEL || 'openai/gpt-oss-120b', viaServer: true },
    walrus: {
      configured: !!(process.env.MEMWAL_ACCOUNT_ID && process.env.MEMWAL_PRIVATE_KEY),
      namespace: NAMESPACE,
      publisher: !!WALRUS_PUBLISHER,
    },
    tatum: {
      configured: !!process.env.TATUM_API_KEY,
      walrusStorage: !!process.env.TATUM_API_KEY,
    },
  });
});

// Groq through the server, so the token lives in this project's .env and never
// has to be pasted into the browser.
app.post('/api/llm/groq', async (req, res) => {
  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) return res.status(503).json({ error: 'GROQ_API_KEY is missing from this project\u2019s .env' });
  try {
    const upstream = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
      body: JSON.stringify({ ...(req.body || {}), model: req.body?.model || process.env.GROQ_MODEL || 'openai/gpt-oss-120b' }),
    });
    const text = await upstream.text();
    res.status(upstream.status).type('application/json').send(text);
  } catch (err) {
    res.status(502).json({ error: `Groq unreachable (${err.message})` });
  }
});

// Every person gets a private namespace derived from a secret memory ID. The server
// derives it, and never accepts a namespace from a request: this Walrus account holds
// other projects too. With no ID, requests can only read the project's sample memory.
const MEMORY_ID = /^[A-Za-z0-9_-]{24,128}$/;

app.use(['/api/memory', '/api/agent'], (req, res, next) => {
  const id = req.get('x-goalstar-memory');
  if (id && !MEMORY_ID.test(id)) return res.status(400).json({ error: 'Invalid memory ID' });
  req.personalNamespace = id ? `goalstar-u-${crypto.createHash('sha256').update(id).digest('hex').slice(0, 32)}` : null;
  next();
});

// The relayer's own counts, which unlike a recall are exact.
let countCache = { at: 0, map: null };
async function namespaceCounts(mw) {
  if (Date.now() - countCache.at < 10000) return countCache.map;
  try {
    const { namespaces } = await mw.listNamespaces();
    countCache = { at: Date.now(), map: new Map(namespaces.map((n) => [n.name, n.memory_count])) };
    return countCache.map;
  } catch (err) {
    console.warn('[Walrus] Count failed:', err.message);
    return null;
  }
}

// Memory Stats & Telemetry
app.get('/api/memory/stats', async (req, res) => {
  const mw = getMemwal();
  const counts = mw ? await namespaceCounts(mw) : null;
  const ns = req.personalNamespace || NAMESPACE;
  res.json({
    ...stats,
    avgRecallMs: stats.recalls ? Math.round(stats.recallMs / stats.recalls) : 0,
    enabled: !!mw,
    memoryCount: counts ? counts.get(ns) ?? 0 : null,
    sampleCount: counts ? counts.get(NAMESPACE) ?? 0 : null,
    accountId: process.env.MEMWAL_ACCOUNT_ID || null,
    namespace: ns,
  });
});

// Write Memory (Single)
app.post('/api/memory/remember', async (req, res) => {
  const { text, friction, category } = req.body || {};
  if (!text) return res.status(400).json({ error: 'Text required' });
  if (!req.personalNamespace) return res.status(401).json({ error: 'A memory ID is required to write memories' });

  const ns = req.personalNamespace;
  recordPending(ns, text);

  const entry = {
    at: new Date().toISOString(),
    ns,
    text,
    friction: friction ?? 0,
    category: category || 'general',
  };

  fs.appendFileSync(LOG_FILE, JSON.stringify(entry) + '\n');

  const mw = getMemwal();
  if (!mw) {
    return res.json({ success: true, mode: 'local_pending', text, ns });
  }

  try {
    const job = await mw.remember(text, ns);
    stats.written++;
    forgetCachedFriction();
    countCache.at = 0;
    res.json({ success: true, mode: 'walrus_mainnet', job, text, ns });
  } catch (err) {
    stats.failed++;
    console.warn('[Walrus] Remember failed:', err.message);
    res.json({ success: true, mode: 'local_pending_retry', error: err.message, text, ns });
  }
});

// Recall Memories
app.post('/api/memory/recall', async (req, res) => {
  const { query = 'workflow blockers and habits' } = req.body || {};
  const limit = Math.min(Math.max(Number(req.body?.limit) || 12, 1), 100);
  const ns = req.personalNamespace || NAMESPACE;
  const mw = getMemwal();

  let results = [];
  const start = Date.now();

  const counts = mw ? await namespaceCounts(mw) : null;
  if (mw && (!counts || counts.get(ns) > 0)) {
    try {
      const resp = await mw.recall({ query: String(query).slice(0, 500), limit, namespace: ns });
      results = (resp.results || []).map(item => ({
        text: item.text,
        distance: item.distance,
        blob: item.blob_id,
        at: item.created_at || null,
        source: 'walrus_mainnet',
      }));
    } catch (err) {
      console.warn('[Walrus] Recall failed:', err.message);
    }
    stats.recalls++;
    stats.recallMs += Date.now() - start;
  }

  // Merge recent local pending items not yet indexed on Mainnet
  const pend = (pendingQueue.get(ns) || []).filter(item => Date.now() - item.at < PENDING_WINDOW_MS);
  for (const p of pend) {
    if (!results.some(r => r.text === p.text)) {
      results.push({ text: p.text, distance: 0.25, source: 'pending_indexing' });
    }
  }

  res.json({ results, namespace: ns, count: results.length });
});

// What the namespace's memories mean for each step of a route. Each label gets its
// own semantic recall, so callers send a few labels at a time.
const FRICTION_BATCH_LIMIT = 12;

app.post('/api/memory/friction', async (req, res) => {
  const { labels, fresh, sample } = req.body || {};
  if (!Array.isArray(labels) || !labels.length || labels.length > FRICTION_BATCH_LIMIT) {
    return res.status(400).json({ error: `labels must be an array of 1 to ${FRICTION_BATCH_LIMIT} step names` });
  }
  const clean = labels.map((l) => String(l).slice(0, 200).trim()).filter(Boolean);

  const mw = getMemwal();
  if (!mw) return res.status(503).json({ error: 'Walrus Memory is not configured' });

  try {
    // Personal goals use only your memories. The sample goal also borrows the project's,
    // so a first-time visitor can see memory change a route.
    const scopes = [req.personalNamespace, (sample || !req.personalNamespace) && NAMESPACE].filter(Boolean);
    const counts = await namespaceCounts(mw);
    const expected = counts ? (ns) => counts.get(ns) ?? 0 : null;
    const steps = await frictionForSteps(mw, clean, scopes, { fresh: !!fresh, expected, sampleNamespace: NAMESPACE });
    res.json({ steps, namespaces: scopes });
  } catch (err) {
    console.warn('[Walrus] Friction lookup failed:', err.message);
    res.status(502).json({ error: err.message });
  }
});

// ==========================================
//      WALRUS BLOBS: SHARE, TEMPLATES, CERTS
// ==========================================

// Save a whole board (goal graph) as an immutable snapshot and return a link.
app.post('/api/walrus/snapshot', async (req, res) => {
  const { board, label } = req.body || {};
  if (!board?.nodes) return res.status(400).json({ error: 'A board is required' });
  try {
    const snapshot = { version: 1, kind: 'board', sharedAt: new Date().toISOString(), board };
    const meta = await publishBlob(snapshot, { kind: 'board', label: label || board.title || 'GoalStar board' });
    res.json({ success: true, ...meta, link: `/index.html?board=walrus://${meta.id}` });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Read any published blob back (board, certificate or template).
app.get('/api/walrus/blob/:id', async (req, res) => {
  try {
    const data = await readBlob(req.params.id);
    if (!data) return res.status(404).json({ error: 'That Walrus blob was not found' });
    res.json({ success: true, ...data });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Shared knowledge base: templates published by anyone into a public namespace.
app.get('/api/walrus/templates', (req, res) => {
  const list = readJsonFile(TEMPLATE_FILE, []);
  res.json({ success: true, namespace: 'goalstar-public', count: list.length, templates: list });
});

app.post('/api/walrus/templates', async (req, res) => {
  const { board, author = 'anonymous', tags = '' } = req.body || {};
  if (!board?.nodes) return res.status(400).json({ error: 'A board is required' });
  try {
    const template = {
      version: 1, kind: 'template',
      title: board.title || board.nodes?.[board.goalId]?.label || 'Untitled goal',
      goal: board.nodes?.[board.goalId]?.label || board.title || '',
      start: board.nodes?.[board.startId]?.label || '',
      author: String(author).slice(0, 60),
      tags: String(tags).slice(0, 120),
      addedAt: new Date().toISOString(),
      board,
    };
    const meta = await publishBlob(template, { kind: 'template', namespace: 'goalstar-public', label: template.title });
    const list = readJsonFile(TEMPLATE_FILE, []);
    if (!list.some((t) => t.id === meta.id)) {
      list.unshift({ id: meta.id, title: template.title, goal: template.goal, start: template.start, author: template.author, tags: template.tags, addedAt: template.addedAt, storage: meta.storage });
      writeJsonFile(TEMPLATE_FILE, list.slice(0, 200));
    }
    res.json({ success: true, ...meta, template: template.title });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ==========================================
//      TATUM: LIVE SUI DATA & CERTIFICATES
// ==========================================

const VALID_JOB_ID = /^[\w-]{8,64}$/;

app.get('/api/tatum/sui-status', async (req, res) => {
  res.set('Cache-Control', 'no-store');
  if (!tatum.isConfigured()) return res.status(503).json({ live: false, error: 'TATUM_API_KEY is not set' });
  try {
    const head = await tatum.getChainHead();
    res.json({ live: true, ...head, gateway: tatum.GRPC_HOST, rateLimitRps: tatum.RATE_LIMIT_RPS });
  } catch (err) {
    res.status(502).json({ live: false, error: err.message });
  }
});

// Seal a milestone: anchor it to a live checkpoint, then store it on Walrus.
app.post('/api/tatum/stamp-milestone', async (req, res) => {
  const { milestoneId, milestoneLabel, checklist, goal, deliverables } = req.body || {};
  if (!milestoneLabel) return res.status(400).json({ error: 'Milestone label required' });

  let certificate;
  try {
    certificate = await buildCertificate({ milestoneId, milestoneLabel, goal, checklist, deliverables });
  } catch (err) {
    return res.status(502).json({ success: false, error: `Could not read a live checkpoint from Tatum: ${err.message}` });
  }

  try {
    const blob = await publishBlob(certificate, { kind: 'certificate', label: certificate.milestoneLabel });
    if (!blob.tatumJobId) {
      return res.status(502).json({ success: false, error: 'Tatum storage did not accept the certificate' });
    }
    const { chainAnchor: anchor } = certificate;
    res.json({
      success: true,
      milestoneId,
      milestoneLabel: certificate.milestoneLabel,
      onchainProof: {
        certVersion: CERTIFICATE_VERSION,
        network: 'Sui Mainnet',
        via: 'tatum-grpc',
        checkpoint: anchor.checkpoint,
        checkpointDigest: anchor.digest,
        checkpointTimestampMs: anchor.timestampMs,
        epoch: anchor.epoch,
        sha256: certificate.sha256,
        tatumJobId: blob.tatumJobId,
        status: 'sealing',
        certificateUrl: blob.url,
        verifyUrl: `/api/tatum/verify/${blob.tatumJobId}`,
        shareLink: `/index.html?cert=tatum://${blob.tatumJobId}`,
        timestamp: certificate.completedAt,
      },
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Independently re-check a certificate against Walrus and Sui. A verified result
// cannot change, so it is reused rather than spending the rate limit again.
const verifiedReports = new Map();
app.get('/api/tatum/verify/:jobId', async (req, res) => {
  const { jobId } = req.params;
  if (!VALID_JOB_ID.test(jobId)) return res.status(400).json({ error: 'Invalid job id' });
  if (verifiedReports.has(jobId)) return res.json(verifiedReports.get(jobId));
  try {
    const report = await verifyCertificate(jobId);
    if (report.verdict === 'verified') verifiedReports.set(jobId, report);
    res.json(report);
  } catch (err) {
    res.status(502).json({ verdict: 'incomplete', jobId, checks: [], error: err.message });
  }
});

// Certified milestones, newest first, so anyone can pick one and verify it.
app.get('/api/tatum/certificates', async (req, res) => {
  try {
    const uploads = await tatum.listUploads();
    const certificates = uploads
      .filter((u) => u.status === 'CERTIFIED' && String(u.filename).startsWith('certificate-'))
      .sort((a, b) => b.createdAt - a.createdAt)
      .slice(0, 20)
      .map((u) => ({
        jobId: u.jobId,
        blobId: u.blobId,
        suiObjectId: u.suiObjectId,
        certifiedTxDigest: storageEvent(u, 'certified')?.txDigest || null,
        createdAt: u.createdAt,
      }));
    res.json({ success: true, count: certificates.length, certificates });
  } catch (err) {
    res.status(502).json({ success: false, error: err.message });
  }
});

app.get('/api/tatum/walrus-uploads', async (req, res) => {
  try {
    res.json({ success: true, uploads: await tatum.listUploads() });
  } catch (err) {
    res.status(502).json({ success: false, error: err.message });
  }
});

app.get('/api/tatum/walrus-status/:jobId', async (req, res) => {
  if (!VALID_JOB_ID.test(req.params.jobId)) return res.status(400).json({ error: 'Invalid job id' });
  try {
    res.json({ success: true, status: await tatum.getUpload(req.params.jobId) });
  } catch (err) {
    res.status(502).json({ success: false, error: err.message });
  }
});

// ==========================================
//        PLANNING AGENT (path editing chat)
// ==========================================
const AGENT_MODEL = process.env.GROQ_MODEL || 'openai/gpt-oss-120b';
const AGENT_OPS = new Set([
  'rename_state', 'rename_action', 'set_done',
  'remove_state', 'remove_action', 'relink_action', 'replan', 'block_state',
  'add_branch',
]);

const AGENT_SYSTEM = `You are the planning agent inside GoalStar, an autonomous system that treats a life goal as an A* graph. STATES are milestones (conditions that become true); ACTIONS are the steps connecting them.

You have access to Walrus Decentralized Memory (which stores past user friction and stamina patterns across sessions) to guide decisions.

The user asks for edits in plain English. Translate the request into a list of operations, answering with ONLY this JSON shape:
{"reply":"one or two short sentences describing what you changed and which Walrus memory guided you","ops":[
  {"type":"rename_state","id":"n_...","label":"new milestone label"},
  {"type":"rename_action","id":"e_...","label":"new action label"},
  {"type":"set_done","id":"n_...","done":true},
  {"type":"remove_state","id":"n_..."},
  {"type":"remove_action","id":"e_..."},
  {"type":"relink_action","id":"e_...","to":"n_..."},
  {"type":"replan","id":"n_..."},
  {"type":"block_state","id":"n_...","level":"expensive"|"impossible","reason":"why it is out of reach"},
  {"type":"add_branch","fromId":"n_...","toId":"n_...","branches":[
    {"milestone":"Milestone A condition","note":"Strategy A details","actionIn":"Action into A","actionOut":"Action from A to destination","duration":"1 week","time":2,"money":1,"effort":2,"risk":1},
    {"milestone":"Milestone B condition","note":"Strategy B details","actionIn":"Action into B","actionOut":"Action from B to destination","duration":"4 days","time":1,"money":3,"effort":1,"risk":1}
  ]}
]}

Rules:
- CONTEXTUAL TARGETING: If the user makes a vague request like "add more paths here", "branch here", "give me more routes here", or says "here", the target milestone is the focused/last-clicked milestone specified in the plan. Do not ask for clarification; immediately expand from that target milestone.
- BRANCHING QUALITY: When asked for more branches/paths, NEVER be lazy and create just one lonely node. Always create multiple (at least 2) distinct parallel alternatives.
- MANDATORY RECONNECTION: Every new branch MUST connect back to a downstream milestone or to the GOAL node (via actionOut and toId). Never leave any newly created branch disconnected or floating as an unreached leaf node!
- WALRUS MEMORY INTEGRATION: Take into account the recalled Walrus memories. If past memory indicates high friction or blockers on certain tasks, route around them or propose lower-friction alternatives.
- Milesone labels are phrased as achieved conditions ("Specs finalized", "Database provisioned"), not tasks; action labels are imperative steps.
- Use an empty ops array when the request is a question, and just answer in reply.`;

function sanitizeAgentOps(ops) {
  return (Array.isArray(ops) ? ops : []).slice(0, 16)
    .map((o) => ({
      type: String(o?.type || '').slice(0, 40),
      id: String(o?.id || o?.fromId || '').slice(0, 80),
      fromId: String(o?.fromId || o?.id || '').slice(0, 80),
      toId: String(o?.toId || o?.to || '').slice(0, 80),
      to: String(o?.to || o?.toId || '').slice(0, 80),
      label: String(o?.label || '').slice(0, 160),
      done: o?.done !== false,
      level: String(o?.level || '').slice(0, 20),
      reason: String(o?.reason || '').slice(0, 160),
      branches: Array.isArray(o?.branches) ? o.branches.slice(0, 6) : undefined,
    }))
    .filter((o) => AGENT_OPS.has(o.type) && (o.id || o.fromId));
}

app.post('/api/agent/chat', async (req, res) => {
  const { message, board } = req.body || {};
  const text = String(message || '').trim();
  if (!text) return res.status(400).json({ error: 'Tell the agent what to change' });
  if (!board?.nodes?.length) return res.status(400).json({ error: 'No open goal to edit' });

  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) {
    return res.status(503).json({ error: 'The edit agent needs GROQ_API_KEY in .env (see .env.example)' });
  }

  // Actively recall from Walrus Decentralized Memory
  let walrusInsights = [];
  const mw = getMemwal();
  const ns = req.personalNamespace || NAMESPACE;
  if (mw) {
    try {
      const resp = await mw.recall({ query: `${text} ${board.goal?.label || ''}`, limit: 5, namespace: ns });
      walrusInsights = (resp.results || []).map(r => r.text);
    } catch (e) {
      console.warn('[Walrus agent recall failed]:', e.message);
    }
  }
  if (!walrusInsights.length) {
    try {
      if (fs.existsSync(LOG_FILE)) {
        const lines = fs.readFileSync(LOG_FILE, 'utf8').trim().split('\n').filter(Boolean);
        walrusInsights = lines.map(l => {
          try { return JSON.parse(l); } catch { return null; }
        }).filter(l => l?.ns === ns).slice(-4).map(l => l.text);
      }
    } catch (e) {}
  }

  const targetNodeId = board.targetNodeId || (board.nodes?.[0]?.id);
  const targetNodeLabel = board.targetNodeLabel || (board.nodes?.[0]?.label);

  const plan = {
    goal: board.goal,
    start: board.start,
    focusedTargetMilestone: targetNodeId ? `${targetNodeId} ("${targetNodeLabel}")` : 'none',
    constraints: board.constraints || '',
    timeframe: board.timeframe || '',
    budget: board.budget || '',
    walrusRecalledMemories: walrusInsights.length ? walrusInsights : ['No past roadblocks logged yet.'],
    states: (board.nodes || []).map((n) => `${n.id} | ${n.kind} | ${n.done ? 'done' : 'open'}${n.blocked ? ` | ${n.blocked.level}` : ''} | ${n.label}`),
    actions: (board.edges || []).map((e) => `${e.id} | ${e.fromLabel} -> ${e.toLabel} | ${e.label}${e.steps?.length ? ` | steps: ${e.steps.join(' / ')}` : ''}`),
    bestPath: (board.bestPath || []).join(' -> '),
  };

  try {
    const upstream = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
      body: JSON.stringify({
        model: AGENT_MODEL,
        temperature: 0.2,
        max_completion_tokens: 2048,
        response_format: { type: 'json_object' },
        messages: [
          { role: 'system', content: `${AGENT_SYSTEM}\n\nCurrent plan:\n${JSON.stringify(plan, null, 1)}` },
          { role: 'user', content: text },
        ],
      }),
    });

    if (!upstream.ok) {
      let detail = `${upstream.status}`;
      try { detail += ` ${(await upstream.json()).error?.message || ''}`; } catch { /* keep status */ }
      const status = upstream.status === 429 ? 429 : 502;
      return res.status(status).json({ error: `Agent unavailable (${detail.trim()})` });
    }

    const payload = await upstream.json();
    const raw = payload.choices?.[0]?.message?.content || '{}';
    let parsed;
    try { parsed = JSON.parse(raw); } catch { parsed = null; }
    if (!parsed) return res.status(502).json({ error: 'Agent replied with something that was not JSON' });

    res.json({
      reply: String(parsed.reply || '').slice(0, 800) || 'Applied your edit.',
      ops: sanitizeAgentOps(parsed.ops),
      walrus: {
        active: true,
        recalls: walrusInsights.slice(0, 3),
      },
    });
  } catch (err) {
    console.warn('[Agent] chat failed:', err.message);
    res.status(502).json({ error: `Agent unreachable (${err.message})` });
  }
});

// Start Server
if (!process.env.VERCEL) {
  app.listen(PORT, '0.0.0.0', () => {
  console.log(`\n======================================================`);
  console.log(`GoalStar Total Recall Edition running at:`);
  console.log(`   http://localhost:${PORT}`);
  console.log(`   Walrus Mainnet Memory: Active`);
  console.log(`   Tatum Sui gRPC Gateway: ${tatum.GRPC_HOST}`);
  console.log(`   Rate Limiting: ${tatum.RATE_LIMIT_RPS} requests/sec (Tatum Free Tier)`);
  console.log(`======================================================\n`);
  getMemwal();
});
}


export default app;
