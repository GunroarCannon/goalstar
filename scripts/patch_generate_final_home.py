import os

path = r"C:\Users\hmmm\goalstar-recall\scripts\generate_final_home.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

norm_text = text.replace("\r\n", "\n")

target = """    document.querySelectorAll('#heroTourBtn, #navTourBtn').forEach(btn => {
      btn.addEventListener('click', () => {
        sound.play('pop');
        currentHomeStep = 0;
        renderHomeTour();
        tourModal.hidden = false;
      });
    });"""

replacement = """    function stopHomeTourBounce() {
      try { localStorage.setItem('goalstar_tour_clicked', 'true'); } catch(e) {}
      document.querySelectorAll('.tour-bounce-btn').forEach(b => b.classList.remove('tour-bounce-btn'));
    }
    if (localStorage.getItem('goalstar_tour_clicked') === 'true' || localStorage.getItem('goalstar_walkthrough_completed') === 'true') {
      stopHomeTourBounce();
    }

    document.querySelectorAll('#heroTourBtn, #navTourBtn').forEach(btn => {
      btn.addEventListener('click', () => {
        stopHomeTourBounce();
        sound.play('pop');
        currentHomeStep = 0;
        renderHomeTour();
        tourModal.hidden = false;
      });
    });"""

if target in norm_text:
    norm_text = norm_text.replace(target, replacement)
    with open(path, "w", encoding="utf-8") as f:
        f.write(norm_text)
    print("Updated generate_final_home.py successfully")
else:
    print("Target not found or already updated in generate_final_home.py")
