import { walrusMemory } from './walrus-memory.js';
// Floating planning-agent chat.
//
// The panel is injected by this module so the app markup stays unchanged. It
// sends the open goal's map to the server-side agent and applies the structured
// edits (rename, complete, invalidate, re-link, re-plan) the agent returns.
//
// The agent runs on the app server: `npm start`, then open the planner.

const SUGGESTIONS = [
  'Mark the first milestone as done',
  'Rename the slowest action to something concrete',
  'Remove the route I am not going to take',
  'Restructure: jump from my current state to the goal in two steps',
];

const ESC = (s) =>
  String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export function initAgentChat({ getContext, applyOps, onEdit } = {}) {
  if (typeof document === 'undefined') return null;
  if (document.querySelector('.agent-chat')) return null;

  const wrap = document.createElement('div');
  wrap.className = 'agent-chat';
  wrap.innerHTML = `
    <button type="button" class="agent-fab" aria-haspopup="dialog" aria-expanded="false"
      title="Ask the agent to edit this goal: rename, complete, invalidate or restructure the route">
      <span class="agent-fab-dot" aria-hidden="true"></span>
      <span class="agent-fab-label">Ask agent</span>
    </button>
    <section class="agent-panel" role="dialog" aria-label="GoalStar planning agent" hidden>
      <header class="agent-head">
        <div class="agent-head-text">
          <div class="agent-head-row">
            <span class="agent-tag">Planning agent</span>
            <span class="agent-walrus-pill" title="Walrus portable memory active"><span class="walrus-dot"></span> WALRUS ACTIVE</span>
          </div>
          <h3>Edit this goal in words</h3>
          <div class="agent-target-indicator" id="agentTargetPill" style="display:none;"></div>
        </div>
        <button type="button" class="agent-close" aria-label="Close">&times;</button>
      </header>
      <div class="agent-log" role="log" aria-live="polite"></div>
      <div class="agent-suggest"></div>
      <form class="agent-form">
        <textarea class="agent-input" rows="2" placeholder="e.g. I finished the API spec — mark it done and drop the Kubernetes branch"></textarea>
        <button type="submit" class="agent-send">Send</button>
      </form>
      <p class="agent-foot">Edits apply to the open goal and save locally. The agent runs on the app server.</p>
    </section>`;

  document.body.appendChild(wrap);

  const fab = wrap.querySelector('.agent-fab');
  const panel = wrap.querySelector('.agent-panel');
  const log = wrap.querySelector('.agent-log');
  const form = wrap.querySelector('.agent-form');
  const input = wrap.querySelector('.agent-input');
  const sendBtn = wrap.querySelector('.agent-send');
  const suggest = wrap.querySelector('.agent-suggest');

  suggest.innerHTML = SUGGESTIONS.map((t) => `<button type="button" class="agent-chip">${ESC(t)}</button>`).join('');

  let open = false;
  let busy = false;

  const addMsg = (role, text, kind = '') => {
    const el = document.createElement('div');
    el.className = `agent-msg ${role}${kind ? ' ' + kind : ''}`;
    el.textContent = text;
    log.append(el);
    log.scrollTop = log.scrollHeight;
  };

  const addNote = (lines, kind = '') => {
    const el = document.createElement('div');
    el.className = `agent-msg note${kind ? ' ' + kind : ''}`;
    el.innerHTML = lines.map((l) => `<span>${ESC(l)}</span>`).join('');
    log.append(el);
    log.scrollTop = log.scrollHeight;
  };

  function setOpen(next) {
    open = next;
    panel.hidden = !open;
    fab.setAttribute('aria-expanded', String(open));
    wrap.classList.toggle('open', open);
    if (open) {
      const targetPill = wrap.querySelector('#agentTargetPill');
      const ctx = getContext?.();
      if (targetPill && ctx?.targetNodeLabel) {
        targetPill.style.display = 'block';
        targetPill.innerHTML = `Target milestone: <strong>${ESC(ctx.targetNodeLabel)}</strong>`;
      } else if (targetPill) {
        targetPill.style.display = 'none';
      }
      if (!log.childElementCount) {
        addMsg('agent', 'Tell me what changed or what to restructure. I can rename or invalidate milestones and actions, mark things complete, re-link steps, or branch out from any milestone using Walrus memory.');
      }
      setTimeout(() => input.focus(), 60);
    }
  }

  async function send(text) {
    const message = text.trim();
    if (!message || busy) return;
    const ctx = getContext?.();
    if (!ctx) {
      addMsg('agent', 'Open or create a goal first, then I can edit its map.', 'err');
      return;
    }

    addMsg('user', message);
    input.value = '';
    busy = true;
    sendBtn.disabled = true;
    sendBtn.textContent = 'Thinking…';

    try {
      const res = await fetch('/api/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...walrusMemory.identityHeaders() },
        body: JSON.stringify({ message, board: ctx }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || `Agent request failed (${res.status})`);

      addMsg('agent', data.reply || 'Done.');
      if (data.walrus?.recalls?.length) {
        addNote(data.walrus.recalls.map((r) => `🧠 Walrus Memory: ${r}`), 'walrus');
      }
      const ops = Array.isArray(data.ops) ? data.ops : [];
      if (ops.length) {
        const out = await applyOps?.(ops);
        if (out?.ok?.length) addNote(out.ok);
        if (out?.fail?.length) addNote(out.fail, 'warn');
        onEdit?.(out);
      }
    } catch (err) {
      addMsg('agent', `${err.message}\n\nThe edit agent runs on the app server — start it with “npm start” and reload.`, 'err');
    } finally {
      busy = false;
      sendBtn.disabled = false;
      sendBtn.textContent = 'Send';
      input.focus();
    }
  }

  fab.addEventListener('click', () => setOpen(!open));
  wrap.querySelector('.agent-close').addEventListener('click', () => setOpen(false));

  suggest.addEventListener('click', (e) => {
    const chip = e.target.closest('.agent-chip');
    if (chip) send(chip.textContent);
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    send(input.value);
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send(input.value);
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && open && !busy) setOpen(false);
  });

  return {
    open: () => setOpen(true),
    close: () => setOpen(false),
    isOpen: () => open,
  };
}
