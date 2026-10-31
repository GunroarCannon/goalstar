import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect home.html structure
with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# Verify that humaaans assets exist
humaaans = [
    'assets/humaaans/webp/hu_stand_24.webp',
    'assets/humaaans/webp/hu_sit_1.webp',
    'assets/humaaans/webp/hu_stand_11.webp',
    'assets/humaaans/webp/hu_stand_16.webp',
    'assets/humaaans/webp/hu_sit_6.webp',
    'assets/humaaans/webp/hu_stand_2.webp',
]
for h in humaaans:
    full_path = os.path.join('goalstar-recall', h)
    if not os.path.exists(full_path):
        print(f"Warning: {full_path} missing")
print("Assets verified!")
