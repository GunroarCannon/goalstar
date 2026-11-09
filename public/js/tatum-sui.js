// Browser bridge to the server's Tatum endpoints: live Sui status, sealing a
// milestone certificate, and watching that certificate become verifiable.

const POLL_INTERVAL_MS = 6000;
const POLL_LIMIT_MS = 5 * 60 * 1000;

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
      this.status = await res.json();
    } catch (err) {
      this.status = { live: false, error: err.message };
    }
    this.notify();
    return this.status;
  }

  async stampMilestone(milestoneId, milestoneLabel, extra = {}) {
    try {
      const res = await fetch(`${this.apiBase}/api/tatum/stamp-milestone`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ milestoneId, milestoneLabel, ...extra }),
      });
      return await res.json();
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async verify(jobId) {
    const res = await fetch(`${this.apiBase}/api/tatum/verify/${encodeURIComponent(jobId)}`);
    return res.json();
  }

  // Walrus certification takes about a minute. Calls onReport with each result
  // until the certificate settles, keepGoing() turns false, or time runs out.
  async watchCertificate(jobId, onReport, keepGoing = () => true) {
    const deadline = Date.now() + POLL_LIMIT_MS;
    for (;;) {
      let report;
      try {
        report = await this.verify(jobId);
      } catch (err) {
        report = { verdict: 'incomplete', jobId, checks: [], error: err.message };
      }
      if (!keepGoing()) return report;
      onReport(report);
      if (report.verdict !== 'pending' || Date.now() > deadline) return report;
      await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
      if (!keepGoing()) return report;
    }
  }
}

export const tatumSui = new TatumSuiBridge();
