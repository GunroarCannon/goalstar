// Server-side client for Tatum's Sui gRPC gateway and Walrus storage API.
//
// Sui deprecated JSON-RPC, so chain reads go over native gRPC. Every function
// either returns real data from Tatum or throws. There is deliberately no
// public-node fallback and no placeholder value: a certificate must never carry
// anything that did not come from the chain.

import grpc from '@grpc/grpc-js';
import { GrpcTransport } from '@protobuf-ts/grpc-transport';
import { SuiGrpcClient } from '@mysten/sui/grpc';

export const GRPC_HOST = process.env.TATUM_SUI_GRPC_HOST || 'sui-mainnet-grpc.gateway.tatum.io:443';
const STORAGE_API = 'https://api.tatum.io/v4/data/storage';
const CALL_TIMEOUT_MS = 15000;
const HEAD_CACHE_MS = 4000;
export const RATE_LIMIT_RPS = 3; // Tatum free plan

export const isConfigured = () => !!process.env.TATUM_API_KEY;

function requireKey() {
  if (!process.env.TATUM_API_KEY) throw new Error('TATUM_API_KEY is not set');
  return process.env.TATUM_API_KEY;
}

// ---- Rate limiting: a shared sliding window across gRPC and storage calls ----
let recentCalls = [];
async function acquireSlot() {
  for (;;) {
    const now = Date.now();
    recentCalls = recentCalls.filter((t) => now - t < 1000);
    if (recentCalls.length < RATE_LIMIT_RPS) {
      recentCalls.push(now);
      return;
    }
    await new Promise((resolve) => setTimeout(resolve, 1000 - (now - recentCalls[0]) + 10));
  }
}

let client = null;
function sui() {
  if (!client) {
    client = new SuiGrpcClient({
      network: 'mainnet',
      transport: new GrpcTransport({
        host: GRPC_HOST,
        channelCredentials: grpc.credentials.createSsl(),
        meta: { 'x-api-key': requireKey() },
        timeout: CALL_TIMEOUT_MS,
      }),
    });
  }
  return client;
}

async function ledger(method, request) {
  requireKey();
  await acquireSlot();
  const { response } = await sui().ledgerService[method](request);
  return response;
}

const timestampMs = (t) => (t ? Number(t.seconds) * 1000 + Math.floor((t.nanos || 0) / 1e6) : null);

// Protobuf Struct values arrive as { kind: { oneofKind, ... } }; flatten to JSON.
function unwrapValue(value) {
  const kind = value?.kind;
  switch (kind?.oneofKind) {
    case 'structValue':
      return Object.fromEntries(Object.entries(kind.structValue.fields).map(([k, v]) => [k, unwrapValue(v)]));
    case 'listValue':
      return kind.listValue.values.map(unwrapValue);
    case 'nullValue':
    case undefined:
      return null;
    default:
      return kind[kind.oneofKind];
  }
}

// ---- Sui reads ----

export async function getCheckpoint(sequence) {
  const { checkpoint } = await ledger('getCheckpoint', {
    checkpointId: { oneofKind: 'sequenceNumber', sequenceNumber: BigInt(sequence) },
    readMask: { paths: ['sequence_number', 'digest', 'summary.timestamp', 'summary.epoch'] },
  });
  return {
    sequence: String(checkpoint.sequenceNumber),
    digest: checkpoint.digest,
    timestampMs: timestampMs(checkpoint.summary?.timestamp),
    epoch: checkpoint.summary?.epoch != null ? String(checkpoint.summary.epoch) : null,
  };
}

async function fetchChainHead() {
  const started = Date.now();
  const info = await ledger('getServiceInfo', {});
  const checkpoint = await getCheckpoint(info.checkpointHeight);
  return {
    network: info.chain,
    chainId: info.chainId,
    epoch: String(info.epoch),
    checkpoint: checkpoint.sequence,
    digest: checkpoint.digest,
    timestampMs: checkpoint.timestampMs,
    node: info.server,
    latencyMs: Date.now() - started,
    via: 'tatum-grpc',
  };
}

// Many page views share one upstream read, which keeps us inside the rate limit.
let headCache = null;
let headInFlight = null;
export function getChainHead({ fresh = false } = {}) {
  if (!fresh && headCache && Date.now() - headCache.at < HEAD_CACHE_MS) return Promise.resolve(headCache.head);
  if (headInFlight) return headInFlight;
  headInFlight = fetchChainHead()
    .then((head) => {
      headCache = { head, at: Date.now() };
      return head;
    })
    .finally(() => { headInFlight = null; });
  return headInFlight;
}

export async function getTransaction(digest) {
  const { transaction } = await ledger('getTransaction', {
    digest,
    readMask: { paths: ['digest', 'checkpoint', 'timestamp', 'effects.status'] },
  });
  return {
    digest: transaction.digest,
    success: transaction.effects?.status?.success === true,
    checkpoint: transaction.checkpoint != null ? String(transaction.checkpoint) : null,
    timestampMs: timestampMs(transaction.timestamp),
  };
}

export async function getObject(objectId) {
  const { object } = await ledger('getObject', {
    objectId,
    readMask: { paths: ['object_id', 'version', 'object_type', 'owner', 'json'] },
  });
  return {
    objectId: object.objectId,
    version: String(object.version),
    type: object.objectType,
    owner: object.owner?.address || null,
    fields: unwrapValue(object.json),
  };
}

// ---- Walrus storage through Tatum ----

async function storageRequest(path, init = {}) {
  const key = requireKey();
  await acquireSlot();
  const res = await fetch(`${STORAGE_API}${path}`, {
    ...init,
    headers: { ...init.headers, 'x-api-key': key },
    signal: AbortSignal.timeout(CALL_TIMEOUT_MS * 2),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Tatum storage responded ${res.status}: ${text.slice(0, 200)}`);
  return JSON.parse(text);
}

export function uploadJson(json, filename) {
  const form = new FormData();
  form.append('file', new Blob([json], { type: 'application/json' }), filename);
  return storageRequest('/upload', { method: 'POST', body: form });
}

export const getUpload = (jobId) => storageRequest(`/upload/${encodeURIComponent(jobId)}`);
export const listUploads = () => storageRequest('/uploads');
