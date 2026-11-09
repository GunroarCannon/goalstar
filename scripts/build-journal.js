// Writes GoalStar's own build journal to Walrus Memory on Mainnet: things that
// actually went wrong or right while building this project, in the same free-text
// form a user would log from the CLI. Entries already stored are skipped.
//
//   npm run journal            write any entries not yet on Walrus
//   npm run journal -- --force write every entry again (e.g. under a new delegate key)
import 'dotenv/config';
import { MemWal } from '@mysten-incubation/memwal';

const NAMESPACE = process.env.MEMWAL_NAMESPACE || 'goalstar-workflows';

export const JOURNAL = [
  "Blocked on the Sui integration: Tatum's Sui JSON-RPC URL returned 404 on every call, and the public fallback answered 'Method not found' because Sui has deprecated JSON-RPC. Certificates silently fell back to placeholder data and we lost a long debugging session finding out.",
  "Moving Sui reads to Tatum's native gRPC gateway worked: real checkpoints, digests and epochs came back live and the certificate flow finally ran on real chain data.",
  "gRPC-web transport failed against the Tatum gateway with 'unexpected response content type: application/grpc'. The fix was the native @grpc/grpc-js transport.",
  "Tatum Storage API uploads to Walrus certify asynchronously, about a minute after upload. Polling the job from the client went smoothly; never block a single request on certification.",
  "Reading a Tatum-stored file by blob id returned the raw 445 KB quilt instead of the file, which broke hash verification until we read it by quilt patch id.",
  "Anchoring certificates to a live checkpoint digest and letting Walrus certify them worked well: no funded wallet and no transaction signing needed, and all six verification checks passed on Mainnet.",
  "Sharing one sliding-window rate limiter across every Tatum call kept the app inside the 3 requests per second free tier during the integration runs.",
  "Hardcoded keyword matching for route friction failed silently: it returned a zero penalty for almost every real memory, so the learning loop looked alive but changed nothing.",
  "Landing page layering was a repeated time sink: cloud placement took several commits, and the mist layer ended up covering the hero headline because of its z-index.",
  "An inline script in index.html with two duplicated lines threw 'Unexpected token function' and killed the avatar picker and toggles. One syntax error in an inline script takes down everything after it.",
  "Vercel static serving broke several times before assets moved into a dedicated public/ directory, and every front-end edit now has to be mirrored there.",
  "Vercel serverless /tmp is not durable, so anything that must survive between requests has to live on Walrus rather than in local files.",
  "A real private key pasted into the README got committed to git. Docs must only ever show placeholders, and the key had to be rotated.",
];

async function main() {
  const mw = MemWal.create({
    key: process.env.MEMWAL_PRIVATE_KEY,
    accountId: process.env.MEMWAL_ACCOUNT_ID,
    serverUrl: process.env.MEMWAL_SERVER_URL || 'https://relayer.memory.walrus.xyz',
    namespace: NAMESPACE,
  });

  let stored = new Set();
  if (!process.argv.includes('--force')) {
    const existing = await mw.recall({ query: JOURNAL[0], limit: 100, namespace: NAMESPACE });
    stored = new Set(existing.results.map((r) => r.text));
  }

  let written = 0;
  for (const text of JOURNAL) {
    if (stored.has(text)) {
      console.log(`skip   ${text.slice(0, 70)}`);
      continue;
    }
    const job = await mw.rememberAndWait(text, NAMESPACE);
    written++;
    console.log(`stored ${String(job.blob_id || job.blobId || '').slice(0, 14)}  ${text.slice(0, 70)}`);
  }
  console.log(`\n${written} written, ${JOURNAL.length - written} already on Walrus (namespace ${NAMESPACE}).`);
}

if (import.meta.url === `file://${process.argv[1].replace(/\\/g, '/')}` || import.meta.url === `file:///${process.argv[1].replace(/\\/g, '/')}`) {
  main().then(() => process.exit(0), (err) => { console.error(err.message); process.exit(1); });
}
