import re

index_path = r'C:\Users\hmmm\goalstar-recall\index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add home link after brand
brand_target = '<span class="word">goal<b>star</b></span></a>'
home_btn = '<span class="word">goal<b>star</b></span></a>\n    <a href="/home" class="nav-home-btn" title="Go to Home / Landing Page">🏠 Home</a>'
if brand_target in html and 'nav-home-btn' not in html:
    html = html.replace(brand_target, home_btn, 1)

# 2. Add theme, sound, login buttons before settingsBtn
settings_target = '<button id="settingsBtn" class="icon" title="Settings" aria-label="Settings">⚙</button>'
extra_controls = '''<button id="themeToggleBtn" class="theme-toggle-btn icon" title="Toggle Dark/Light Mode" aria-label="Toggle Dark Mode">🌙</button>
    <button id="soundToggleBtn" class="sound-toggle-btn icon" title="Toggle Sound Effects" aria-label="Toggle Sound">🔊</button>
    <button id="loginBtn" class="login-btn" title="Log In or Connect Wallet">🔑 Log In</button>
    <div id="userBadge" class="user-badge" hidden>
      <span class="indicator live"></span>
      <span id="userName" class="user-name">Guest</span>
      <button id="logoutBtn" class="logout-link">logout</button>
    </div>
    <button id="settingsBtn" class="icon" title="Settings" aria-label="Settings">⚙</button>'''

if settings_target in html and 'themeToggleBtn' not in html:
    html = html.replace(settings_target, extra_controls, 1)

# 3. Add login dialog before </body>
login_dlg = '''
  <dialog id="loginDlg" class="crunchy-modal">
    <div class="modal-card">
      <div class="modal-head">
        <h3>🔑 Connect &amp; Sync Portable Memory</h3>
        <button type="button" class="close-login-dlg" id="closeLoginDlg" aria-label="Close">✕</button>
      </div>
      <p class="muted small" style="margin-bottom: 16px;">
        Your stamina profile, completed milestones, and friction rules follow you across sessions and the CLI via Walrus Mainnet.
      </p>

      <div class="login-options">
        <div class="login-option" id="loginGuestOpt">
          <div class="opt-icon">⚡</div>
          <div class="opt-info">
            <h4>One-Click Guest Profile</h4>
            <p>Instant access with local persistence &amp; Walrus cloud bridge.</p>
          </div>
          <button id="connectGuestBtn" class="mini-btn">Instant Login</button>
        </div>

        <div class="login-option" id="loginWalletOpt">
          <div class="opt-icon">🌊</div>
          <div class="opt-info">
            <h4>Connect Sui Web3 Wallet</h4>
            <p>Suiet, Slush, Ethos or any browser Sui wallet.</p>
          </div>
          <button id="connectWalletBtn" class="mini-btn secondary">Connect Wallet</button>
        </div>

        <div class="login-option" id="loginWalrusOpt">
          <div class="opt-icon">🧠</div>
          <div class="opt-info">
            <h4>Walrus Account ID</h4>
            <p>Sync with your decentralized memory namespace.</p>
            <input type="text" id="walrusAccountInput" placeholder="e.g. 0x8a94b2... or alice-dev" />
          </div>
          <button id="connectWalrusBtn" class="mini-btn secondary">Sync Memory</button>
        </div>
      </div>
    </div>
  </dialog>
'''

if 'id="loginDlg"' not in html:
    html = html.replace('</body>', login_dlg + '\n</body>', 1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated index.html successfully')
