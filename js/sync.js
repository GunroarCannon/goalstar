// Cloud sync via a secret GitHub Gist: free, no expiry, versioned.
// Needs a GitHub token with only the "gist" scope. Secrets (API keys, the token) are never uploaded.

const API = 'https://api.github.com/gists';
const FILE = 'goalstar.json';

const headers = (token) => ({
  Authorization: `Bearer ${token}`,
  Accept: 'application/vnd.github+json',
  'Content-Type': 'application/json',
});

async function check(res) {
  if (res.ok) return res.json();
  const msg = res.status === 401 ? 'bad token' : res.status === 404 ? 'gist not found' : `GitHub ${res.status}`;
  throw new Error(msg);
}

export async function pull({ token, id }) {
  const g = await check(await fetch(`${API}/${id}`, { headers: headers(token) }));
  const f = g.files?.[FILE];
  if (!f) return null;
  const text = f.truncated ? await (await fetch(f.raw_url)).text() : f.content;
  return JSON.parse(text);
}

export async function push({ token, id }, payload) {
  const body = JSON.stringify({
    description: 'goalstar data',
    ...(id ? {} : { public: false }),
    files: { [FILE]: { content: JSON.stringify(payload, null, 1) } },
  });
  const g = await check(await fetch(id ? `${API}/${id}` : API, { method: id ? 'PATCH' : 'POST', headers: headers(token), body }));
  return g.id;
}

// Newest copy of each board wins; deletions are kept as tombstones.
export function mergeData(local, remote) {
  const deleted = { ...(remote.deleted || {}), ...local.deleted };
  for (const [id, t] of Object.entries(remote.deleted || {})) deleted[id] = Math.max(t, local.deleted[id] || 0);
  const boards = {};
  for (const src of [remote.boards || {}, local.boards]) {
    for (const b of Object.values(src)) {
      if (deleted[b.id] && deleted[b.id] >= (b.updated || 0)) continue;
      if (!boards[b.id] || (b.updated || 0) > (boards[b.id].updated || 0)) boards[b.id] = b;
    }
  }
  return { boards, deleted };
}
