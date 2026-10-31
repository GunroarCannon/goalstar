# GoalStar: Total Recall Edition

> **Autonomous Habit & Workflow Watchdog Agent** with Walrus Portable Memory on Mainnet & Tatum Sui RPC Gateway.
> Built for the **Total Recall Hackathon** — *Track 02: Smart Agents for Real Life*.

---

## The Pitch: Apps That Remember Last Tuesday

Traditional habit and goal planners fail because they are **static to-do lists**. When life gets messy (long shifts, burnout, technical roadblocks), users miss 2 days, feel guilty, and abandon the app.

**GoalStar Total Recall Edition** transforms goal pathfinding into an **autonomous workflow watchdog** that remembers your real-world stamina, friction points, and past struggles across tools and sessions.

* **Portable Memory Across Tools**: Your memory lives on **Walrus Mainnet** via a portable Agent ID. Log blockers from your terminal CLI while coding (`npm run cli "Blocked on Docker setup"`), and your desktop GoalStar map picks up right where you left off.
* **Remembers Last Tuesday**: The agent recalls: *"Last Tuesday you spent 4 hours fighting Kubernetes configs and quit."*
* **Learns Your Escalation Rules**: When a task stalls for >48 hours, the agent automatically decomposes monolithic tasks into 15-minute micro-steps (`breakdown` dreamer mode).
* **Visibly Changes the Product ($500 Best Walrus Memory Bonus)**: A* pathfinding doesn't just calculate theoretical costs; it applies dynamic friction penalties from Walrus Mainnet. **The A* path physically reroutes on screen around your personal friction patterns!**
* **Verifiable Milestones on Sui (Tatum Gateway)**: Achieved milestones are stamped on the Sui blockchain using Tatum's Sui RPC, providing immutable proof-of-streak.

---

## Hackathon Checklist Alignment

| Total Recall Requirement | How GoalStar Delivers |
| :--- | :--- |
| **01. Walrus Memory on Mainnet** | Fully integrated using `@mysten-incubation/memwal` writing directly to `https://relayer.memory.walrus.xyz`. |
| **02. Tatum RPC for Onchain Data** | Connected to Tatum's Sui Gateway (`https://api.tatum.io/v3/blockchain/node/sui-mainnet`) for live checkpoint and milestone proof verification. |
| **03. At Least 10 Memories on Mainnet** | Built-in 1-click seeder (`npm run cli --seed` or UI button) storing 10 realistic habit velocity and blocker memories on Walrus Mainnet. |
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
MEMWAL_ACCOUNT_ID=0x49cb5c5550e8f69445a4af7ec37f2088b54ed8ce10667dc0fa03c2f503ca2cb5
MEMWAL_PRIVATE_KEY=f6987e903219defd0811f8f21f45393b069a54fb3cd73dc61a4e669011fda562
MEMWAL_SERVER_URL=https://relayer.memory.walrus.xyz
MEMWAL_NAMESPACE=goalstar-workflows

TATUM_API_KEY=your_tatum_key_here
TATUM_SUI_RPC_URL=https://api.tatum.io/v3/blockchain/node/sui-mainnet

GROQ_API_KEY=your_groq_key_here
```

### 3. Run Automated Tests
Verify Walrus Mainnet connectivity and Tatum RPC:
```bash
npm run test:integration
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
npm run cli --status

# Check Tatum Sui RPC gateway state
npm run cli --sui

# Pre-seed 10 memories on Walrus Mainnet
npm run cli --seed

# Log a real-time progress update or blocker from terminal:
npm run cli "Spent 3 hours debugging OAuth tokens, exhausted. Need smaller micro-steps tomorrow."
```

When you next open the web application, the **"Remembered Last Tuesday"** banner automatically recalls this entry and adapts the A* path!

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
│  - "Remembered Last Tuesday"  │             │  • Walrus Memory Bridge (memwal.js)     │
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

## Submission Form Values

* **Project Name**: GoalStar: Total Recall Edition
* **Selected Track**: Track 02: Smart Agents for Real Life
* **MEMWAL_AGENT_ID**: `0x49cb5c5550e8f69445a4af7ec37f2088b54ed8ce10667dc0fa03c2f503ca2cb5`
* **Special Award Target**: Best Walrus Memory ($500)
