import os

path = r"C:\Users\hmmm\goalstar-recall\js\render.js"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

target = """  centerOn(id, animate = true) {
    const n = this.board?.nodes[id];
    if (!n) return;
    const s = this.sizes[id] || { w: CARD_W, h: 80 };
    const W = this.root.clientWidth, H = this.root.clientHeight, k = this.view.k;
    this.setView({ k, x: W / 2 - (n.x + s.w / 2) * k, y: H / 2 - (n.y + s.h / 2) * k }, animate);
  }
}"""

replacement = """  centerOn(id, animate = true) {
    const n = this.board?.nodes[id];
    if (!n) return;
    const s = this.sizes[id] || { w: CARD_W, h: 80 };
    const W = this.root.clientWidth, H = this.root.clientHeight, k = this.view.k;
    const sideOffset = window.innerWidth > 900 ? 110 : 0;
    this.setView({ k, x: (W / 2 + sideOffset) - (n.x + s.w / 2) * k, y: H / 2 - (n.y + s.h / 2) * k }, animate);
  }

  centerOnEdge(edgeId, animate = true) {
    const e = this.board?.edges[edgeId];
    if (!e) return;
    const a = this.board.nodes[e.from], b = this.board.nodes[e.to];
    if (!a || !b) return;
    const sa = this.sizes[e.from] || { w: CARD_W, h: 80 }, sb = this.sizes[e.to] || { w: CARD_W, h: 80 };
    const midX = (a.x + sa.w + b.x) / 2;
    const midY = (a.y + sa.h / 2 + b.y + sb.h / 2) / 2;
    const W = this.root.clientWidth, H = this.root.clientHeight, k = this.view.k;
    const sideOffset = window.innerWidth > 900 ? 110 : 0;
    this.setView({ k, x: (W / 2 + sideOffset) - midX * k, y: H / 2 - midY * k }, animate);
  }
}"""

norm_text = text.replace("\r\n", "\n")
norm_target = target.replace("\r\n", "\n")
assert norm_target in norm_text, "Target not found in render.js"

updated = norm_text.replace(norm_target, replacement.replace("\r\n", "\n"))
with open(path, "w", encoding="utf-8") as f:
    f.write(updated)
print("Updated render.js successfully")
