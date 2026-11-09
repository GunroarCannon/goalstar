// The dreamer protocol: what every dreamer plugin receives and must return.
//
// Request (parameters in):
//   { mode: 'dream' | 'expand' | 'bridge' | 'breakdown' | 'detail',
//     goal:  { label, note }, start: { label, note }, constraints, timeframe, budget,
//     focus: { node: {id,label,note,h} } | { edge: {label,note,from,to,cost,steps} } | null,
//     existing: [{ id, label, kind, done }],
//     params: { maxStates, detail: 'brief'|'normal'|'detailed'|'deep', routes: 'one'|'some'|'many', weights } }
//
// Result (parameters out):
//   { states:  [{ key, label, note, h }],
//     actions: [{ from, to, label, note, time, money, effort, risk, duration, steps: [string] }] }
//
// In actions, from/to are: "START", "GOAL", "HERE" (expand), "FROM"/"TO" (breakdown),
// an existing node id, or the key of a new state from `states`.

export const RESULT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['states', 'actions'],
  properties: {
    states: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['key', 'label', 'note', 'h'],
        properties: {
          key: { type: 'string' },
          label: { type: 'string' },
          note: { type: 'string' },
          h: { type: 'number' },
        },
      },
    },
    actions: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['from', 'to', 'label', 'note', 'time', 'money', 'effort', 'risk', 'duration', 'steps'],
        properties: {
          from: { type: 'string' },
          to: { type: 'string' },
          label: { type: 'string' },
          note: { type: 'string' },
          time: { type: 'number' },
          money: { type: 'number' },
          effort: { type: 'number' },
          risk: { type: 'number' },
          duration: { type: 'string' },
          steps: { type: 'array', items: { type: 'string' } },
        },
      },
    },
  },
};

export const SYSTEM_PROMPT = `You are the "dreamer" inside goalstar, a personal planner that treats reaching a life goal like A* pathfinding.

The plan is a directed graph:
- STATES are nodes: situations that are true at some point, phrased as achieved conditions ("Valid passport in hand", "1,000 weekly active users"), never as tasks.
- ACTIONS are edges from one state to the next: concrete things the person does ("Apply for a passport at the post office").

Rate every action on four 0–10 scales:
- time: 0 = minutes, 3 ≈ a week, 5 ≈ a month, 7 ≈ six months, 10 = years
- money: 0 = free, 5 ≈ a month of income, 10 = life savings
- effort: 0 = trivial, 10 = all-consuming
- risk: 0 = certain to work, 10 = likely to fail

Also give each action a realistic "duration" in plain words ("2–3 weeks", "about 6 months") and "steps": a checklist of concrete sub-tasks for doing it (how many depends on the requested detail level).

For every state give h: your estimate of the remaining cost from that state to the goal, i.e. the sum over the remaining actions of the average of their four ratings. h must shrink as states get closer to the goal.

Be specific and realistic for this person's situation: name real platforms, documents, programs, numbers and typical timelines. Where genuinely different routes exist, branch into alternatives so the search can compare them. Keep labels short (under ~60 characters) and put detail in notes and steps.

In actions, refer to nodes by: "START" (where the person is now), "GOAL", an existing node id from the list provided, or the key of a new state you define. Every new state must be connected by at least one incoming action and at least one outgoing action towards subsequent milestones or GOAL, so no state is left as an orphaned dead-end leaf node.`;

const DETAIL = {
  brief: { steps: '2–3', text: 'brief. Keep notes to one short sentence; steps may be empty or 1–2 items.' },
  normal: { steps: '3–5', text: 'normal. Notes 1–2 sentences; 2–4 checklist steps per action.' },
  detailed: { steps: '4–6', text: 'detailed. Multi-path plan with 4–5 alternative branches. Notes 2–3 specific sentences (real names, numbers, costs); 3–6 concrete checklist steps per action.' },
  deep: { steps: '5–8', text: 'deep. Exhaustive multi-path exploration with 5+ parallel routes; notes 2–4 sentences with specifics, tips and common pitfalls; 4–8 checklist steps per action; prefer several smaller states over a few big leaps.' },
};
const ROUTES = {
  one: 'Give a single best route with no alternatives (but still split a step where the order genuinely matters).',
  some: 'Branch into 3–4 alternative parallel routes wherever they genuinely exist; put at least two parallel choices at the main decision points.',
  many: 'Explore many alternative paths: 4–6 genuinely different routes, including unconventional ones. At least three decision points must have two or more outgoing actions, and all alternative branches should connect through to GOAL.',
};

