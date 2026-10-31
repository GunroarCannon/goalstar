// GoalStar Workflow Watchdog & Escalation Rule Engine
// Tracks active workflow nodes, logs daily progress, and executes learned escalation rules

export class WorkflowWatchdog {
  constructor(memoryBridge) {
    this.memory = memoryBridge;
    this.staleThresholdHours = 48;
    this.lastTuesdayInsight = null;
  }

  /**
   * Generates the adaptive memory insight banner from Walrus Memory.
   */
  generateLastTuesdayInsight() {
    if (!this.memory.memories.length) {
      return {
        hasInsight: false,
        text: "No memories logged yet.",
        ruleApplied: "Record progress notes or blockers to apply learned friction to future routes."
      };
    }

    const frictionMem = this.memory.memories.find(m => 
      (m.text || '').toLowerCase().includes('blocked') ||
      (m.text || '').toLowerCase().includes('friction') ||
      (m.text || '').toLowerCase().includes('stuck') ||
      (m.text || '').toLowerCase().includes('injury') ||
      (m.text || '').toLowerCase().includes('cant') ||
      (m.text || '').toLowerCase().includes("can't")
    );

    if (frictionMem) {
      return {
        hasInsight: true,
        source: frictionMem.source || 'walrus_mainnet',
        text: frictionMem.text,
        ruleApplied: "A* engine applies dynamic friction penalties to matching roadblocks.",
      };
    }

    return {
      hasInsight: true,
      source: 'walrus_mainnet',
      text: this.memory.memories[0]?.text || '',
      ruleApplied: "A* route informed by your real recorded session history.",
    };
  }

  /**
   * Evaluates active board nodes to detect stalled/stale tasks (>48h).
   */
  evaluateEscalation(board) {
    if (!board || !board.nodes) return [];

    const escalations = [];
    const now = Date.now();

    for (const node of Object.values(board.nodes)) {
      if (node.kind === 'start' || node.done) continue;

      const startTime = node.activeSince || node.created;
      if (!startTime) continue; // Real timestamp only - no simulated age

      const ageHours = (now - startTime) / (1000 * 3600);
      if (ageHours >= this.staleThresholdHours) {
        escalations.push({
          nodeId: node.id,
          label: node.label,
          ageHours: Math.round(ageHours),
          recommendation: "Auto-Decompose into 15-minute micro-steps (breakdown mode)",
          rule: "Learned Escalation Rule: Break down milestones when inactive >48h",
        });
      }
    }

    return escalations;
  }
}
