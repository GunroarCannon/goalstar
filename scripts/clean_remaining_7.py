import sys, os

sys.stdout.reconfigure(encoding='utf-8')

# Clean index.html
with open('goalstar-recall/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u2726 Dream', 'Dream')
text = text.replace('\u2605 Search', 'Search')
text = text.replace('\U0001f393 Tour', 'Tour')
text = text.replace('\u2699', '')
text = text.replace('\u2699\ufe0f', '')
text = text.replace('\u2726 Detail every step', 'Detail every step')

# In settingsBtn if empty, put SVG
if '<button id="settingsBtn" class="icon" title="Settings" aria-label="Settings"></button>' in text:
    text = text.replace(
        '<button id="settingsBtn" class="icon" title="Settings" aria-label="Settings"></button>',
        '<button id="settingsBtn" class="icon" title="Settings" aria-label="Settings"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></button>'
    )

with open('goalstar-recall/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Clean js/tour.js
with open('goalstar-recall/js/tour.js', 'r', encoding='utf-8') as f:
    tour_text = f.read()

tour_text = tour_text.replace('\u2794', '->')
tour_text = tour_text.replace('\U0001f680 Open Interactive Planner', 'Open Planner')
tour_text = tour_text.replace('\U0001f680 Start Planning', 'Start Planning')

with open('goalstar-recall/js/tour.js', 'w', encoding='utf-8') as f:
    f.write(tour_text)

print("Remaining emojis cleaned!")
