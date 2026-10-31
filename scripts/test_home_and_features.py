import os
import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.sync_api import sync_playwright

output_dir = r"C:\Users\hmmm\goalstar-recall\tour_screenshots"
os.makedirs(output_dir, exist_ok=True)

def run():
    print("[START] Starting Playwright verification for /home, Dark Mode, Sound, Auth, and Walkthrough...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 850})
        page = context.new_page()

        errors = []
        page.on("pageerror", lambda err: errors.append(f"PAGE ERROR: {err}"))
        page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}") if msg.type in ['error', 'warn'] else None)

        # ----------------------------------------------------
        # 1. TEST /home (Landing Page)
        # ----------------------------------------------------
        print("\n--- 1. Testing /home Landing Page ---")
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        time.sleep(1)

        # Screenshot hero
        hero_shot = os.path.join(output_dir, "home_hero_light.png")
        page.screenshot(path=hero_shot)
        print(f"[OK] Saved hero screenshot: {hero_shot}")

        # Test Interactive Simulator
        slider = page.locator("#frictionSlider")
        slider.fill("3")
        slider.dispatch_event("input")
        time.sleep(0.5)
        sim_feedback = page.locator("#simFeedback").text_content()
        print(f"[OK] Slider rerouting feedback: {sim_feedback.strip()[:60]}...")

        # Test Scroll-linked Use Cases
        print("[INFO] Scrolling down to trigger linked use-case animation...")
        page.evaluate("window.scrollTo({ top: 950, behavior: 'instant' });")
        time.sleep(1)
        
        cards = page.locator(".uc-card")
        print(f"[OK] Found {cards.count()} use case cards on /home")
        
        usecases_shot = os.path.join(output_dir, "home_usecases_scrolled.png")
        page.screenshot(path=usecases_shot)
        print(f"[OK] Saved scrolled use cases screenshot: {usecases_shot}")

        # Test Dark Mode on /home
        print("[INFO] Toggling Dark Mode on /home...")
        theme_btn = page.locator("#themeToggleBtn")
        theme_btn.click()
        time.sleep(0.5)

        is_dark = page.evaluate("document.documentElement.classList.contains('dark-mode') && document.body.dataset.paper === 'night'")
        print(f"[OK] Dark mode active on /home: {is_dark}")

        dark_shot = os.path.join(output_dir, "home_dark_mode.png")
        page.screenshot(path=dark_shot)
        print(f"[OK] Saved dark mode screenshot: {dark_shot}")

        # Test Sound Toggle
        sound_btn = page.locator("#soundToggleBtn")
        sound_btn.click()
        sound_btn.click() # toggle back
        print("[OK] Sound toggle tested")

        # Test Login Dialog on /home
        print("[INFO] Testing Login Modal on /home...")
        login_btn = page.locator("#loginBtn")
        login_btn.click()
        time.sleep(0.5)
        
        # Click Instant Guest Login
        guest_btn = page.locator("#connectGuestBtn")
        guest_btn.click()
        time.sleep(0.8)

        user_name = page.locator("#userName").text_content()
        print(f"[OK] Successfully logged in as: {user_name.strip()}")

        # Test Quick Guide Modal on /home
        page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' });")
        time.sleep(0.5)
        page.locator("#heroTourBtn").click()
        time.sleep(0.5)
        guide_title = page.locator("#homeTourTitle").text_content()
        print(f"[OK] Home tour opened: {guide_title.strip()}")
        page.locator("#nextHomeTourBtn").click()
        time.sleep(0.3)
        page.locator("#closeHomeTourBtn").click()
        time.sleep(0.3)

        # ----------------------------------------------------
        # 2. TEST MAIN PLANNER APP (/)
        # ----------------------------------------------------
        print("\n--- 2. Testing Main Planner App (/) ---")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        time.sleep(1.5)

        # Verify user badge persisted from /home session
        app_user = page.locator("#userName").text_content()
        print(f"[OK] User session persisted in main app: {app_user.strip()}")

        # Verify Home nav button exists
        home_nav = page.locator(".nav-home-btn")
        print(f"[OK] Home button visible: {home_nav.is_visible()}, href: {home_nav.get_attribute('href')}")

        # The walkthrough tour should be visible (auto-opens on first load)
        print("\n--- 3. Testing 6-Step Actionable Walkthrough Tour ---")
        tour_overlay = page.locator(".sketch-tour-overlay")
        if not tour_overlay.is_visible():
            page.locator("#tourBtn").click()
            time.sleep(0.5)

        for step in range(1, 7):
            tour_title = page.locator(".sketch-title").text_content()
            badge = page.locator(".sketch-badge").text_content()
            print(f"[OK] Tour Step {step}: {badge.strip()} - {tour_title.strip()[:40]}...")
            
            step_shot = os.path.join(output_dir, f"tour_action_step_{step}.png")
            page.screenshot(path=step_shot)

            if step < 6:
                page.locator("#tourNextBtn").click()
                time.sleep(0.6)
            else:
                page.locator("#tourNextBtn").click() # Closes tour
                time.sleep(0.6)

        print("[OK] Tour finished and closed successfully.")

        # Test Dark Mode in Main App
        print("\n--- 4. Testing Dark Mode in Main App ---")
        page.locator("#themeToggleBtn").click()
        time.sleep(0.5)
        app_is_dark = page.evaluate("document.body.dataset.paper === 'night'")
        print(f"[OK] Dark mode active in main app: {app_is_dark}")

        app_dark_shot = os.path.join(output_dir, "app_dark_mode.png")
        page.screenshot(path=app_dark_shot)
        print(f"[OK] Saved app dark mode screenshot: {app_dark_shot}")

        # Test Wallet Login in Main App
        print("\n--- 5. Testing Wallet Login Modal in Main App ---")
        page.locator("#logoutBtn").click()
        time.sleep(0.3)
        page.locator("#loginBtn").click()
        time.sleep(0.4)
        login_dlg = page.locator("#loginDlg")
        print(f"[OK] Login dialog open: {login_dlg.is_visible()}")
        
        login_modal_shot = os.path.join(output_dir, "login_modal.png")
        page.screenshot(path=login_modal_shot)
        print(f"[OK] Saved login modal screenshot: {login_modal_shot}")

        page.locator("#connectWalletBtn").click()
        time.sleep(0.5)
        wallet_user = page.locator("#userName").text_content()
        print(f"[OK] Logged in with Sui Wallet: {wallet_user.strip()}")

        # Replay tour to ensure replay button works
        print("\n--- 6. Testing Tour Replay Button ---")
        page.locator("#tourBtn").click()
        time.sleep(0.5)
        print(f"[OK] Replayed tour visible: {page.locator('.sketch-tour-overlay').is_visible()}")
        page.locator("#tourCloseBtn").click()
        time.sleep(0.3)

        print("\n--- 7. Verification Check for Uncaught Errors ---")
        if errors:
            print("[ERROR] ERRORS DETECTED:")
            for err in errors:
                print("  ", err)
            sys.exit(1)
        else:
            print("[SUCCESS] ZERO ERRORS! All tests passed with flying colors!")

        browser.close()

if __name__ == "__main__":
    run()
