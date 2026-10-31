import sys

with open(r'C:\Users\hmmm\goalstar-recall\scripts\test_final_experience.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('#walkthroughStepBadge', '#scenarioStepNum')
code = code.replace('#walkthroughNextBtn', '#nextScenarioStepBtn')
code = code.replace('#walkthroughLaunchBtn', '#openFullPlannerBtn')

with open(r'C:\Users\hmmm\goalstar-recall\scripts\test_final_experience.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated test_final_experience.py with exact scenario modal IDs!")
