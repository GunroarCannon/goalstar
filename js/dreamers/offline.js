// Built-in dreamer: no network, no model. Picks a hand-written route template
// by keyword, then fills in h with an exact backward search over the template.
import { normLabel } from '../model.js';

// state: [key, label, note]   action: [from, to, label, time, money, effort, risk, note?]
const TEMPLATES = [
  {
    id: 'relocate',
    match: /\b(move|moving|leave|leaving|emigrat|immigra|abroad|relocat|visa|overseas|live in|living in|citizenship|residen|country)\b/i,
    states: [
      ['r1', 'Target country & visa route chosen', 'You know which country and which legal route (work, study, nomad, family) fits you.'],
      ['r2', 'Job offer from a visa-sponsoring employer', 'An employer abroad will sponsor your work permit.'],
      ['r3', 'Accepted into a study program abroad', 'Student visas are often the most accessible route and lead to post-study work rights.'],
      ['r4', 'Remote income above a nomad-visa threshold', 'Many countries offer digital-nomad visas if you earn enough from abroad.'],
      ['r5', 'Documents ready (passport, degrees, records)', 'Valid passport, apostilled degrees, police record, translations.'],
      ['r6', 'Visa / residence permit approved', ''],
      ['r7', 'Move fund saved (flights + 3–6 months of costs)', ''],
      ['r8', 'First month of housing arranged', ''],
    ],
    actions: [
      ['START', 'r1', 'Compare countries: visa routes, cost of living, language, jobs', 2, 0, 3, 1],
      ['r1', 'r2', 'Apply to visa-sponsoring jobs (LinkedIn, Relocate.me, company sites)', 6, 1, 7, 6],
      ['r1', 'r3', 'Apply to universities or language schools; line up funding', 6, 7, 6, 4],
      ['r1', 'r4', 'Build remote income: freelance clients or a remote job', 7, 1, 7, 5],
      ['r2', 'r5', 'Collect the documents your employer\'s visa needs', 3, 3, 4, 2],
      ['r3', 'r5', 'Collect admission letter, proof of funds, insurance', 3, 4, 4, 2],
      ['r4', 'r5', 'Gather income proof, contracts and bank statements', 3, 2, 4, 3],
      ['r5', 'r6', 'Submit the visa application; attend biometrics / interview', 4, 4, 4, 5],
      ['r6', 'r7', 'Top up the move fund; give notice; sell or store belongings', 4, 5, 5, 2],
      ['r7', 'r8', 'Book temporary housing and flights', 2, 6, 3, 2],
      ['r8', 'GOAL', 'Move, register your address, open a bank account, get a SIM', 2, 3, 5, 3],
    ],
  },
  {
    id: 'app',
    match: /\b(app|apps|app store|play store|startup|saas|launch|product|game|users|downloads|make it big|indie)\b/i,
    states: [
      ['a1', 'Problem validated with 10+ target users', 'They describe the pain unprompted and have tried to solve it.'],
      ['a2', 'Underserved niche spotted in store charts', 'Popular apps with lots of 1–3★ reviews complaining about the same thing.'],
      ['a3', 'Clickable prototype tested with 5 users', ''],
      ['a4', 'MVP in beta (TestFlight / Play testing)', 'Smallest version that delivers the core value.'],
      ['a5', 'Live on the store with a strong listing', 'Good icon, screenshots, keywords, first reviews.'],
      ['a6', 'First 1,000 users from launch & communities', ''],
      ['a7', 'First 1,000 users from ASO & content', ''],
      ['a8', 'Healthy retention: users come back weekly', ''],
      ['a9', 'Repeatable growth engine working', 'Referrals, content, or paid ads that pay back.'],
    ],
    actions: [
      ['START', 'a1', 'Interview potential users about the problem', 3, 0, 4, 2],
      ['START', 'a2', 'Study top charts & competitors\' bad reviews for unmet needs', 2, 0, 3, 3],
      ['a1', 'a3', 'Prototype in Figma; run quick usability tests', 3, 1, 4, 2],
      ['a2', 'a3', 'Prototype the better version; test with competitor users', 3, 1, 4, 3],
      ['a3', 'a4', 'Build the smallest version that delivers the core value', 6, 2, 8, 4],
      ['a4', 'a5', 'Fix beta feedback; screenshots, keywords, privacy policy; submit', 3, 2, 5, 3],
      ['a5', 'a6', 'Launch on Product Hunt, Reddit, TikTok, Discord communities', 3, 1, 6, 5],
      ['a5', 'a7', 'Keyword research; optimize listing; publish content on the problem', 5, 1, 5, 4],
      ['a6', 'a8', 'Measure retention; talk to churned users; ship weekly', 5, 1, 7, 4],
      ['a7', 'a8', 'Measure retention; talk to churned users; ship weekly', 5, 1, 7, 4],
      ['a8', 'a9', 'Add referral loops; test paid acquisition where LTV > CAC', 6, 5, 6, 5],
      ['a9', 'GOAL', 'Scale the best channel; hire help; keep shipping', 8, 6, 7, 4],
    ],
  },
  {
    id: 'money',
    match: /\b(money|rich|wealth|income|salary|save|saving|debt|invest|financ|million|\$)/i,
    states: [
      ['m1', 'Clear picture of income, spending & net worth', ''],
      ['m2', 'Emergency fund: 3 months of expenses', ''],
      ['m3', 'High-interest debt paid off', ''],
      ['m4', 'Income raised (raise, new job or side income)', ''],
      ['m5', 'Investing automatically every month', ''],
    ],
    actions: [
      ['START', 'm1', 'Track every expense for 30 days; build a budget', 2, 0, 3, 0],
      ['m1', 'm2', 'Cut 2–3 big expenses; automate savings transfers', 5, 0, 4, 1],
      ['m2', 'm3', 'Avalanche method: pay highest-interest debt first', 6, 0, 4, 1],
      ['m2', 'm4', 'Negotiate a raise, switch jobs, or start a side gig', 5, 0, 6, 4],
      ['m3', 'm5', 'Automate contributions to index funds / retirement accounts', 1, 0, 2, 2],
      ['m4', 'm5', 'Invest the extra income automatically', 1, 0, 2, 2],
      ['m5', 'GOAL', 'Stay the course; raise contributions whenever income grows', 9, 0, 3, 3],
    ],
  },
  {
    id: 'fitness',
    match: /\b(fit|fitness|weight|lose|muscle|run|running|marathon|gym|health|strong|diet)\b/i,
    states: [
      ['f1', 'Baseline measured & realistic target set', ''],
      ['f2', 'Training 3×/week for 4 weeks straight', ''],
      ['f3', 'Nutrition & sleep dialed in', ''],
      ['f4', 'Coach, program or training partner in place', ''],
      ['f5', 'First milestone hit', ''],
    ],
    actions: [
      ['START', 'f1', 'Measure weight / times / lifts; check in with a doctor', 1, 1, 2, 1],
      ['f1', 'f2', 'Pick a simple program; schedule sessions like meetings', 4, 1, 6, 2],
      ['f1', 'f4', 'Join a club, hire a coach, or find a partner', 2, 5, 3, 1],
      ['f4', 'f2', 'Show up to every scheduled session', 4, 1, 5, 1],
      ['f2', 'f3', 'Track food for 2 weeks; fix your sleep schedule', 3, 1, 4, 1],
      ['f3', 'f5', 'Progressive overload with weekly check-ins', 6, 1, 6, 2],
      ['f5', 'GOAL', 'Repeat training blocks; adjust the plan every 6 weeks', 7, 1, 6, 3],
    ],
  },
  {
    id: 'career',
    match: /\b(job|career|promot|hired|interview|role|position|work at|engineer at)\b/i,
    states: [
      ['c1', 'Target role & companies defined', ''],
      ['c2', 'Skill gaps for the role closed', ''],
      ['c3', 'Resume & portfolio tailored to the role', ''],
      ['c4', 'Warm intros / referrals lined up', ''],
      ['c5', 'Interviews in progress', ''],
      ['c6', 'Offer in hand', ''],
    ],
    actions: [
      ['START', 'c1', 'Read 20 job posts; list required skills & salary range', 1, 0, 2, 0],
      ['c1', 'c2', 'Close the gaps with one focused project', 6, 2, 6, 2],
      ['c1', 'c3', 'Rewrite your resume around results; add portfolio pieces', 2, 0, 4, 1],
      ['c2', 'c3', 'Turn the project into a portfolio piece; update resume', 2, 0, 3, 1],
      ['c3', 'c4', 'Reach out to 20 people at target companies', 3, 0, 5, 3],
      ['c3', 'c5', 'Send 30+ tailored applications', 4, 0, 6, 4],
      ['c4', 'c5', 'Ask for referrals; book interviews', 2, 0, 3, 3],
      ['c5', 'c6', 'Practice interviews; follow up; negotiate', 3, 0, 6, 5],
      ['c6', 'GOAL', 'Accept, set a start date, onboard well', 1, 0, 2, 1],
    ],
  },
  {
    id: 'learn',
    match: /\b(learn|master|fluent|language|skill|study|degree|certif|become a|draw|guitar|piano|code)\b/i,
    states: [
      ['l1', 'Clear target level & how it will be tested', ''],
      ['l2', 'One course or curriculum chosen', ''],
      ['l3', 'Daily practice habit running (30+ min)', ''],
      ['l4', 'First real project / conversation completed', ''],
      ['l5', 'Feedback from an expert or community', ''],
      ['l6', 'Credential or portfolio proving the skill', ''],
    ],
    actions: [
      ['START', 'l1', 'Define what "done" looks like (exam, project, fluency test)', 1, 0, 2, 0],
      ['l1', 'l2', 'Pick one course or book; ignore the rest', 1, 2, 2, 1],
      ['l2', 'l3', 'Schedule daily practice; keep a streak', 4, 0, 5, 2],
      ['l3', 'l4', 'Use the skill on something real', 4, 1, 6, 3],
      ['l4', 'l5', 'Share your work; get critique; find a mentor', 2, 1, 4, 3],
      ['l5', 'l6', 'Polish into a portfolio or sit the exam', 4, 3, 6, 3],
      ['l6', 'GOAL', 'Use it for real: a job, a client, a trip, or teaching others', 4, 1, 5, 3],
    ],
  },
  {
    id: 'generic',
    match: /.*/,
    states: [
      ['g1', 'Finish line defined & measurable', 'What exactly is true on the day you\'ve made it?'],
      ['g2', 'Gaps mapped: skills, money, people, time', ''],
      ['g3', 'Advice from someone who already did it', ''],
      ['g4', 'First small milestone achieved', ''],
      ['g5', 'Weekly routine & feedback loop running', ''],
      ['g6', 'Biggest obstacle removed', ''],
    ],
    actions: [
      ['START', 'g1', 'Write what "{goal}" means in numbers and a date', 1, 0, 2, 0],
      ['g1', 'g2', 'List what you lack; estimate cost & time for each', 1, 0, 3, 1],
      ['g2', 'g3', 'Find and ask 3 people who achieved it', 2, 0, 4, 2],
      ['g2', 'g4', 'Do the smallest real step toward it this week', 2, 1, 4, 2],
      ['g3', 'g4', 'Apply their advice to a first small step', 2, 1, 4, 2],
      ['g4', 'g5', 'Block weekly time; review progress every Sunday', 4, 0, 5, 2],
      ['g5', 'g6', 'Tackle the hardest blocker head-on', 5, 3, 7, 5],
      ['g6', 'GOAL', 'Keep compounding until you cross the finish line', 7, 3, 6, 4],
    ],
  },
];

