path = r'C:\Users\hmmm\goalstar-recall\home.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old_launch = '''    function launchPlanner() {
      sound.play('click');
      if (!auth.isLoggedIn()) {
        auth.connectGuest();
      } else {
        window.location.href = '/';
      }
    }'''

new_launch = '''    function launchPlanner() {
      sound.play('click');
      if (!auth.isLoggedIn()) {
        auth.connectGuest();
      }
      setTimeout(() => {
        window.location.href = '/';
      }, 50);
    }'''

if old_launch in c:
    c = c.replace(old_launch, new_launch, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated launchPlanner in home.html')
