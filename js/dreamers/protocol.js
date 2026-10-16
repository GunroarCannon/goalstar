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

In actions, refer to nodes by: "START" (where the person is now), "GOAL", an existing node id from the list provided, or the key of a new state you define. Every new state must be connected by at least one action.`;

const DETAIL = {
  brief: { steps: '2–3', text: 'brief. Keep notes to one short sentence; steps may be empty or 1–2 items.' },
  normal: { steps: '3–5', text: 'normal. Notes 1–2 sentences; 2–4 checklist steps per action.' },
  detailed: { steps: '4–6', text: 'detailed. Notes 2–3 specific sentences (real names, numbers, costs); 3–6 concrete checklist steps per action.' },
  deep: { steps: '5–8', text: 'deep. Be exhaustive: notes 2–4 sentences with specifics, tips and common pitfalls; 4–8 checklist steps per action; prefer several smaller states over a few big leaps.' },
};
const ROUTES = {
  one: 'Give a single best route, no alternatives.',
  some: 'Branch into 2–3 alternative routes where they genuinely exist.',
  many: 'Explore many alternatives: 3–5 genuinely different routes, including unconventional ones.',
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
  if (req.mode === 'dream') {
    lines.push(`Task: map out how to get from START to GOAL. Create about ${max} new states (fewer if the goal is simple). ${ROUTES[req.params?.routes] || ROUTES.some} Every route must end with an action whose "to" is "GOAL" — do not invent a separate state that means the goal itself.`);
  } else if (req.mode === 'expand') {
    const n = req.focus.node;
    lines.push(`Task: expand the state HERE = "${n.label}"${n.note ? ` (${n.note})` : ''}. Propose 2–4 promising next states, each reached from HERE by one action (from: "HERE"). If HERE essentially means the goal is reached, or the goal follows from HERE in one natural step, you MUST add an action from HERE to GOAL. Otherwise don't — never jump straight to GOAL from the starting situation or skip over obvious milestones. You may link to existing states when they are the natural next step.`);
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
