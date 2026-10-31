import re

def verify():
    with open('home.html', 'r', encoding='utf-8') as f:
        html = f.read()

    with open('js/app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()

    errors = []

    # 1. Hero text check
    if "GoalStar maps the path between where you are right now and where you want to be." not in html:
        errors.append("Hero description not updated with humanized text")
    if "Runs A* over your own weights" in html:
        errors.append("Old robotic text still present in hero")

    # 2. Simulator check
    if 'sim-preset-btn' not in html:
        errors.append("Simulator preset buttons missing")
    if 'data-preset="raise"' not in html:
        errors.append("Raise preset missing in simulator")
    if 'data-preset="dating"' not in html:
        errors.append("Dating preset missing in simulator")

    # 3. Scenarios check
    if 'STEP 01' in html or 'STEP 02' in html or 'STEP 05' in html:
        errors.append("Found old STEP XX badges in home.html")
    if 'The Career Climber' not in html:
        errors.append("Career Climber scenario missing")
    if 'The Global Dreamer' not in html:
        errors.append("Global Dreamer scenario missing")
    if 'Map Your Own Goal' not in html:
        errors.append("Card 5 Map Your Own Goal missing")
    if 'customGoalInput' not in html:
        errors.append("customGoalInput missing in Card 5")

    # 4. Modal check
    if 'PART 1 OF 5' in html:
        errors.append("Old 'PART 1 OF 5' still in modal")
    if 'STAGE 1' not in html:
        errors.append("Modal STAGE 1 missing")
    if 'custom: {' not in html:
        errors.append("Custom scenario missing in scenarioData")

    # 5. js/app.js goal param check
    if 'goalParam' not in app_js:
        errors.append("goalParam handling missing in js/app.js")

    if errors:
        print("[FAIL] Verification errors found:")
        for e in errors:
            print("  - " + e)
        return False
    else:
        print("[PASS] All relatable updates verified successfully!")
        return True

if __name__ == '__main__':
    verify()
