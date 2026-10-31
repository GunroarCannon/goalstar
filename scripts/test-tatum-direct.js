const key = process.env.TATUM_API_KEY;

async function test() {
  console.log('Sending JSON-RPC request to https://sui-mainnet.gateway.tatum.io with key:', key.slice(0, 8) + '...');
  
  const payload = {
    jsonrpc: '2.0',
    id: 1,
    method: 'sui_getLatestCheckpointSequenceNumber',
    params: []
  };

  const res = await fetch('https://sui-mainnet.gateway.tatum.io', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'x-api-key': key
    },
    body: JSON.stringify(payload)
  });

  console.log('Status:', res.status, res.statusText);
  console.log('Plan header:', res.headers.get('x-ttm-plan'));
  const text = await res.text();
  console.log('Body:', text);
}

test();
