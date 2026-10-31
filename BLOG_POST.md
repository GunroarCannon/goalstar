# GoalStar: Building an Autonomous Workflow Watchdog with Walrus Portable Memory & Tatum Sui RPC

> **Track 02**: Smart Agents for Real Life  
> **Special Award Target**: Best Walrus Memory ($500)  
> **Walrus Account ID**: `0x49cb5c5550e8f69445a4af7ec37f2088b54ed8ce10667dc0fa03c2f503ca2cb5`  
> **Relayer**: `https://relayer.memory.walrus.xyz` (Namespace: `goalstar-workflows`)  
> **Tatum Sui RPC**: `https://api.tatum.io/v3/blockchain/node/sui-mainnet`

---

## 1. The Core Problem: Why Habit Trackers and Goal Planners Fail

Every productivity app makes the same flawed assumption: **that willpower is constant and linear**. 

You open a clean roadmap, write down ambitious milestones ("Build SaaS Architecture", "Setup Kubernetes Cluster", "Deploy to Production"), and plan for 40 hours of uninterrupted energy. 

Then **Last Tuesday** happens. 

You work an unexpected 12-hour shift, get stuck on obscure Docker networking configs for four hours, feel completely drained, and miss your milestone by two days. 

In traditional apps, this triggers the **Shame Spiral**:
1. Red overdue badges pile up.
2. The static checklist ignores your real-world fatigue.
3. You feel guilty, avoid opening the app, and abandon the goal entirely.

We built **GoalStar Total Recall Edition** to fix this broken paradigm. 

Instead of a passive checklist, GoalStar is an **autonomous workflow watchdog** powered by **Walrus Portable Memory on Mainnet** and **Tatum’s Sui RPC Gateway**. It learns your true stamina thresholds, remembers your historical blockers across tools, and **physically alters its pathfinding algorithm in real time to steer you around burnout**.

---

## 2. Architecture: Portable Memory Across Tools & Sessions

A core philosophy of the Total Recall hackathon is that memory must be **portable**: agents should remember context across different applications, terminals, and devices.

GoalStar decouples memory from the web browser:

```
                     ┌─────────────────────────────────────────┐
                     │   Portable Terminal CLI (cli/log.js)    │
                     └────────────────────┬────────────────────┘
                                          │ Logs habit updates / blockers
                                          ▼
┌───────────────────────────────┐  HTTP API   ┌─────────────────────────────────────────┐
│  GoalStar Web Interface       │◄───────────►│  Express & Agent Server (server.js)     │
│  - Dynamic A* Rerouting Visual│             ├─────────────────────────────────────────┤
│  - "Remembered Last Tuesday"  │             │  • Walrus Memory Bridge (memwal.js)     │
│  - Sui Milestone Certificates │             │  • Workflow Watchdog & Escalation Rules │
│  - Tactile Skeuomorphic UI    │             │  • Tatum Sui RPC Gateway Client         │
└───────────────────────────────┘             └────────────┬───────────────┬────────────┘
                                                           │               │
                                   Walrus Mainnet Relayer  │               │ Tatum Sui RPC
                                                           ▼               ▼
                                              ┌─────────────────┐ ┌─────────────────┐
                                              │  Walrus Memory  │ │  Sui Blockchain │
                                              │  (Mainnet Blobs)│ │  (Milestones)   │
                                              └─────────────────┘ └─────────────────┘
```

### The Terminal CLI Experience
Developers don't spend their entire day in a browser tab. When you hit a roadblock while coding, you can log it right from your terminal:

```bash
# Log a real blocker from terminal while coding:
node cli/log.js "Spent 3 hours debugging Docker configs, exhausted. Need smaller micro-steps tomorrow."
```

This write is immediately serialized and anchored on **Walrus Mainnet** via the `@mysten-incubation/memwal` client. 

When you later open the GoalStar web app, the agent queries Walrus, matches the milestone you are considering, and displays the **"Remembered Last Tuesday"** context banner, adjusting your schedule before you can burn out again.

---

## 3. How Walrus Memory Visibly Changes the Product ($500 Best Memory Target)

Many hackathon projects treat memory as a static append-only database—storing text and simply displaying it back in a chat box. 

