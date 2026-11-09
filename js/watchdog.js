// GoalStar Workflow Watchdog & Escalation Rule Engine
// Tracks active workflow nodes, logs daily progress, and executes learned escalation rules

export class WorkflowWatchdog {
  constructor(memoryBridge) {
    this.memory = memoryBridge;
    // ?staleHours= shortens the wait so a demo doesn't take two days.
    const override = typeof location !== 'undefined' ? Number(new URLSearchParams(location.search).get('staleHours')) : 0;
    this.staleThresholdHours = override > 0 ? override : 48;
  }

  // The step you should be on right now has seen no progress for too long.
  // Only the next steps on the best route count: later ones aren't due yet.
  evaluateEscalation(board, routeEdges = []) {
    const stalled = [];
    const now = Date.now();
    for (const id of routeEdges) {
      const edge = board.edges[id];
      const from = board.nodes[edge?.from];
      const to = board.nodes[edge?.to];
      if (!from || !to || to.done || !(from.done || from.kind === 'start')) continue;
      const since = Math.max(from.doneAt || 0, to.created || 0, edge.touchedAt || 0, board.created || 0);
      if (!since) continue; // real timestamps only
      const ageHours = (now - since) / 3600000;
      if (ageHours >= this.staleThresholdHours) stalled.push({ edgeId: id, nodeId: to.id, label: edge.label, ageHours });
    }
    return stalled;
  }
}
