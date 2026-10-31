// GoalStar Authentication & Identity Manager
// Supports Sui Web3 Wallet, Walrus Decentralized Account ID, and 1-Click Guest Profile

import { sound } from './sound.js';

export class AuthManager {
  constructor() {
    this.user = this.loadUser();
    this.dlg = null;
  }

  loadUser() {
    try {
      const saved = localStorage.getItem('goalstar_user');
      return saved ? JSON.parse(saved) : null;
    } catch (e) {
      return null;
    }
  }


  redirectIfOnHome() {
    if (typeof window !== 'undefined' && (window.location.pathname === '/home' || window.location.pathname.endsWith('/home.html'))) {
      setTimeout(() => {
        window.location.href = '/';
      }, 450);
    }
  }

  saveUser(user) {
    this.user = user;
    if (user) {
      localStorage.setItem('goalstar_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('goalstar_user');
    }
    this.updateUI();
  }

  isLoggedIn() {
    return !!this.user;
  }

  openLoginModal() {
    sound.play('pop');
    if (!this.dlg) this.dlg = document.getElementById('loginDlg') || document.getElementById('loginDialog');
    if (this.dlg) {
      if (typeof this.dlg.showModal === 'function') {
        this.dlg.showModal();
      } else {
        this.dlg.hidden = false;
        this.dlg.removeAttribute('hidden');
        this.dlg.setAttribute('open', 'true');
        this.dlg.style.display = 'flex';
      }
    }
  }

  closeLoginModal() {
    sound.play('click');
    if (!this.dlg) this.dlg = document.getElementById('loginDlg') || document.getElementById('loginDialog');
    if (this.dlg) {
      if (typeof this.dlg.close === 'function') {
        this.dlg.close();
      } else {
        this.dlg.hidden = true;
        this.dlg.setAttribute('hidden', 'true');
        this.dlg.removeAttribute('open');
        this.dlg.style.display = 'none';
      }
    }
  }

  async connectWallet() {
    sound.play('click');
    let provider = null;
    let address = null;
    let walletName = 'Sui Wallet';

    // 1. Detect browser Sui wallet providers (Sui Wallet, Suiet, Slush, Nightly, Martian)
    if (typeof window !== 'undefined') {
      if (window.suiWallet) {
        provider = window.suiWallet;
        walletName = 'Sui Wallet';
      } else if (window.suiet) {
        provider = window.suiet;
        walletName = 'Suiet';
      } else if (window.slushWallet) {
        provider = window.slushWallet;
        walletName = 'Slush Wallet';
      } else if (window.sui) {
        provider = window.sui;
        walletName = 'Sui Web3';
      } else if (window.nightly && window.nightly.sui) {
        provider = window.nightly.sui;
        walletName = 'Nightly';
      }
    }

    if (provider) {
      try {
        let accounts = [];
        if (typeof provider.requestPermissions === 'function') {
          await provider.requestPermissions();
          if (typeof provider.getAccounts === 'function') {
            accounts = await provider.getAccounts();
          }
        } else if (typeof provider.getAccounts === 'function') {
          accounts = await provider.getAccounts();
        } else if (provider.features && provider.features['standard:connect']) {
          const res = await provider.features['standard:connect'].connect();
          if (res && res.accounts && res.accounts[0]) {
            accounts = [res.accounts[0].address];
          }
        }
        if (accounts && accounts.length > 0) {
          address = accounts[0];
        }
      } catch (err) {
        console.warn('Sui wallet request rejected or failed:', err);
        if (typeof window.toast === 'function') {
          window.toast('Wallet connection rejected or cancelled.', 'warn');
        }
        return;
      }
    }

    // 2. If no browser extension detected, provide an honest prompt
    if (!address) {
      const input = prompt(
        "No Sui Web3 wallet extension (Sui Wallet, Suiet, Slush) was detected in this browser window.\n\n" +
        "You can either:\n" +
        "1. Enter your Sui address or Walrus Account ID below to sync your personalized onchain memory, OR\n" +
        "2. Cancel to keep using the gasless guest relayer."
      );
      if (input && input.trim()) {
        address = input.trim();
        walletName = 'Sui Linked';
      } else {
        if (typeof window.toast === 'function') {
          window.toast('Continuing with gasless sponsored relayer.', 'info');
        }
        return;
      }
    }

    const shortDisplay = address.length > 14 
      ? address.slice(0, 6) + '…' + address.slice(-4) 
      : address;

    const user = {
      type: 'sui_wallet',
      name: `${walletName} (${shortDisplay})`,
      address: address,
      connectedAt: new Date().toISOString()
    };
    this.saveUser(user);
    this.closeLoginModal();
    sound.play('stamp');
    if (typeof window.toast === 'function') {
      window.toast(`Connected Sui Wallet: ${shortDisplay}! Walrus Memory active.`, 'ok');
    }
  }

  connectWalrusId(customId) {
    sound.play('click');
    const id = (customId || '').trim() || 'walrus-user-' + Math.floor(1000 + Math.random() * 9000);
    const user = {
      type: 'walrus_id',
      name: id,
      address: id,
      connectedAt: new Date().toISOString()
    };
    this.saveUser(user);
    this.closeLoginModal();
    sound.play('stamp');
    if (typeof window.toast === 'function') {
      window.toast(`Logged in as ${user.name}! Syncing portable state.`, 'ok');
    }
  }

  connectEmail(email) {
    sound.play('click');
    const clean = (email || '').trim() || 'builder@goalstar.app';
    const user = {
      type: 'email',
      name: clean,
      email: clean,
      address: clean,
      connectedAt: new Date().toISOString()
    };
    this.saveUser(user);
    this.closeLoginModal();
    sound.play('stamp');
    if (typeof window.toast === 'function') {
      window.toast(`Logged in as ${clean}!`, 'ok');
    }
  }

  connectGuest() {
    sound.play('click');
    const user = {
      type: 'demo_guest',
      name: 'Guest Builder #' + Math.floor(100 + Math.random() * 900),
      address: '0x' + Math.random().toString(16).slice(2, 8),
      connectedAt: new Date().toISOString()
    };
    this.saveUser(user);
    this.closeLoginModal();
    sound.play('stamp');
    if (typeof window.toast === 'function') {
      window.toast(`Welcome ${user.name}! Ready to plan.`, 'ok');
    }
  }

  logout() {
    sound.play('click');
    this.saveUser(null);
    if (typeof window.toast === 'function') {
      window.toast('Logged out. Switched to offline guest mode.');
    }
    if (typeof window !== 'undefined' && window.location.pathname !== '/home' && !window.location.pathname.endsWith('/home.html')) {
      window.location.replace('/home');
    }
  }

  updateUI() {
    const loginBtns = document.querySelectorAll('.login-btn, #loginBtn');
    const userBadges = document.querySelectorAll('.user-badge, #userBadge');
    const userNames = document.querySelectorAll('.user-name, #userName');

    if (this.user) {
      loginBtns.forEach(btn => { btn.hidden = true; btn.style.display = 'none'; });
      userBadges.forEach(b => { b.hidden = false; b.style.display = 'inline-flex'; b.title = this.user.name; });
      let displayName = this.user.name || 'User';
      if (this.user.type === 'demo_guest') {
        displayName = this.user.name.replace('Guest Builder #', 'Guest #');
      } else if (this.user.type === 'sui_wallet') {
        displayName = this.user.address ? (this.user.address.slice(0, 6) + '…' + this.user.address.slice(-3)) : 'Sui';
      } else if (this.user.type === 'email') {
        displayName = (this.user.email || '').split('@')[0];
      }
      userNames.forEach(n => { n.textContent = displayName; });
    } else {
      loginBtns.forEach(btn => { btn.hidden = false; btn.style.display = 'inline-flex'; });
      userBadges.forEach(b => { b.hidden = true; b.style.display = 'none'; });
    }
  }

  init() {
    this.dlg = document.getElementById('loginDlg') || document.getElementById('loginDialog');

    document.querySelectorAll('.login-btn, #loginBtn, .user-badge, #userBadge').forEach(b => {
      b.addEventListener('click', (e) => {
        if (e.target.closest('#logoutBtn') || e.target.classList.contains('logout-link')) return;
        this.openLoginModal();
      });
    });

    document.querySelectorAll('.close-login-dlg, #closeLoginDlg').forEach(b => {
      b.addEventListener('click', () => this.closeLoginModal());
    });

    const submitEmail = () => {
      const input = document.getElementById('loginEmailInput');
      const val = input ? input.value.trim() : '';
      if (!val || !val.includes('@')) {
        alert('Please enter a valid email address.');
        return;
      }
      this.connectEmail(val);
      if (window.pendingGoal && typeof window.launchPlanner === 'function') {
        const g = window.pendingGoal;
        window.pendingGoal = null;
        window.launchPlanner(g);
      }
    };

    document.querySelectorAll('#loginEmailSubmitBtn, #loginEmailBtn').forEach(b => {
      b.addEventListener('click', submitEmail);
    });

    document.getElementById('loginEmailInput')?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        submitEmail();
      }
    });

    document.querySelectorAll('#connectGuestBtn, #loginGuestBtn').forEach(b => {
      b.addEventListener('click', () => {
        this.connectGuest();
        if (window.pendingGoal && typeof window.launchPlanner === 'function') {
          const g = window.pendingGoal;
          window.pendingGoal = null;
          window.launchPlanner(g);
        }
      });
    });

    document.getElementById('connectWalletBtn')?.addEventListener('click', () => this.connectWallet());
    document.getElementById('connectWalrusBtn')?.addEventListener('click', () => {
      const input = document.getElementById('walrusAccountInput');
      this.connectWalrusId(input ? input.value : '');
    });

    document.querySelectorAll('.logout-link, #logoutBtn').forEach(b => {
      b.addEventListener('click', (e) => {
        e.stopPropagation();
        this.logout();
      });
    });

    this.updateUI();
  }
}

export const auth = new AuthManager();
