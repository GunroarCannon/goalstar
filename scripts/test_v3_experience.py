import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def run_tests():
    print("=== STARTING V3 VERIFICATION TEST SUITE ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Test /home Desktop
        print("\n--- 1. Testing /home Landing Page (Desktop) ---")
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        
        # Listen for console errors
        errors = []
        page.on("pageerror", lambda err: errors.append(f"PAGE ERROR: {err}"))
        page.on("console", lambda msg: errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type == "error" else None)
        
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.wait_for_timeout(1000)
        
        # Verify ink underline initial state
        ink_svg = page.locator("#inkSwashSvg")
        print("ink_svg count:", ink_svg.count())
        assert ink_svg.count() == 1, "inkSwashSvg must exist"
        
        # Check theme selector in nav
        theme_select = page.locator("#themeSelect")
        print("themeSelect count:", theme_select.count())
        assert theme_select.count() >= 1, "themeSelect must exist on /home"
        
        # Switch to night theme
        theme_select.first.select_option("night")
        page.wait_for_timeout(400)
        paper_attr = page.evaluate("() => document.body.getAttribute('data-paper')")
        print("data-paper after selecting 'night':", paper_attr)
        assert paper_attr == "night", "Body data-paper should be 'night'"
        
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v3_home_night.png"))
        print("Captured artifact_v3_home_night.png")
        
        # Switch to monograph theme
        theme_select.first.select_option("monograph")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v3_home_monograph.png"))
        print("Captured artifact_v3_home_monograph.png")

        # Switch back to notebook theme
        theme_select.first.select_option("notebook")
        page.wait_for_timeout(400)
        
        # Check Card 5 & Journey Terminal elements
        card5 = page.locator("#card5")
        terminal = page.locator("#journeyTerminal")
        terminal_target = page.locator("#terminalCircleTarget")
        arrow = page.locator("#travelingArrow")
        
        print("card5 count:", card5.count())
        print("journeyTerminal count:", terminal.count())
        print("terminalCircleTarget count:", terminal_target.count())
        print("travelingArrow count:", arrow.count())
        
        # Scroll down through the use cases section
        print("Scrolling to #card5...")
        card5.scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        
        # Scroll down to the journey terminal at the bottom
        print("Scrolling to #journeyTerminal...")
        terminal.scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        
        # Scroll to bottom of window to fully dock arrow
        page.evaluate("() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
        page.wait_for_timeout(1000)
        
        # Check arrow classes and geometry
        arrow_class = arrow.get_attribute("class") or ""
        print("Arrow class at terminal:", arrow_class)
        has_is_circle = "is-circle" in arrow_class
        print("Has 'is-circle' class:", has_is_circle)
        assert has_is_circle, "Arrow MUST turn into a circle at terminal!"
        
        # Check terminal target arrival class
        term_class = terminal_target.get_attribute("class") or ""
        print("Terminal circle target class:", term_class)
        has_arrived = "arrived" in term_class
        print("Has 'arrived' class:", has_arrived)
        assert has_arrived, "Terminal circle target MUST have 'arrived' class!"
        
        # Check arrow position relative to terminal target
        arrow_box = arrow.bounding_box()
        term_box = terminal_target.bounding_box()
        track_box = page.locator("#journeyTrack").bounding_box()
        
        # Verify arrow is centered horizontally (middle X position)
        if arrow_box and track_box:
            track_center_x = track_box["x"] + track_box["width"] / 2
            arrow_center_x = arrow_box["x"] + arrow_box["width"] / 2
            diff_x = abs(track_center_x - arrow_center_x)
            print(f"Track Center X: {track_center_x:.1f}, Arrow Center X: {arrow_center_x:.1f}, Diff: {diff_x:.1f}px")
            assert diff_x < 30, f"Arrow should be centered horizontally within track, diff was {diff_x}px"
            
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v3_arrow_terminal_circle.png"))
        print("Captured artifact_v3_arrow_terminal_circle.png")
        
        # 2. Test Mobile Viewport (375px)
        print("\n--- 2. Testing /home Landing Page (Mobile 375px) ---")
        page_mobile = browser.new_page(viewport={"width": 375, "height": 667})
        page_mobile.goto("http://localhost:8000/home", wait_until="networkidle")
        page_mobile.wait_for_timeout(800)
        
        # Check horizontal scroll / overflow
        overflow = page_mobile.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
        print("Mobile has horizontal overflow:", overflow)
        assert not overflow, "Mobile page must not have horizontal overflow!"
        
        page_mobile.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v3_home_mobile.png"))
        print("Captured artifact_v3_home_mobile.png")
        page_mobile.close()
        
        # 3. Test / Planner Workspace & Guide & Dream
        print("\n--- 3. Testing / Planner Workspace & Guide & Dream ---")
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page_planner = context.new_page()
        planner_errors = []
        page_planner.on("pageerror", lambda err: planner_errors.append(f"PLANNER ERROR: {err}"))
        page_planner.on("console", lambda msg: planner_errors.append(f"PLANNER CONSOLE {msg.type}: {msg.text}") if msg.type == "error" else None)
        
        # Set localStorage user and tour completed BEFORE navigating so it opens workspace directly without tour blocking
        page_planner.goto("http://localhost:8000/home")
        page_planner.evaluate("() => { localStorage.setItem('goalstar_user', JSON.stringify({ type: 'guest', id: 'Guest#888' })); localStorage.setItem('goalstar_walkthrough_completed', 'true'); }")
        
        page_planner.goto("http://localhost:8000/", wait_until="networkidle")
        page_planner.wait_for_timeout(1200)
        
        # Test Theme Selector on Planner
        planner_theme_select = page_planner.locator("#themeSelect")
        print("Planner themeSelect count:", planner_theme_select.count())
        assert planner_theme_select.count() >= 1, "themeSelect must exist on /"
        
        planner_theme_select.first.select_option("blueprint")
        page_planner.wait_for_timeout(400)
        p_paper = page_planner.evaluate("() => document.body.getAttribute('data-paper')")
        print("Planner data-paper after selecting 'blueprint':", p_paper)
        assert p_paper == "blueprint", "Planner body data-paper should be 'blueprint'"
        
        page_planner.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v3_planner_blueprint.png"))
        print("Captured artifact_v3_planner_blueprint.png")
        
        # Test Guide Button
        guide_btn = page_planner.locator("#uiGuideBtn")
        print("uiGuideBtn count:", guide_btn.count())
        assert guide_btn.count() == 1, "uiGuideBtn must exist on planner!"
        
        guide_btn.click()
        page_planner.wait_for_timeout(500)
        
        guide_dlg = page_planner.locator("#uiGuideDlg")
        is_open = guide_dlg.evaluate("el => el.open")
        print("uiGuideDlg is open:", is_open)
        assert is_open, "uiGuideDlg must open when ? Guide is clicked"
        
        page_planner.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v3_guide_modal.png"))
        print("Captured artifact_v3_guide_modal.png")
        
        # Close guide modal
        page_planner.locator("#closeGuideDlgBtn").click()
        page_planner.wait_for_timeout(400)
        is_open_after = guide_dlg.evaluate("el => el.open")
        print("uiGuideDlg is open after close:", is_open_after)
        assert not is_open_after, "uiGuideDlg should close"
        
        # Test Dream Action & Verify Zero Runtime TypeError
        print("\n--- 4. Testing Dream Action via newGoalDlg & Error Verification ---")
        new_goal_btn = page_planner.locator("#newGoalBtn")
        print("newGoalBtn count:", new_goal_btn.count())
        new_goal_btn.click()
        page_planner.wait_for_timeout(500)
        
        # Check newGoalDlg is open
        new_goal_dlg = page_planner.locator("#newGoalDlg")
        print("newGoalDlg open:", new_goal_dlg.evaluate("el => el.open"))
        
        # Select first example chip
        first_chip = page_planner.locator("#examples button.chipbtn").first
        first_chip.click()
        page_planner.wait_for_timeout(300)
        
        # Ensure Dream initial roadmap is checked
        dream_checkbox = page_planner.locator("input[name='dream']")
        dream_checkbox.check()
        
        # Submit the new goal form
        submit_btn = page_planner.locator("#newGoalDlg button[value='ok']")
        submit_btn.click()
        
        # Wait for dream execution to complete
        page_planner.wait_for_timeout(3000)
        
        # Check if any errors occurred during dream execution
        print(f"Total planner console/page errors recorded: {len(planner_errors)}")
        for err in planner_errors:
            print("  ->", err)
            
        type_errors = [e for e in planner_errors if "Cannot read properties of undefined (reading 'nodes')" in e]
        assert len(type_errors) == 0, f"TypeError in dream occurred: {type_errors}"
        print("SUCCESS: Dream executed with ZERO 'nodes' TypeErrors!")
        
        page_planner.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v3_planner_after_dream.png"))
        print("Captured artifact_v3_planner_after_dream.png")
        
        browser.close()
        print("\n=== ALL TESTS COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    run_tests()
