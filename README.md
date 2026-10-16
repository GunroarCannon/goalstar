# goalstar ★

A* pathfinding for life goals. You describe where you are and where you want to be. A **dreamer** (Claude, a local model, your own plugin, or the built-in offline one) invents the states in between and the actions that connect them. A* then finds the cheapest route based on what you care about: time, money, effort and risk.

It's one static site with no build step and no server. Everything is saved in your browser, and you can optionally sync it to a secret GitHub Gist.

## Run it

ES modules need http, not `file://`:

```bash
cd goalstar
python -m http.server 8000      # or: npx serve
# open http://localhost:8000
```

## Host it (free)

- **GitHub Pages:** push this folder to a repo, then go to Settings → Pages → Deploy from branch → `main` / root. Your site is at `https://<you>.github.io/<repo>/`.
- **Cloudflare Pages / Netlify:** drag and drop the folder. There's no build command.

The site holds no secrets. API keys and tokens live only in each browser's localStorage.

## Where the data lives

| Layer | What | Cost |
|---|---|---|
| localStorage | Always on; it's the source of truth on each device | free |
| Secret GitHub Gist | ⟳ button / auto-sync. Newest copy of each goal wins, and deletes sync too | free, no expiry, versioned |
| Export / Import JSON | Manual backups | free |

To set up sync, create a GitHub **classic token** with only the `gist` scope (github.com/settings/tokens) and paste it into Settings → Cloud sync. The first sync creates the gist. Paste the same gist id on your other devices. Keys and tokens are never uploaded.

## The model

- **States** (cards) are situations that become true, like "Visa approved". The start card is *you are here*.
- **Actions** (arrows) are what you do to move between states. Each one is rated 0–10 for time, money, effort and risk.
- **Edge cost** is the weighted average of those ratings, using the sliders under *What matters to you*.
- **h** on a card is the dreamer's estimate of the cost still left to reach the goal. It's A*'s heuristic.
- **g** is the cost so far from whatever you've already achieved. Ticking a card ✓ makes it a new starting point, so the path and *Do next* move forward with you.

### Buttons

- **✦ Dream map:** generates a whole map from start to goal, with alternative routes, in one call.
- **★ Search:** *lazy A\**, where the dreamer is the successor function. It runs A* over the current map. If no path reaches the goal, it asks the dreamer to expand the most promising unexpanded state (lowest g + h, leaves first) and repeats until a path exists or the budget runs out. Each expansion is animated.
- **✦ Dream next states** (select a card) expands just that state.
- **✦ Break into smaller steps** (select an arrow) replaces one action with a chain of smaller ones.
- Double-click the paper to add a state. Select a card and use **Link →** to draw an action by hand. Delete/Backspace removes the selection.

## Dreamers

| Dreamer | Needs | Notes |
|---|---|---|
| Offline | nothing | Keyword templates (moving abroad, app launch, money, fitness, career, learning, generic), with exact h values. Also used as the automatic fallback. |
| Groq | a free API key from console.groq.com | Fast hosted open models over Groq's OpenAI-style endpoint, in JSON mode. Default is `openai/gpt-oss-20b`; `openai/gpt-oss-120b` gives better plans. The free tier is rate-limited, so goalstar waits and retries automatically. |
| Claude | an API key from console.anthropic.com | Calls the API straight from your browser with the official SDK, using a strict JSON schema for output. Default model is `claude-opus-5-5`; Sonnet 5.5 and Haiku 5.5 are cheaper. |
| Ollama | [Ollama](https://ollama.com) + a pulled model | Fully offline. When the site isn't served from localhost, allow its origin: `OLLAMA_ORIGINS=https://<you>.github.io ollama serve` (on Windows: `setx OLLAMA_ORIGINS https://<you>.github.io`, then restart Ollama). |
| Webhook | any URL | Your own plugin. See below. |

If a dreamer fails (no network, bad key…), goalstar falls back to the offline dreamer and tells you. You can turn this off in Settings.

### Write your own dreamer

**As a webhook.** goalstar POSTs `{ request, schema }` and expects `{ states, actions }` back:

```jsonc
// request (parameters in)
{
  "mode": "dream" | "expand" | "breakdown",
  "goal":  { "label": "Live in Canada", "note": "" },
  "start": { "label": "Now: dev in Lagos", "note": "3 yrs exp, some savings" },
  "constraints": "Budget $5k",
  "focus": { "node": { "id": "n_ab12", "label": "...", "h": 12 } }   // expand
        // { "edge": { "label": "...", "from": "...", "to": "...", "cost": {...} } } // breakdown
        // null                                                            // dream
  "existing": [{ "id": "n_ab12", "label": "...", "kind": "state", "done": false }],
  "params": { "maxStates": 8, "weights": { "time": 1, "money": 1, "effort": 1, "risk": 1 } }
}

// result (parameters out)
{
  "states":  [{ "key": "s1", "label": "Job offer in hand", "note": "", "h": 14 }],
  "actions": [{ "from": "START", "to": "s1", "label": "Apply to 30 sponsoring employers",
                "note": "", "time": 6, "money": 1, "effort": 7, "risk": 6 }]
}
```

In `from`/`to` you can use `START`, `GOAL`, `HERE` (expand), `FROM`/`TO` (breakdown), an existing node id, or a key from `states`. Here's a minimal Python plugin:

```python
# pip install flask flask-cors
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__); CORS(app)

@app.post("/dream")
def dream():
    req = request.json["request"]
    return jsonify(states=[{"key": "s1", "label": "First step done", "note": "", "h": 5}],
                   actions=[{"from": "HERE" if req["mode"] == "expand" else "START", "to": "s1",
                             "label": "Take the first step", "note": "", "time": 2, "money": 0, "effort": 3, "risk": 1},
                            {"from": "s1", "to": "GOAL", "label": "Finish", "note": "", "time": 5, "money": 2, "effort": 5, "risk": 3}])

app.run(port=8787)
```

**As a module.** Add a file in `js/dreamers/` that exports `{ id, name, async generate(request, params) }` and register it in `js/dreamers/index.js`. Add a settings pane in `index.html` if it needs parameters (`name="<id>.<param>"` inputs bind automatically).

## Files

```
index.html            UI shell
css/style.css         lined-paper look
js/app.js             wiring: boards, inspector, dreaming, lazy A* search, sync
js/model.js           data model, localStorage, merging dreamer output
js/astar.js           A*, edge cost, next actions, h estimation
js/layout.js          left-to-right layered layout
js/render.js          pan/zoom canvas, cards and inked arrows
js/sync.js            GitHub Gist sync + merge
js/dreamers/          protocol (schema + prompt), offline, claude, ollama, webhook
```
