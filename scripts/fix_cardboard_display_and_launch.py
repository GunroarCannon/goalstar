import re

# 1. Update css/style.css
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Pattern for .cardboard-piece down to .cb-stamp
css_pattern = re.compile(
    r'/\* Individual Cardboard piece \*/.*?(?=\.cardboard-stamp-svg|@media|\n\n/\* ======|\Z)',
    re.DOTALL
)

new_cardboard_css = """/* Individual Cardboard piece */
.cardboard-piece {
  position: relative;
  flex: 1;
  max-width: 540px;
  min-height: 660px;
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-color: transparent !important;
  border-radius: 0;
  filter: drop-shadow(0 18px 28px rgba(35, 18, 8, 0.42));
  box-shadow: none !important;
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  color: #1a0e05;
  transition: transform 1.1s cubic-bezier(0.18, 0.9, 0.28, 1), opacity 0.9s ease;
  will-change: transform, opacity;
  box-sizing: border-box;
}

/* Walrus Cardboard: High-res cardboard-1 (padded away from left corrugated tear) */
.cardboard-piece.walrus-cardboard {
  background-image: url('../assets/cardboards/cardboard-1.png');
  transform: translate3d(-140vw, -30px, 0) rotate(-45deg);
  opacity: 0;
  padding: 68px 46px 54px 74px;
}

/* Tatum Cardboard: High-res cardboard-2 (padded away from left corrugated tear) */
.cardboard-piece.tatum-cardboard {
  background-image: url('../assets/cardboards/cardboard-2.png');
  transform: translate3d(140vw, 30px, 0) rotate(45deg);
  opacity: 0;
  padding: 68px 52px 54px 68px;
}

/* Entered state: covering the engraved Walrus X Tatum */
.cardboard-stage-wrap.cards-entered .walrus-cardboard {
  transform: translate3d(0, 0, 0) rotate(-2.2deg);
  opacity: 1;
}

.cardboard-stage-wrap.cards-entered .tatum-cardboard {
  transform: translate3d(0, 0, 0) rotate(2.8deg);
  opacity: 1;
}

/* Dim the engraved centerpiece slightly when cards cover it */
.cardboard-stage-wrap.cards-entered .engraved-centerpiece {
  opacity: 0.12;
  transform: translate(-50%, -50%) scale(0.97);
}

/* Cardboard Tape Accents - positioned firmly ON the cardboard body */
.cardboard-tape {
  position: absolute;
  width: 95px;
  height: 28px;
  background: rgba(245, 235, 215, 0.82);
  border-left: 2px dashed rgba(160, 130, 90, 0.55);
  border-right: 2px dashed rgba(160, 130, 90, 0.55);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.25);
  z-index: 10;
  pointer-events: none;
}
.cardboard-tape.top-left {
  top: 18px;
  left: 78px;
  transform: rotate(-4deg);
}
.cardboard-tape.top-right {
  top: 18px;
  right: 78px;
  transform: rotate(5deg);
}

/* Etched text styling - Crisp, Dark, Highly Readable */
.cb-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.cb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.cb-tag {
  font-family: 'Space Grotesk', monospace;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.12em;
  color: #241103;
}

.cb-badge {
  font-family: 'Space Grotesk', monospace;
  font-size: 10.5px;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 4px;
  letter-spacing: 0.08em;
  border: 1.5px solid #1a0b02;
}
.cb-badge.live-active {
  background: rgba(5, 150, 105, 0.22);
  color: #044333;
}
.cb-badge.live-sui {
  background: rgba(2, 132, 199, 0.22);
  color: #034b73;
}

.cb-title {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-size: 23px;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: #120701;
  margin: 0 0 6px;
}

.cb-meta {
  font-family: 'Courier Prime', Courier, monospace;
  font-size: 12.5px;
  font-weight: 700;
  color: #381a06;
  margin-bottom: 14px;
}

.cb-rule {
  color: rgba(50, 25, 8, 0.45);
  font-size: 11px;
  letter-spacing: -0.05em;
  margin-bottom: 14px;
  user-select: none;
}

.cb-telemetry-box {
  background: rgba(40, 20, 8, 0.08);
  border: 1.5px dashed rgba(60, 30, 10, 0.45);
  border-radius: 6px;
  padding: 10px 14px;
  margin-bottom: 16px;
}

.cb-telemetry-title {
  font-family: 'Space Grotesk', monospace;
  font-size: 11.5px;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #120701;
  margin-bottom: 3px;
}

.cb-telemetry-status {
  font-family: 'Space Grotesk', monospace;
  font-size: 11px;
  color: #2b1405;
  font-weight: 700;
}

.cb-spec-list {
  list-style: none;
  padding: 0;
  margin: 0 0 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex-grow: 1;
}

.cb-spec-list li {
  position: relative;
  padding-left: 20px;
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  font-size: 13.5px;
  line-height: 1.52;
  color: #150902;
  font-weight: 600;
}

.cb-bullet {
  position: absolute;
  left: 0;
  top: 1px;
  color: #92400e;
  font-weight: 900;
}

.cb-spec-list strong {
  color: #0b0400;
  font-weight: 800;
}

.cb-spec-list code {
  font-family: 'Courier Prime', monospace;
  background: rgba(30, 15, 5, 0.12);
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: 700;
  color: #0b0400;
}

.cb-footer {
  margin-top: auto;
  padding-top: 14px;
  border-top: 1.5px dashed rgba(60, 30, 10, 0.35);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Space Grotesk', monospace;
  font-size: 11.5px;
  font-weight: 700;
  color: #261103;
}

.cb-stamp {
  font-size: 10px;
  font-weight: 800;
  border: 1.5px solid #261103;
  padding: 2px 7px;
  border-radius: 3px;
  letter-spacing: 0.08em;
}

"""

if css_pattern.search(css):
    css = css_pattern.sub(new_cardboard_css, css)
    with open('css/style.css', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(css)
    print('[OK] Updated css/style.css with readable cardboard styling.')
else:
    print('[ERR] css_pattern not matched in css/style.css')

# 2. Update home.html: fix launchPlanner URL redirection
with open('home.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_launch = """    // Launch action
    function launchPlanner(targetGoal = null) {
      sound.play('click');
      if (!auth.isLoggedIn()) {
        auth.connectGuest();
      }
      setTimeout(() => {
        if (targetGoal) {
          window.location.href = '/?goal=';
        } else {
          window.location.href = '/';
        }
      }, 50);
    }"""

fixed_launch = """    // Launch action
    function launchPlanner(targetGoal = null) {
      sound.play('click');
      if (!auth.isLoggedIn()) {
        auth.connectGuest();
      }
      setTimeout(() => {
        if (targetGoal) {
          window.location.href = '/?goal=' + encodeURIComponent(targetGoal);
        } else {
          window.location.href = '/';
        }
      }, 50);
    }"""

html_norm = html.replace('\r\n', '\n')
target_launch_norm = target_launch.replace('\r\n', '\n')
if target_launch_norm in html_norm:
    html_norm = html_norm.replace(target_launch_norm, fixed_launch)
    with open('home.html', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(html_norm)
    print('[OK] Fixed launchPlanner targetGoal URL construction in home.html.')
else:
    print('[ERR] target_launch not found in home.html')
