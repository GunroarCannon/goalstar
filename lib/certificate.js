// Milestone certificates, and the independent check that proves one is genuine.
//
// A certificate is a JSON file that embeds the digest of a live Sui checkpoint,
// stored on Walrus through Tatum. Walrus then certifies the blob in a Sui
// transaction. Those two chain facts bound when the certificate was created:
//   - it cannot predate the anchor checkpoint, whose digest was unknowable earlier
//   - it cannot postdate the transaction that certified the blob
//
// verifyCertificate re-derives every claim from Tatum and Walrus. It does not
// trust anything this server stored at sealing time.

import crypto from 'node:crypto';
import * as tatum from './tatum.js';

export const CERTIFICATE_VERSION = 2;

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map((k) => [k, canonicalize(value[k])]));
  }
  return value;
}

const hashBody = (body) => crypto.createHash('sha256').update(JSON.stringify(canonicalize(body))).digest('hex');

export async function buildCertificate({ milestoneId, milestoneLabel, goal, checklist, deliverables }) {
  const head = await tatum.getChainHead({ fresh: true });
  const body = {
    kind: 'certificate',
    version: CERTIFICATE_VERSION,
    milestoneId: milestoneId ?? null,
    milestoneLabel: String(milestoneLabel).slice(0, 200),
    goal: String(goal || '').slice(0, 200),
    completedAt: new Date().toISOString(),
    checklist: Array.isArray(checklist) ? checklist.slice(0, 40).map((s) => String(s).slice(0, 300)) : [],
    deliverables: String(deliverables || '').slice(0, 4000),
    chainAnchor: {
      network: head.network,
      chainId: head.chainId,
      epoch: head.epoch,
      checkpoint: head.checkpoint,
      digest: head.digest,
      timestampMs: head.timestampMs,
    },
  };
  return { ...body, sha256: hashBody(body) };
}

// Walrus encodes a blob id as URL-safe base64 of a little-endian 256-bit integer;
// the Sui Blob object stores that same integer in decimal.
function blobIdToU256(blobId) {
  const bytes = Buffer.from(blobId, 'base64url');
  return BigInt(`0x${Buffer.from(bytes).reverse().toString('hex')}`).toString();
}

const scan = (type, id) => `https://suiscan.xyz/mainnet/${type}/${id}`;

async function fetchWalrusJson(url) {
  const res = await fetch(url, { signal: AbortSignal.timeout(20000) });
  if (!res.ok) throw new Error(`Walrus aggregator responded ${res.status}`);
  return res.json();
}

export function storageEvent(job, type) {
  return (job.storageEvents || []).find((event) => event.type === type) || null;
}

export async function verifyCertificate(jobId) {
  const checks = [];
  const add = (id, label, status, detail, link) => {
    checks.push({ id, label, status, detail, ...(link ? { link } : {}) });
    return status;
  };
  const result = (verdict, extra = {}) => ({ verdict, jobId, checks, ...extra });

  const job = await tatum.getUpload(jobId);
  if (job.status !== 'CERTIFIED') {
    add('stored', 'Certified on Walrus', 'pending', `Tatum storage job is ${job.status}`);
    return result('pending', { jobStatus: job.status });
  }
  add('stored', 'Certified on Walrus', 'pass', `Blob ${job.blobId}, stored through epoch ${job.walrusEndEpoch}`);

  // Each remaining check runs even if an earlier one fails, so the report is complete.
  const attempt = async (id, label, fn) => {
    try {
      return await fn();
    } catch (err) {
      add(id, label, 'unavailable', err.message);
      return null;
    }
  };

  const certifiedEvent = storageEvent(job, 'certified');
  const certifiedTx = await attempt('certifiedTx', 'Sui transaction succeeded', async () => {
    if (!certifiedEvent) throw new Error('Tatum reported no certified event for this job');
    const tx = await tatum.getTransaction(certifiedEvent.txDigest);
    add('certifiedTx', 'Sui transaction succeeded', tx.success ? 'pass' : 'fail',
      `${tx.digest} in checkpoint #${tx.checkpoint}`, scan('tx', tx.digest));
    return tx;
  });

  await attempt('blobObject', 'Sui object matches this blob', async () => {
    const object = await tatum.getObject(job.suiObjectId);
    const isBlob = /::blob::Blob$/.test(object.type || '');
    const matches = object.fields?.blob_id === blobIdToU256(job.blobId);
    const certifiedEpoch = object.fields?.certified_epoch;
    add('blobObject', 'Sui object matches this blob',
      isBlob && matches && certifiedEpoch != null ? 'pass' : 'fail',
      `${object.objectId}, certified in Walrus epoch ${certifiedEpoch}`, scan('object', object.objectId));
  });

  const certificate = await attempt('content', 'Certificate content is intact', async () => {
    const cert = await fetchWalrusJson(job.downloadUrlByQuiltPatchId);
    const { sha256, ...body } = cert;
    add('content', 'Certificate content is intact', sha256 && sha256 === hashBody(body) ? 'pass' : 'fail',
      `SHA-256 ${hashBody(body)}, recomputed from the bytes on Walrus`);
    return cert;
  });

  const anchor = certificate?.chainAnchor;
  const anchorCheckpoint = await attempt('anchor', 'Anchor checkpoint matches Sui', async () => {
    if (!anchor) throw new Error('Certificate has no chain anchor');
    const live = await tatum.getCheckpoint(anchor.checkpoint);
    add('anchor', 'Anchor checkpoint matches Sui', live.digest === anchor.digest ? 'pass' : 'fail',
      `#${live.sequence} has digest ${live.digest}`, scan('checkpoint', live.sequence));
    return live;
  });

  let window = null;
  if (anchorCheckpoint && certifiedTx) {
    const ordered = anchorCheckpoint.timestampMs <= certifiedTx.timestampMs;
    add('ordering', 'Timeline is consistent', ordered ? 'pass' : 'fail',
      'The anchor checkpoint comes before the certifying transaction');
    if (ordered) window = { notBefore: anchorCheckpoint.timestampMs, notAfter: certifiedTx.timestampMs };
  }

  const statuses = checks.map((c) => c.status);
  const verdict = statuses.includes('fail') ? 'failed' : statuses.includes('unavailable') ? 'incomplete' : 'verified';
  return result(verdict, {
    window,
    certificate,
    blobId: job.blobId,
    suiObjectId: job.suiObjectId,
    certifiedTxDigest: certifiedEvent?.txDigest || null,
    walrusUrl: job.downloadUrlByQuiltPatchId,
  });
}