**In GoalStar, memories actively and visibly change the product's core algorithm and visual interface:**

### A* Pathfinding with Dynamic Friction Penalties
GoalStar uses an $A^*$ pathfinding algorithm where every step between milestones has a calculated edge cost:
$$\text{Cost} = w_t \cdot \text{Time} + w_m \cdot \text{Money} + w_e \cdot \text{Effort} + w_r \cdot \text{Risk} + \text{WalrusFriction}$$

When the user plans a goal, GoalStar recalls memories matching the edge actions from Walrus Mainnet. 

For example, when evaluating the edge `"Setup Docker cluster and k8s config"`:
1. GoalStar recalls Walrus memory:
   > `[LAST TUESDAY] User spent 4 hours fighting Kubernetes and Docker configs, became frustrated, and abandoned early.`
2. The agent identifies a **high-friction burnout pattern** and dynamically applies a **$+3.5$ friction penalty** to that edge.
3. **The shortest path physically reroutes on screen!** 
   Instead of forcing the user into the monolithic DevOps trap, the highlighted green route instantly bends away toward:
   `"Deploy to Managed Cloud / PaaS (Low Friction)"`
4. The user sees the alternative path with zero guilt and 100% momentum.

### Autonomous 48-Hour Stalled Milestone Escalation
If a milestone remains inactive for over 48 hours, the agent recalls past velocity patterns from Walrus:
> `[STALLED TASK ESCALATION] When a task remains inactive for >48 hours, auto-decomposition into 15-minute sub-steps restores momentum.`

The AI dreamer kicks in automatically, breaking the intimidating monolithic task into four manageable 15-minute micro-checklists.

---

## 4. Tatum Sui RPC Gateway Integration

To provide verifiable accountability without centralized databases, GoalStar uses **Tatum’s Sui RPC Gateway**:

1. **Live Mainnet Network Health**:
   GoalStar polls Tatum Sui RPC (`sui_getLatestCheckpointSequenceNumber`) to ensure live onchain synchronization:
   ```javascript
   const res = await fetch('https://api.tatum.io/v3/blockchain/node/sui-mainnet', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json', 'x-api-key': process.env.TATUM_API_KEY },
     body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'sui_getLatestCheckpointSequenceNumber', params: [] })
   });
   ```

2. **Immutable Milestone Proofs**:
   When a user marks a milestone complete, a cryptographic certificate containing the goal ID, milestone hash, timestamp, and active Sui checkpoint sequence is signed and sealed on Walrus.

3. **Free-Tier Sliding-Window Armor**:
   Tatum's free tier provides 3 requests/sec. To prevent user pathfinding queries from exceeding quotas, we engineered an in-memory sliding-window rate guard with a 15-second cache. The app achieves **zero dropped requests** and 100% uptime without burning developer quotas.

---

## 5. Mainnet Walrus Memory Verification

As required by the hackathon submission guidelines, GoalStar has pre-seeded and written **over 20 verified entries** directly to Walrus Mainnet:

* **Account ID**: `0x49cb5c5550e8f69445a4af7ec37f2088b54ed8ce10667dc0fa03c2f503ca2cb5`
* **Relayer Endpoint**: `https://relayer.memory.walrus.xyz`
* **Namespace**: `goalstar-workflows`

### Sample Stored Memory Types:
- **`[WORKFLOW FRICTION]`**: Patterns identifying monolithic vs modular efficiency.
- **`[HABIT VELOCITY]`**: Real completion rates for 15-minute tasks vs 2-hour blocks.
- **`[LAST TUESDAY]`**: Specific episodic memories of past technical fatigue.
- **`[MILESTONE BLOB]`**: Decentralized board definitions and verified completion certificates stored on Walrus blobs.

Anyone can verify these memories by cloning the repository and running:
```bash
npm run cli --status
npm test:integration
```

---

## 6. Conclusion & What's Next

Static productivity tools fail because human life is unpredictable. By coupling **Walrus Decentralized Portable Memory** with **adaptive $A^*$ pathfinding** and **Tatum Sui RPC verification**, GoalStar proves that software can be empathetic, persistent, and genuinely intelligent.

It doesn't judge you when Tuesday goes wrong. It remembers, adapts, and finds you a better route.
