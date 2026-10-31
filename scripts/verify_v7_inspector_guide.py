import time
import os
from playwright.sync_api import sync_playwright

BRAIN_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print("[1] Opening app with guest session ...")
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.evaluate("""() => {
            localStorage.setItem('goalstar_user', JSON.stringify({ name: 'Guest Builder #493', isGuest: true, id: 'g_493' }));
        }""")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 1. Test clicking a milestone node on the canvas
        print("[2] Clicking a milestone node on canvas ...")
        first_node = page.locator(".node:not(.k-start)").first
        first_node.click()
        page.wait_for_timeout(500)

        # Verify inspector is open
        inspector = page.locator("#inspector")
        assert inspector.is_visible(), "Inspector MUST be visible after clicking a node"
        print("  Inspector opened successfully!")

        # Verify ? Guide button inside inspector header
        ins_guide_btn = page.locator(".ins-guide-btn")
        assert ins_guide_btn.is_visible(), "? Guide button MUST exist in inspector header"
        print("  Found ? Guide button in inspector header!")

        # Click the ? Guide button in inspector header
        print("[3] Clicking ? Guide inside inspector header ...")
        ins_guide_btn.click()
        page.wait_for_timeout(500)

        # Verify the guide card is brought up!
        sketch_card = page.locator(".sketch-card")
        assert sketch_card.is_visible(), "Guide card MUST be brought up when clicking ? Guide!"
        guide_title = page.locator(".sketch-title").inner_text()
        print(f"  Guide card is visible with title: '{guide_title}'")
        assert "Inspector" in guide_title, f"Expected guide to be on Inspector step, got '{guide_title}'"

        # Capture screenshot: inspector with guide
        shot1 = os.path.join(BRAIN_DIR, "artifact_v7_inspector_with_guide.png")
        page.screenshot(path=shot1)
        print(f"  Saved screenshot: {shot1}")

        # Close tour guide
        page.locator("#tourCloseBtn").click()
        page.wait_for_timeout(300)

        # 2. Test topbar ? Guide button
        print("[4] Testing topbar #uiGuideBtn ...")
        page.locator("#uiGuideBtn").click()
        page.wait_for_timeout(500)

        # Should bring up the guide directly!
        assert page.locator(".sketch-card").is_visible(), "Topbar ? Guide MUST bring up the guide!"
        guide_title2 = page.locator(".sketch-title").inner_text()
        print(f"  Topbar ? Guide brought up: '{guide_title2}'")
        assert page.locator("#inspector").is_visible(), "Inspector MUST be open when guide is on inspector step!"

        shot2 = os.path.join(BRAIN_DIR, "artifact_v7_topbar_guide_brought_up.png")
        page.screenshot(path=shot2)
        print(f"  Saved screenshot: {shot2}")

        # Close guide
        page.locator("#tourCloseBtn").click()
        page.wait_for_timeout(300)

        # 3. Test on career goal ("Get a good paying job") if exists, or create it
        print("[5] Testing on career / job board ...")
        # Check if option exists in #boardPick
        options = page.locator("#boardPick option").all_inner_texts()
        print(f"  Options in #boardPick: {options}")

        # If career board not present, let's create a new goal "Get a good paying job"
        has_job = any("job" in opt.lower() or "paying" in opt.lower() for opt in options)
        if not has_job:
            print("  Creating new goal 'Get a good paying job' ...")
            page.locator("#newGoalBtn").click()
            page.wait_for_timeout(300)
            page.locator("#newGoalInput").fill("Get a good paying job")
            page.locator("#newGoalDlg button[type='submit']").click()
            page.wait_for_timeout(1000)

        # Now select a state node on this board
        page.wait_for_timeout(500)
        state_node = page.locator(".node:not(.k-start)").first
        state_node.click()
        page.wait_for_timeout(500)

        # Verify inspector is open
        assert page.locator("#inspector").is_visible(), "Inspector MUST be open on job goal!"
        state_label = page.locator("#inspector textarea[data-f='label']").input_value()
        print(f"  Job goal state label in inspector: '{state_label}'")

        # Click ? Guide in topbar
        print("[6] Clicking topbar ? Guide on job goal ...")
        page.locator("#uiGuideBtn").click()
        page.wait_for_timeout(500)

        # Verify both inspector AND guide are visible!
        assert page.locator("#inspector").is_visible(), "Inspector MUST remain open!"
        assert page.locator(".sketch-card").is_visible(), "Guide card MUST be visible!"

        shot3 = os.path.join(BRAIN_DIR, "artifact_v7_job_inspector_with_guide.png")
        page.screenshot(path=shot3)
        print(f"  Saved screenshot: {shot3}")

        browser.close()
        print("\nALL V7 INSPECTOR & GUIDE VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
