import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py', 'r', encoding='utf-8') as f:
    text = f.read()

print("Hero ink swash:")
idx1 = text.find('inkSwashSvg')
print(text[idx1-100:idx1+400])

print("\nCard 5 and end of journeyTrack:")
idx2 = text.find('id="card5"')
idx3 = text.find('</section>', idx2)
print(text[idx2:idx3])
