# GoalStar: Total Recall Edition

> **Autonomous Habit & Workflow Watchdog Agent** with Walrus Portable Memory on Mainnet & Tatum Sui RPC Gateway.
> Built for the **Total Recall Hackathon** — *Track 02: Smart Agents for Real Life*.

---

## The Pitch: Autonomous Workflow Memory

Traditional habit and goal planners fail because they are **static to-do lists**. When engineers hit real-world friction (long shifts, burnout, technical roadblocks), tasks stall, overdue alerts pile up, and users abandon the roadmap.

**GoalStar Total Recall Edition** transforms goal pathfinding into an **autonomous workflow watchdog** that remembers your real-world stamina, friction points, and past struggles across tools and sessions.

* **Portable Memory Across Tools**: Your memory lives on **Walrus Mainnet** via a portable Agent ID. Log blockers from your terminal CLI while coding (`npm run cli "Blocked on Docker setup"`), and your desktop GoalStar map picks up right where you left off.
* **Learns True Friction Patterns**: The agent remembers past execution friction (e.g., *"Monolithic deployments hit repeated CI/CD build bottlenecks"*).
* **Learns Your Escalation Rules**: When a task stalls for >48 hours, the agent automatically decomposes monolithic tasks into 15-minute micro-steps (`breakdown` dreamer mode).
* **Visibly Changes the Product ($500 Best Walrus Memory Bonus)**: A* pathfinding doesn't just calculate theoretical costs; it applies dynamic friction penalties from Walrus Mainnet. **The A* path physically reroutes on screen around your personal friction patterns!**
* **Verifiable Milestones (Tatum + Walrus + Sui)**: Finished milestones become certificates anchored to a live Sui checkpoint read through Tatum, stored on Walrus through Tatum, and independently re-checkable against the chain by anyone.

---

## Hackathon Checklist Alignment

