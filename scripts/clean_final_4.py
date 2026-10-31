import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('goalstar-recall/index.html', 'r', encoding='utf-8') as f:
    idx_lines = f.readlines()

for i in range(len(idx_lines)):
    # line 29: dreamBtn
    if 'id="dreamBtn"' in idx_lines[i]:
        idx_lines[i] = '      <button id="dreamBtn" class="primary engraved-btn" title="Generate states and actions with an AI dreamer">Dream</button>\n'
    # line 30: searchBtn
    if 'id="searchBtn"' in idx_lines[i]:
        idx_lines[i] = '      <button id="searchBtn" class="gold engraved-btn" title="A* search for the lowest-cost path from START to GOAL">Search</button>\n'
    # line 33: tourBtn
    if 'id="tourBtn"' in idx_lines[i]:
        idx_lines[i] = '      <button id="tourBtn" class="tour-nav-btn engraved-btn" title="Take a visual walkthrough of Total Recall features">Tour</button>\n'

with open('goalstar-recall/index.html', 'w', encoding='utf-8') as f:
    f.writelines(idx_lines)

with open('goalstar-recall/js/tour.js', 'r', encoding='utf-8') as f:
    tour_lines = f.readlines()

for i in range(len(tour_lines)):
    if 'id="tourNextBtn"' in tour_lines[i]:
        tour_lines[i] = "      <button class=\"sketch-btn primary\" id=\"tourNextBtn\">${isLast ? 'Finish Tour' : 'Next'}</button>\n"

with open('goalstar-recall/js/tour.js', 'w', encoding='utf-8') as f:
    tour_lines = [l.replace('\u2794', '->').replace('\U0001f680', '') for l in tour_lines]
    f.writelines(tour_lines)

print("Final 4 cleaned!")
