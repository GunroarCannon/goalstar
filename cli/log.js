#!/usr/bin/env node
// GoalStar Portable Memory CLI
// Allows logging habit progress and blockers directly to Walrus Mainnet from any terminal or tool session.

import 'dotenv/config';

const API_BASE = process.env.API_BASE || 'http://localhost:8000';
const args = process.argv.slice(2);

async function main() {
  if (args.includes('--status')) {
    const res = await fetch(`${API_BASE}/api/memory/stats`);
    const json = await res.json();
    console.log('\n[Walrus Portable Memory Status]');
    console.log(`- Enabled: ${json.enabled}`);
    console.log(`- Account ID: ${json.accountId}`);
    console.log(`- Namespace: ${json.namespace}`);
    console.log(`- Memories Written: ${json.written}`);
    console.log(`- Recalls: ${json.recalls} (avg ${json.avgRecallMs}ms)\n`);
    return;
  }

  if (args.includes('--sui')) {
    const res = await fetch(`${API_BASE}/api/tatum/sui-status`);
    const json = await res.json();
    console.log('\n[Tatum Sui RPC Gateway]');
    console.log(`- Latest Checkpoint: ${json.checkpoint}`);
    console.log(`- Chain ID: ${json.chainId}`);
    console.log(`- Reference Gas: ${json.referenceGasPriceMIST} MIST`);
    console.log(`- Gateway: ${json.gateway}\n`);
    return;
  }

  if (args.includes('--storage')) {
    const res = await fetch(`${API_BASE}/api/tatum/walrus-uploads`);
    const json = await res.json();
    console.log('\n[Tatum Walrus Storage API (/v4/data/storage/uploads)]');
    if (json.uploads && Array.isArray(json.uploads)) {
      console.log(`- Total Uploads: ${json.uploads.length}`);
      json.uploads.slice(0, 5).forEach((u, i) => {
        console.log(`  ${i + 1}. Job ${u.jobId} | ${u.filename || 'blob'} | Status: ${u.status || 'N/A'} | Blob: ${u.blobId || 'N/A'}`);
      });
    } else {
      console.log(`- Status:`, json);
    }
    console.log('');
    return;
  }

  if (args.includes('--seed')) {
    console.log('\nSeeding 10 workflow memories to Walrus Mainnet...');
    const res = await fetch(`${API_BASE}/api/memory/seed`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const json = await res.json();
    console.log(`✓ Seeded ${json.count} memories. Mode: ${json.mode}\n`);
    return;
  }

  const text = args.join(' ').trim();
  if (!text) {
    console.log(`
Usage:
  node cli/log.js "Your habit update or blocker description"
  node cli/log.js --status      Check Walrus Memory statistics
  node cli/log.js --sui         Check Tatum Sui RPC connection
  node cli/log.js --storage     Check Tatum Walrus Storage API uploads
  node cli/log.js --seed        Pre-populate 10 memories on Mainnet
`);
    return;
  }

  console.log(`\nLogging to Walrus Memory on Mainnet: "${text}"...`);
  try {
    const res = await fetch(`${API_BASE}/api/memory/remember`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, category: 'cli_update' })
    });
    const json = await res.json();
    console.log(`✓ Stored successfully! (Mode: ${json.mode})`);
    console.log(`[Note] Next time you open GoalStar, the workflow agent will pick up where you left off!\n`);
  } catch (err) {
    console.error(`Error logging memory:`, err.message);
  }
}

main();
