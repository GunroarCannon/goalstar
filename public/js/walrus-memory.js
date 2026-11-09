// Walrus Memory Frontend Bridge
// Connects GoalStar UI with the Walrus Memory on Mainnet relayer via /api/memory

const FRICTION_BATCH = 6;
// Looser than route costs: a whole goal is broader than one step, and the planner
// weighs what it's given. Unrelated goals measured 0.83 and up.
const PLANNING_RELEVANCE = 0.8;

export class WalrusMemoryBridge {
  constructor(apiBase = '') {
    this.apiBase = apiBase;
    this.memories = [];
    this.friction = new Map(); // step label -> { penalty, because }
    this.getMemoryId = () => null;
    this.stats = { enabled: false, written: 0, recalls: 0 };
    this.listeners = new Set();
  }

  identityHeaders() {
    const id = this.getMemoryId();
    return id ? { 'X-GoalStar-Memory': id } : {};
  }

  subscribe(fn) {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  }

  notify() {
    for (const fn of this.listeners) {
      try { fn(this); } catch (e) { console.error(e); }
    }
  }

  async checkStatus() {
    try {
      const res = await fetch(`${this.apiBase}/api/memory/stats`, { headers: this.identityHeaders() });
      if (res.ok) {
        this.stats = await res.json();
        this.notify();
      }
    } catch (err) {
      console.warn('Memory stats check failed:', err);
    }
    return this.stats;
  }

  async recall(query = 'habits and blockers', limit = 10) {
    try {
      const res = await fetch(`${this.apiBase}/api/memory/recall`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...this.identityHeaders() },
        body: JSON.stringify({ query, limit })
      });
      if (res.ok) {
        const data = await res.json();
        this.memories = data.results || [];
        this.notify();
        return this.memories;
      }
    } catch (err) {
      console.warn('Memory recall failed:', err);
    }
    return [];
  }

  async remember(text, category = 'habit', friction = 0) {
    try {
      const res = await fetch(`${this.apiBase}/api/memory/remember`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...this.identityHeaders() },
        body: JSON.stringify({ text, category, friction })
      });
      if (res.ok) {
        const data = await res.json();
        await this.checkStatus();
        return data;
      }
    } catch (err) {
      console.warn('Remember failed:', err);
    }
    return null;
  }

  // Memories relevant to a goal, as plain text for the planner. Planning must never
  // hang on memory, so this gives up after a few seconds.
  async recallForPlanning(query) {
    try {
      const res = await fetch(`${this.apiBase}/api/memory/recall`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...this.identityHeaders() },
        body: JSON.stringify({ query, limit: 12 }),
        signal: AbortSignal.timeout(8000),
      });
      if (!res.ok) return [];
      const { results } = await res.json();
      return results
        .filter((m) => m.distance < PLANNING_RELEVANCE && !/^\s*\[BLOB /.test(m.text))
        .slice(0, 6)
        .map((m) => m.text.slice(0, 240));
    } catch (err) {
      console.warn('Planning recall failed:', err);
      return [];
    }
  }

  // Asks Walrus what the namespace's memories mean for each step, a few steps at a
  // time so a large board never holds one long request open. Keeps prior answers if
  // Walrus is unreachable, and reports whether any step's cost changed.
  async loadFriction(labels, { fresh = false, sample = false, onBatch = null } = {}) {
    const unique = [...new Set(labels.filter(Boolean))];
    let changed = false;
    for (let i = 0; i < unique.length; i += FRICTION_BATCH) {
      const batch = unique.slice(i, i + FRICTION_BATCH);
      try {
        const res = await fetch(`${this.apiBase}/api/memory/friction`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', ...this.identityHeaders() },
          body: JSON.stringify({ labels: batch, fresh, sample }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const { steps } = await res.json();
        let batchChanged = false;
        for (const [label, value] of Object.entries(steps)) {
          if (this.getFrictionPenalty(label) !== value.penalty) batchChanged = true;
          this.friction.set(label, value);
        }
        if (batchChanged) {
          changed = true;
          onBatch?.();
        }
      } catch (err) {
        console.warn('Friction lookup failed:', err);
      }
    }
    return changed;
  }

  getFrictionPenalty(label = '') {
    return this.friction.get(label)?.penalty || 0;
  }

  explainFriction(label = '') {
    return this.friction.get(label)?.because || null;
  }
}

export const walrusMemory = new WalrusMemoryBridge();
