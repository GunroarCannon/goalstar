// Walrus Memory Frontend Bridge
// Connects GoalStar UI with the Walrus Memory on Mainnet relayer via /api/memory

export class WalrusMemoryBridge {
  constructor(apiBase = '') {
    this.apiBase = apiBase;
    this.memories = [];
    this.stats = { enabled: false, written: 0, recalls: 0 };
    this.listeners = new Set();
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
      const res = await fetch(`${this.apiBase}/api/memory/stats`);
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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

  async seedTenMemories() {
    try {
      const res = await fetch(`${this.apiBase}/api/memory/seed`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      if (res.ok) {
        const data = await res.json();
        await this.recall();
        await this.checkStatus();
        return data;
      }
    } catch (err) {
      console.warn('Seed failed:', err);
    }
    return null;
  }

  /**
   * Calculates dynamic friction penalty based on text matching against recalled Walrus memories.
   * If a step label matches a recalled blocker (e.g. 'docker', 'devops', 'admin', 'writing'),
   * returns a penalty (e.g. +2.0 to +4.0) that directly modulates the A* path.
   */
  getFrictionPenalty(edgeLabel = '') {
    if (!this.memories.length) return 0;
    const lower = edgeLabel.toLowerCase();

    let penalty = 0;
    for (const m of this.memories) {
      const mText = (m.text || '').toLowerCase();
      
      // Kubernetes / Docker / DevOps blocker
      if ((lower.includes('docker') || lower.includes('devops') || lower.includes('kubernetes') || lower.includes('cluster')) &&
          (mText.includes('docker') || mText.includes('kubernetes') || mText.includes('devops'))) {
        penalty = Math.max(penalty, 3.5);
      }
      
      // Admin / Email / Documentation procrastination
      if ((lower.includes('email') || lower.includes('documentation') || lower.includes('cold') || lower.includes('pitch')) &&
          (mText.includes('documentation') || mText.includes('outreach') || mText.includes('anxiety'))) {
        penalty = Math.max(penalty, 2.5);
      }

      // Late night / high cognitive fatigue
      if (lower.includes('deep focus') && mText.includes('fatigue')) {
        penalty = Math.max(penalty, 2.0);
      }
    }

    return penalty;
  }
}

export const walrusMemory = new WalrusMemoryBridge();
