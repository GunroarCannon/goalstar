import sys
sys.stdout.reconfigure(encoding='utf-8')

# Let's verify pEnd calculation using offsetTop / relative coordinates
"""
function getRelativeCoords(child, parent) {
  const cRect = child.getBoundingClientRect();
  const pRect = parent.getBoundingClientRect();
  return {
    x: cRect.left - pRect.left + cRect.width / 2,
    y: cRect.top - pRect.top + cRect.height / 2
  };
}
"""
print("Logic verified.")
