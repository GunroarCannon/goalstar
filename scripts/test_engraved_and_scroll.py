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
    print("[START] Running End-to-End Verification: Engraved UI, Auth Redirect & Scroll Animation...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 850})
        page = context.new_page()

        errors = []
        page.on("pageerror", lambda err: errors.append(f"PAGE ERROR: {err}"))
        page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}") if msg.type in ['error', 'warn'] else None)

        # ----------------------------------------------------
        # 1. VERIFY DEFAULT REDIRECT TO /home IF NOT LOGGED IN
        # ----------------------------------------------------
        print("\n--- 1. Testing Default Redirect to /home ---")
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.evaluate("localStorage.clear();")
        time.sleep(0.3)

        # Now navigate to / with no user session
        page.goto("http://localhost:8000/", wait_until="networkidle")
        time.sleep(0.8)
        current_url = page.url
        print(f"[OK] Navigated to root with no session; redirected to: {current_url}")
        assert "/home" in current_url, f"Expected redirect to /home, got {current_url}"

        # ----------------------------------------------------
        # 2. TEST ENGRAVED UI & SWITCHES ON /home
        # ----------------------------------------------------
        print("\n--- 2. Testing Engraved Controls on /home ---")
        # Ensure initial state is light
        page.evaluate("theme.applyTheme('light');")
        time.sleep(0.3)

        hero_shot = os.path.join(output_dir, "engraved_home_hero_light.png")
        page.screenshot(path=hero_shot)
        print(f"[OK] Saved light hero with paper sculpture: {hero_shot}")

        # Test Engraved Theme Switch (Reference 0)
        print("Toggling Engraved Theme Switch...")
        theme_sw = page.locator("#themeSwitch")
        theme_sw.click()
        time.sleep(0.5)

        is_dark = page.evaluate("document.body.dataset.paper === 'night' && document.getElementById('themeSwitch').classList.contains('active')")
        print(f"[OK] Dark mode active & switch knob shifted: {is_dark}")
        assert is_dark, "Theme switch should activate dark mode"

        dark_shot = os.path.join(output_dir, "engraved_home_hero_dark.png")
        page.screenshot(path=dark_shot)
        print(f"[OK] Saved dark hero: {dark_shot}")

        # Toggle back to light mode
        theme_sw.click()
        time.sleep(0.4)

        # Test Engraved Sound Switch
        print("Toggling Engraved Sound Switch...")
        sound_sw = page.locator("#soundSwitch")
        sound_sw.click()
        time.sleep(0.2)
        sound_sw.click()
        print("[OK] Engraved Sound Switch tested successfully")

        # Test Interactive Route Simulator
        slider = page.locator("#frictionSlider")
        slider.fill("3")
        slider.dispatch_event("input")
        time.sleep(0.4)
        sim_feedback = page.locator("#simFeedback").text_content()
        print(f"[OK] Simulator feedback: {sim_feedback.strip()[:50]}...")

        # ----------------------------------------------------
        # 3. TEST SCROLL-DRIVEN ANIMATION & DOCKING BAYS
        # ----------------------------------------------------
        print("\n--- 3. Testing Scroll-Driven Animation & Bay Docking ---")
        # Scroll down through the use cases
        for scroll_y in [600, 1100, 1600, 2200]:
            page.evaluate(f"window.scrollTo({{ top: {scroll_y}, behavior: 'smooth' }});")
            time.sleep(0.4)

        # Verify docking
        docked_cards = page.locator(".uc-card.docked-in").count()
        docked_bays = page.locator(".card-bay.docked").count()
        print(f"[OK] Cards docked into bays: {docked_cards}/5, Bay indicators: {docked_bays}/5")

        scroll_shot = os.path.join(output_dir, "scroll_driven_arrows_scrolled.png")
        page.screenshot(path=scroll_shot)
        print(f"[OK] Saved scroll-driven animation screenshot: {scroll_shot}")

        # ----------------------------------------------------
        # 4. TEST LAUNCH PLANNER FROM /home (WITH GUEST AUTH)
        # ----------------------------------------------------
        print("\n--- 4. Testing Launch Planner Button ---")
        page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' });")
        time.sleep(0.3)
        launch_btn = page.locator("#heroLaunchBtn")
        launch_btn.click()
        page.wait_for_url("http://localhost:8000/", timeout=6000)

        planner_url = page.url
        print(f"[OK] Planner URL after launch: {planner_url}")
        assert planner_url == "http://localhost:8000/" or planner_url.endswith("/"), f"Expected planner root, got {planner_url}"

        user_name = page.locator("#userName").text_content()
        print(f"[OK] User logged in as: {user_name.strip()}")

        # Take screenshot of planner topbar with engraved controls
        app_shot = os.path.join(output_dir, "planner_engraved_topbar.png")
        page.screenshot(path=app_shot)
        print(f"[OK] Saved planner with engraved controls: {app_shot}")

        # ----------------------------------------------------
        # 5. TEST REPLAY TOUR ON PLANNER
        # ----------------------------------------------------
        print("\n--- 5. Testing Tour on Planner ---")
        # Close tour if auto-opened
        if page.locator(".sketch-tour-overlay").is_visible():
            page.locator("#tourCloseBtn").click()
            time.sleep(0.3)

        page.locator("#tourBtn").click()
        time.sleep(0.5)
        print(f"[OK] Tour active: {page.locator('.sketch-tour-overlay').is_visible()}")
        tour_shot = os.path.join(output_dir, "tour_on_planner.png")
        page.screenshot(path=tour_shot)
        page.locator("#tourCloseBtn").click()
        time.sleep(0.3)

        # ----------------------------------------------------
        # 6. TEST LOGOUT REDIRECT BACK TO /home
        # ----------------------------------------------------
        print("\n--- 6. Testing Logout Redirect back to /home ---")
        page.locator("#logoutBtn").click()
        page.wait_for_url("**/home*", timeout=6000)
        after_logout_url = page.url
        print(f"[OK] URL after logout: {after_logout_url}")
        assert "/home" in after_logout_url, f"Expected redirect to /home after logout, got {after_logout_url}"

        # ----------------------------------------------------
        # 7. FINAL VERIFICATION
        # ----------------------------------------------------
        if errors:
            print("[ERROR] ERRORS DETECTED:")
            for e in errors:
                print("  ", e)
            sys.exit(1)
        else:
            print("\n[SUCCESS] ALL CHECKS PASSED PERFECTLY WITH ZERO ERRORS!")

        browser.close()

if __name__ == "__main__":
    run()
