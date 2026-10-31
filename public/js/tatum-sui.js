// Tatum Sui RPC Frontend Bridge
// Connects GoalStar UI with Tatum Sui Gateway for onchain milestone verification

export class TatumSuiBridge {
  constructor(apiBase = '') {
    this.apiBase = apiBase;
    this.status = null;
    this.listeners = new Set();
  }

  subscribe(fn) {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  }

  notify() {
    for (const fn of this.listeners) {
      try { fn(this.status); } catch (e) { console.error(e); }
    }
  }

  async checkStatus() {
    try {
      const res = await fetch(`${this.apiBase}/api/tatum/sui-status`);
      if (res.ok) {
        this.status = await res.json();
        this.notify();
        return this.status;
      }
    } catch (err) {
      console.warn('Tatum Sui check failed:', err);
    }
    return null;
  }

  async stampMilestone(milestoneId, milestoneLabel, extra = {}) {
    try {
      const res = await fetch(`${this.apiBase}/api/tatum/stamp-milestone`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ milestoneId, milestoneLabel, ...extra })
      });
      if (res.ok) {
        return await res.json();
      }
    } catch (err) {
      console.warn('Milestone stamp failed:', err);
    }
    return null;
  }
}

export const tatumSui = new TatumSuiBridge();
