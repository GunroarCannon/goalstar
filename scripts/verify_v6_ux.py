import time
import os
from playwright.sync_api import sync_playwright

BRAIN_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print("[1] Seeding guest session and navigating to http://localhost:8000 ...")
        # Navigate to home first to set localStorage
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.evaluate("""() => {
            localStorage.setItem('goalstar_user', JSON.stringify({ name: 'Guest Builder #493', isGuest: true, id: 'g_493' }));
            localStorage.removeItem('goalstar_tour_clicked');
            localStorage.removeItem('goalstar_walkthrough_completed');
        }""")

        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Close any welcome guide dialog if open
        guide_close = page.locator("#closeUiGuideBtn, #closeGuideDlgBtn")
        if guide_close.count() > 0 and guide_close.first.is_visible():
            guide_close.first.click()
            page.wait_for_timeout(300)

        tour_btn = page.locator("#tourBtn")
        initial_classes = tour_btn.get_attribute("class") or ""
        print(f"[2] Initial #tourBtn classes: '{initial_classes}'")
        assert "tour-bounce-btn" in initial_classes, f"Tour button should bounce initially, got: {initial_classes}"

        # Click tour button
        print("[3] Clicking #tourBtn ...")
        tour_btn.click()
        page.wait_for_timeout(400)

        after_click_classes = tour_btn.get_attribute("class") or ""
        print(f"[4] After click #tourBtn classes: '{after_click_classes}'")
        assert "tour-bounce-btn" not in after_click_classes, "Tour button MUST STOP bouncing immediately after click"

        is_clicked_saved = page.evaluate("() => localStorage.getItem('goalstar_tour_clicked')")
        print(f"[5] localStorage.goalstar_tour_clicked: '{is_clicked_saved}'")
        assert is_clicked_saved == "true", "Clicked state must be saved to localStorage"

        # Check all 6 steps
        for step_idx in range(1, 7):
            page.wait_for_timeout(350)
            
            # Check font size & family
            title_text = page.locator(".sketch-title").inner_text()
            font_size = page.evaluate("() => window.getComputedStyle(document.querySelector('.sketch-text')).fontSize")
            font_family = page.evaluate("() => window.getComputedStyle(document.querySelector('.sketch-text')).fontFamily")
            card_width = page.evaluate("() => window.getComputedStyle(document.querySelector('.sketch-card')).width")
            
            # Check spotlight mask y position
            spot_y = page.evaluate("""() => {
                const rect = document.querySelector('#sketch-mask rect:nth-child(2)');
                return rect ? parseFloat(rect.getAttribute('y') || '0') : 0;
            }""")

            print(f"  Step {step_idx}: '{title_text}' | font-size={font_size} | font-family={font_family} | card-width={card_width} | spot_y={spot_y}")
            
            # Verifications
            assert float(font_size.replace("px", "")) >= 15.0, f"Font size must be >= 15px, got {font_size}"
            assert "Space Grotesk" in font_family or "sans-serif" in font_family, f"Font family must be readable sans-serif, got {font_family}"
            assert spot_y >= 75.0, f"Spotlight y ({spot_y}) must be >= 75px so it NEVER clips into the header"

            # Capture screenshot
            step_shot_path = os.path.join(BRAIN_DIR, f"artifact_v6_tour_step_{step_idx}.png")
            page.screenshot(path=step_shot_path)
            print(f"  Saved screenshot: {step_shot_path}")

            if step_idx < 6:
                page.locator("#tourNextBtn").click()

        # Finish tour
        page.locator("#tourNextBtn").click()
        page.wait_for_timeout(300)

        # Reload page and verify #tourBtn STILL does not bounce
        print("[6] Reloading page to verify tour button does NOT bounce after reload ...")
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(500)
        reloaded_classes = page.locator("#tourBtn").get_attribute("class") or ""
        print(f"[7] Reloaded #tourBtn classes: '{reloaded_classes}'")
        assert "tour-bounce-btn" not in reloaded_classes, "Tour button must remain non-bouncing across reloads"

        stopped_bounce_path = os.path.join(BRAIN_DIR, "artifact_v6_tour_stopped_bounce.png")
        page.screenshot(path=stopped_bounce_path)
        print(f"  Saved screenshot: {stopped_bounce_path}")

        # Test on alternate goal: "#boardPick option 1"
        print("[8] Switching goal via #boardPick ...")
        options = page.locator("#boardPick option").all_inner_texts()
        print(f"  Available board options: {options}")
        # Choose the second option if available
        if len(options) > 1:
            page.locator("#boardPick").select_option(index=1)
            page.wait_for_timeout(600)

        # Open tour again on alternate goal
        print("[9] Opening tour on alternate goal ...")
        page.locator("#tourBtn").click()
        page.wait_for_timeout(400)

        job_step_1 = os.path.join(BRAIN_DIR, "artifact_v6_job_goal_step_1.png")
        page.screenshot(path=job_step_1)
        print(f"  Saved screenshot: {job_step_1}")

        # Go to Step 3 (Action Cost) on alternate goal
        page.locator("#tourNextBtn").click() # to step 2
        page.wait_for_timeout(300)
        page.locator("#tourNextBtn").click() # to step 3
        page.wait_for_timeout(400)

        spot_y_step3 = page.evaluate("""() => {
            const rect = document.querySelector('#sketch-mask rect:nth-child(2)');
            return rect ? parseFloat(rect.getAttribute('y') || '0') : 0;
        }""")
        print(f"  Job goal Step 3 spot_y: {spot_y_step3}")
        assert spot_y_step3 >= 75.0, f"Job goal Step 3 spot_y must be >= 75px, got {spot_y_step3}"

        job_step_3 = os.path.join(BRAIN_DIR, "artifact_v6_job_goal_step_3.png")
        page.screenshot(path=job_step_3)
        print(f"  Saved screenshot: {job_step_3}")

        # Go to Step 6 (Sui Inspector) on alternate goal
        page.locator("#tourNextBtn").click() # to step 4
        page.wait_for_timeout(300)
        page.locator("#tourNextBtn").click() # to step 5
        page.wait_for_timeout(300)
        page.locator("#tourNextBtn").click() # to step 6
        page.wait_for_timeout(500)

        # Check arrow target on step 6
        arrow_to = page.evaluate("""() => {
            const path = document.querySelector('.sketch-tour-svg path');
            return path ? path.getAttribute('d') : null;
        }""")
        print(f"  Job goal Step 6 arrow path: {arrow_to}")
        assert "0 0" not in str(arrow_to), f"Arrow must NOT point to (0, 0)! Path was: {arrow_to}"

        job_step_6 = os.path.join(BRAIN_DIR, "artifact_v6_job_goal_step_6.png")
        page.screenshot(path=job_step_6)
        print(f"  Saved screenshot: {job_step_6}")

        # Check Home page walkthrough button
        print("[10] Testing http://localhost:8000/home ...")
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.wait_for_timeout(600)
        home_nav_btn = page.locator("#navTourBtn")
        home_classes = home_nav_btn.get_attribute("class") or ""
        print(f"  Home #navTourBtn classes: '{home_classes}'")
        # Since localStorage already has goalstar_tour_clicked=true, it should not bounce
        assert "tour-bounce-btn" not in home_classes, "Home nav tour button should not bounce when already clicked"

        home_shot_path = os.path.join(BRAIN_DIR, "artifact_v6_home_nav.png")
        page.screenshot(path=home_shot_path)
        print(f"  Saved screenshot: {home_shot_path}")

        browser.close()
        print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