const avg = (a) => (a[3] + a[4] + a[5] + a[6]) / 4;
const fill = (s, goal) => s.replaceAll('{goal}', goal);

function pickTemplate(req) {
  const text = `${req.goal.label} ${req.goal.note || ''}`;
  return TEMPLATES.find((t) => t.match.test(text));
}

// Exact remaining cost from each template state to GOAL (Dijkstra on reversed edges).
function remaining(t) {
  const dist = { GOAL: 0 };
  for (let changed = true; changed;) {
    changed = false;
    for (const a of t.actions) {
      if (dist[a[1]] == null) continue;
      const d = dist[a[1]] + avg(a);
      if (dist[a[0]] == null || d < dist[a[0]]) { dist[a[0]] = d; changed = true; }
    }
  }
  return dist;
}

function toAction(a, goal, from = a[0]) {
  return { from, to: a[1], label: fill(a[2], goal), note: a[7] || '', time: a[3], money: a[4], effort: a[5], risk: a[6] };
}

function dream(req) {
  const t = pickTemplate(req);
  const h = remaining(t);
  const goal = req.goal.label;
  return {
    states: t.states.map(([key, label, note]) => ({ key, label: fill(label, goal), note, h: Math.round((h[key] ?? 10) * 10) / 10 })),
    actions: t.actions.map((a) => toAction(a, goal)),
  };
}

