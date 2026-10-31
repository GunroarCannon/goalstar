import sys

with open(r'C:\Users\hmmm\goalstar-recall\js\model.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Inspect current applyDream
start_idx = text.find('export function applyDream')
end_idx = text.find('export function deleteNode', start_idx)

current_apply = text[start_idx:end_idx]
print("Current applyDream:")
print(current_apply)