export function buildUserPrompt(req) {
  const lines = [
    `Goal: ${req.goal.label}`,
    req.goal.note && `Goal notes: ${req.goal.note}`,
    `Where I am now: ${req.start.label}${req.start.note ? ' — ' + req.start.note : ''}`,
    req.constraints && `Constraints / resources: ${req.constraints}`,
    req.timeframe && `Timeframe: ${req.timeframe}`,
    req.budget && `Budget: ${req.budget}`,
  ];
  if (req.memories?.length) {
    lines.push('', 'What this person has learned from past work. Steer away from what blocked them and build on what worked:', ...req.memories.map((m) => `- ${m}`));
  }
  if (req.existing?.length) {
    lines.push('', 'Existing states (id: label):');
    for (const n of req.existing) {
      const tag = n.kind === 'goal' ? ' [GOAL]' : n.kind === 'start' ? ' [START]' : n.done ? ' [achieved]' : '';
      lines.push(`- ${n.id}: ${n.label}${tag}`);
    }
  }
  lines.push('');
  const max = req.params?.maxStates ?? 8;
  const detail = DETAIL[req.params?.detail] || DETAIL.normal;
  const isDetailed = req.params?.detail === 'detailed' || req.params?.detail === 'deep';
  if (req.mode === 'dream') {
    let branches = req.params?.routes === 'many' ? 5 : req.params?.routes === 'one' ? 1 : 3;
    if (isDetailed && branches < 4) branches = 4;
    lines.push(`Task: map out how to get from START to GOAL. Create about ${max} new states (fewer only if the goal is truly simple). Aim for at least ${branches} distinct routes or decision points so the search has multiple alternative paths to choose between. ${ROUTES[req.params?.routes] || (isDetailed ? ROUTES.many : ROUTES.some)} Every route must end with an action whose "to" is "GOAL" — do not invent a separate state that means the goal itself.`);
    if (isDetailed || req.params?.routes === 'many') {
      lines.push(
        '',
        'CRITICAL REQUIREMENT — MULTIPLE PARALLEL PATHS:',
        'The user specifically requested a DETAILED multi-path plan. You MUST map out at least 4–6 distinct parallel routes or decision branches from START to GOAL (e.g. fast-track vs budget-friendly vs safe/traditional vs DIY).',
        'Do NOT return a single linear chain of milestones. Decision points must branch into genuine alternatives, and EVERY branch must connect all the way through to GOAL so A* can evaluate and compare multiple complete paths.'
      );
    }
  } else if (req.mode === 'expand') {
    const n = req.focus.node;
    lines.push(
      `Task: expand the state HERE = "${n.label}"${n.note ? ` (${n.note})` : ''}. Propose 2–4 promising next states reached from HERE by actions (from: "HERE"). Include at least one genuinely different alternative route so the search has real branches to compare.`,
      '',
      'CRITICAL REQUIREMENT — NO DEAD-END LEAF NODES:',
      'Newly added states must NOT be dead-end leaf nodes. Every new state MUST have at least one outgoing action that helps form a path to the goal:',
      '1. Link to existing milestone: If an existing state (from the list of existing states below) is the natural next step, add an action from the new state to that existing state ID.',
      '2. Link to GOAL: If the new state reaches or is adjacent to the goal, add an action from the new state to "GOAL".',
      '3. Chain to next step: If introducing intermediate milestones, connect them sequentially towards GOAL (e.g. HERE -> newStateA -> newStateB -> GOAL or existing state ID).',
      'Every branch created MUST provide a navigable continuation toward GOAL so A* can find a complete path through it. Never leave any new state as an isolated leaf node!'
    );
  } else if (req.mode === 'bridge') {
    const n = req.focus.node;
    lines.push(`Task: the plan currently stops at HERE = "${n.label}"${n.note ? ` (${n.note})` : ''} without reaching the goal. Add the 0–3 remaining states and the actions needed to get from HERE (from: "HERE") all the way to GOAL. The chain MUST end with an action whose "to" is "GOAL". If the goal follows directly from HERE, return just that one action to GOAL.`);
  } else if (req.mode === 'breakdown') {
    const e = req.focus.edge;
    lines.push(`Task: break the action "${e.label}"${e.note ? ` (${e.note})` : ''} — which goes from FROM = "${e.from}" to TO = "${e.to}" — into 2–4 smaller sequential steps. Create the intermediate states and a chain of actions FROM → … → TO. The sub-actions together should cost roughly what the original did.`);
  } else if (req.mode === 'detail') {
    const e = req.focus.edge;
    lines.push(`Task: flesh out the action "${e.label}"${e.note ? ` (${e.note})` : ''}, which goes from FROM = "${e.from}" to TO = "${e.to}". Return NO states and exactly ONE action with from "FROM" and to "TO": keep the label (tighten it only if it is vague), write a specific note, give a realistic duration and re-rate the costs, and list ${detail.steps} concrete checklist steps in order. Name the real websites, offices, forms, documents, amounts and timelines involved.${e.steps?.length ? ` Existing checklist to improve on: ${e.steps.join(' | ')}` : ''}`);
  }
  if (req.mode !== 'detail') lines.push('', `Detail level: ${detail.text}`);
  return lines.filter((l) => l !== undefined && l !== null && l !== false).join('\n');
}

const num = (v, lo, hi, d) => {
  const x = Number(v);
  return Number.isFinite(x) ? Math.min(hi, Math.max(lo, x)) : d;
};
const str = (v, max) => String(v ?? '').trim().slice(0, max);

// Make any dreamer's output safe to merge.
export function normalize(r) {
  if (!r || typeof r !== 'object') throw new Error('Dreamer returned no data');
  const states = (Array.isArray(r.states) ? r.states : []).slice(0, 40)
    .map((s, i) => ({ key: str(s?.key || `s${i}`, 60), label: str(s?.label, 140), note: str(s?.note, 600), h: num(s?.h, 0, 500, null) }))
    .filter((s) => s.label);
  const actions = (Array.isArray(r.actions) ? r.actions : []).slice(0, 80)
    .map((a) => ({
      from: str(a?.from, 60), to: str(a?.to, 60),
      label: str(a?.label, 160) || 'Next step', note: str(a?.note, 600),
      time: num(a?.time, 0, 10, 3), money: num(a?.money, 0, 10, 3),
      effort: num(a?.effort, 0, 10, 3), risk: num(a?.risk, 0, 10, 3),
      duration: str(a?.duration, 40),
      steps: (Array.isArray(a?.steps) ? a.steps : []).slice(0, 12).map((t) => str(typeof t === 'string' ? t : t?.text, 320)).filter(Boolean),
    }))
    .filter((a) => a.from && a.to);
  return { states, actions };
}