function expand(req) {
  const t = pickTemplate(req);
  const h = remaining(t);
  const goal = req.goal.label;
  const node = req.focus.node;
  const isStart = req.existing?.some((n) => n.id === node.id && n.kind === 'start');
  const tKey = isStart ? 'START' : t.states.find((s) => normLabel(fill(s[1], goal)) === normLabel(node.label))?.[0];

  if (tKey) {
    const next = t.actions.filter((a) => a[0] === tKey);
    if (next.length) {
      const keys = new Set(next.map((a) => a[1]));
      return {
        states: t.states.filter((s) => keys.has(s[0])).map(([key, label, note]) => ({ key, label: fill(label, goal), note, h: h[key] ?? 10 })),
        actions: next.map((a) => toAction(a, goal, 'HERE')),
      };
    }
  }

  // No template knowledge: offer three generic moves, plus a final push once we're past the start.
  const g = goal.length > 40 ? goal.slice(0, 39) + '…' : goal;
  const base = Math.max(4, (node.h ?? 12) - 3);
  const out = {
    states: [
      { key: 'x1', label: `Know exactly what's needed after "${node.label.slice(0, 40)}"`, note: '', h: base },
      { key: 'x2', label: `Small real test toward "${g}" done`, note: '', h: base - 1 },
      { key: 'x3', label: `Mentor or insider for "${g}" found`, note: '', h: base },
    ],
    actions: [
      { from: 'HERE', to: 'x1', label: 'Research the requirements for the next step', note: '', time: 2, money: 0, effort: 3, risk: 1 },
      { from: 'HERE', to: 'x2', label: 'Run the smallest experiment you can this week', note: '', time: 2, money: 1, effort: 4, risk: 3 },
      { from: 'HERE', to: 'x3', label: 'Ask three people who have done it', note: '', time: 2, money: 0, effort: 4, risk: 3 },
    ],
  };
  if (!isStart) out.actions.push({ from: 'HERE', to: 'GOAL', label: `Final push to "${g}"`, note: 'Rough guess — break it down when you get here.', time: 6, money: 4, effort: 7, risk: 5 });
  return out;
}