| Total Recall Requirement | How GoalStar Delivers |
| :--- | :--- |
| **01. Walrus Memory on Mainnet** | Fully integrated using `@mysten-incubation/memwal` writing directly to `https://relayer.memory.walrus.xyz`. |
| **02. Tatum Sui RPC & Native Walrus Storage** | Tatum's Sui gRPC gateway (`sui-mainnet-grpc.gateway.tatum.io`) supplies live checkpoints and re-reads transactions and objects during verification. Tatum's Storage API (`/v4/data/storage/upload`) certifies each milestone on Walrus Mainnet. See [How a certificate is verified](#how-a-certificate-is-verified). |
| **03. At Least 10 Memories on Mainnet** | 42 memories in the project namespace, including a build journal written with `npm run journal`. |
| **04. Published Blog Post & Docs** | Comprehensive writeup explaining the Walrus learning loop and Tatum Sui architecture. |
| **05. Working Demo & Public Repo** | Fully functional local server, web interface, and portable CLI. |
| **Special: Best Walrus Memory ($500)** | The A* search algorithm dynamically recalculates edge costs using Walrus memories, visibly altering the shortest path in real time. |

---

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment (`.env`)
Copy `.env.example` to `.env`:
```ini
PORT=8000
MEMWAL_ACCOUNT_ID=your_walrus_account_id
MEMWAL_PRIVATE_KEY=your_walrus_delegate_key
MEMWAL_SERVER_URL=https://relayer.memory.walrus.xyz
MEMWAL_NAMESPACE=goalstar-workflows

TATUM_API_KEY=your_tatum_key_here

GROQ_API_KEY=your_groq_key_here
```

### 3. Run Automated Tests
These run against the real Walrus relayer and Sui mainnet, and exit non-zero on any failure:
```bash
npm run test:integration

# Also store one new certificate through Tatum and verify it on chain (about 2 minutes)
npm run test:integration -- --seal
```

### 4. Start the Application
```bash
npm start
```
Open **`http://localhost:8000`** in your browser.

---

## Portable Memory in Action (CLI Tool)

The hackathon emphasizes: *"Portable memory means they pick up where they left off across tools and sessions."*

You don't need to have the web browser open to update your agent. While working in the terminal:

```bash
# Check Walrus memory stats
npm run cli -- --status

# Check the live Sui head through Tatum
npm run cli -- --sui

# Pre-seed 10 memories on Walrus Mainnet

# Log a real-time progress update or blocker from terminal:
npm run cli "Spent 3 hours debugging OAuth tokens, exhausted. Need smaller micro-steps tomorrow."
```

When you next open the web application, the **Adaptive Memory** banner automatically recalls this entry and adapts the A* path!

---

## Architecture

```
                    ┌─────────────────────────────────────────┐
                    │      Portable Terminal CLI (cli/log.js) │
                    └────────────────────┬────────────────────┘
                                         │ Logs habit progress
                                         ▼
┌───────────────────────────────┐  HTTP API   ┌─────────────────────────────────────────┐
│  GoalStar Web Interface       │◄───────────►│  Express & Agent Server (server.js)     │
│  - Interactive A* Node Graph  │             ├─────────────────────────────────────────┤
│  - Adaptive Memory Banner     │             │  • Walrus Memory Bridge (memwal.js)     │
│  - Tatum Sui Milestone Stamp  │             │  • Workflow Watchdog & Escalation Rules │
│  - Dynamic Friction Visuals   │             │  • Tatum Sui RPC Gateway Client         │
└───────────────────────────────┘             └────────────┬───────────────┬────────────┘
                                                           │               │
                                   Walrus Mainnet Relayer  │               │ Tatum Sui RPC
                                                           ▼               ▼
                                              ┌─────────────────┐ ┌─────────────────┐
                                              │  Walrus Memory  │ │  Sui Blockchain │
                                              │  (Mainnet Blobs)│ │  (Milestones)   │
                                              └─────────────────┘ └─────────────────┘
```

---

## Try every feature

Start the app with `npm start`, then run `npm run try`. It walks through real situations: why A* picks a route, a bad day changing the plan, keeping memory private, checking a certificate, and a hands-on pass through the app. Run one with `npm run try -- astar` (also `memory`, `privacy`, `proof`, `browser`).

## How memory changes the route

`lib/friction.js` turns memories into A* costs. Each step name is a semantic recall against Walrus; blockers raise that step's cost by how bad they were, wins lower it, and a newer win cancels an older blocker. The app plans the route with and without memory and shows the difference. `npm run journal` writes the project's own build journal to Mainnet.

Finished steps, slips and 48-hour stalls are written to memory automatically, and new maps are planned with it. Each person has a private namespace derived from a secret memory ID; to use the CLI, copy it from the Walrus panel and set `GOALSTAR_MEMORY_ID`.

## How a certificate is verified

Sui deprecated JSON-RPC, so GoalStar reads the chain over Tatum's native gRPC gateway (`lib/tatum.js`). Nothing falls back to a public node or a placeholder: if Tatum cannot answer, sealing fails with an error.

Sealing a milestone reads the latest checkpoint through Tatum, embeds its digest in a JSON certificate with a SHA-256 of the contents, and uploads the file to Walrus through Tatum's Storage API.

`GET /api/tatum/verify/:jobId` (`lib/certificate.js`) then re-derives every claim from Tatum and Walrus:

| Check | What it proves |
| :--- | :--- |
| Certified on Walrus | Tatum's storage job finished and the blob is certified |
| Sui transaction succeeded | The certifying transaction exists and succeeded on Sui |
| Sui object matches this blob | The onchain `Blob` object holds this exact blob id |
| Certificate content is intact | The SHA-256 recomputed from the bytes on Walrus matches |
| Anchor checkpoint matches Sui | The embedded digest is the real digest of that checkpoint |
| Timeline is consistent | The anchor checkpoint precedes the certifying transaction |

Together these bound when the certificate was created: not before the anchor checkpoint, whose digest could not be known earlier, and not after the transaction that certified it.

---

## Submission Form Values

* **Project Name**: GoalStar: Total Recall Edition
* **Selected Track**: Track 02: Smart Agents for Real Life
* **MEMWAL_AGENT_ID**: `0x49cb5c5550e8f69445a4af7ec37f2088b54ed8ce10667dc0fa03c2f503ca2cb5`
* **Special Award Target**: Best Walrus Memory ($500)