function breakdown(req) {
  const e = req.focus.edge;
  const c = e.cost || {};
  const third = (v) => Math.round(((v ?? 3) / 3) * 10) / 10;
  const cost = { time: third(c.time), money: third(c.money), effort: third(c.effort), risk: third(c.risk) };
  const what = e.label.length > 50 ? e.label.slice(0, 49) + '…' : e.label;
  return {
    states: [
      { key: 'b1', label: `Ready to: ${what}`, note: 'Requirements known, materials and time lined up.', h: null },
      { key: 'b2', label: `Halfway through: ${what}`, note: '', h: null },
    ],
    actions: [
      { from: 'FROM', to: 'b1', label: 'Plan it: list sub-tasks, deadlines and what you need', note: '', ...cost },
      { from: 'b1', to: 'b2', label: 'Do the first half', note: '', ...cost },
      { from: 'b2', to: 'TO', label: 'Finish and verify it worked', note: '', ...cost },
    ],
  };
}

export default {
  id: 'offline',
  name: 'Offline',
  async generate(req) {
    if (req.mode === 'dream') return dream(req);
    if (req.mode === 'expand') return expand(req);
    if (req.mode === 'breakdown') return breakdown(req);
    throw new Error(`Unknown mode ${req.mode}`);
  },
};
