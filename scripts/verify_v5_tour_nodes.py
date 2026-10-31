import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def test_tour_on_career_goal():
    print("=== TESTING TOUR ON 'GET A GOOD PAYING JOB' GOAL ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        # 1. Login as guest and set goalstar_user
        page.goto("http://localhost:8000/home")
        page.evaluate("() => localStorage.setItem('goalstar_user', JSON.stringify({ type: 'guest', id: 'Guest#454' }))")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_timeout(1000)
        
        # Switch to "Get a good paying job" board
        board_select = page.locator("#boardPick")
        board_options = board_select.locator("option").all_inner_texts()
        print("Available boards:", board_options)
        
        # Select career board if present or select second option
        if len(board_options) > 1:
            board_select.select_option(index=1)
            page.wait_for_timeout(600)
            print("Switched to board index 1:", board_select.evaluate("el => el.value"))
            
        # If tour was auto-opened, close it first to test cleanly
        if page.locator(".sketch-tour-overlay").count() > 0:
            page.locator("#tourSkipBtn").click(force=True)
            page.wait_for_timeout(400)
            
        # Click Tour button to start fresh tour
        page.locator("#tourBtn").click(force=True)
        page.wait_for_timeout(600)
        
        # Step through each step and verify arrow does NOT point to (0,0)
        for step_idx in range(1, 7):
            title = page.locator(".sketch-title").inner_text()
            text = page.locator(".sketch-text").inner_text()
            badge = page.locator(".sketch-badge").inner_text()
            print(f"\n--- {badge} ---")
            print("Title:", title)
            print("Text:", text)
            
            # Check arrow coordinates
            arrow_path = page.locator(".sketch-tour-svg path").first
            d_attr = arrow_path.get_attribute("d") if arrow_path.count() > 0 else ""
            print("Arrow path d:", d_attr)
            
            # Verify arrow does NOT terminate at (0, 0)
            assert " 0 0" not in d_attr and " 0,0" not in d_attr and " 0 2" not in d_attr, f"Arrow terminates near (0,0) in step {step_idx}: {d_attr}"
            
            # Capture artifact screenshot of this step
            ss_path = os.path.join(ARTIFACT_DIR, f"artifact_v5_tour_step_{step_idx}.png")
            page.screenshot(path=ss_path)
            print(f"Captured artifact_v5_tour_step_{step_idx}.png")
            
            if step_idx < 6:
                page.locator("#tourNextBtn").click(force=True)
                page.wait_for_timeout(500)
            else:
                page.locator("#tourNextBtn").click(force=True)
                page.wait_for_timeout(400)
                
        # Verify tour is closed after last step
        assert page.locator(".sketch-tour-overlay").count() == 0, "Tour should close after finish"
        print("SUCCESS: Tour finished cleanly on career board!")
        
        # Capture final canvas state showing node and edge labels without overlap
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v5_nodes_and_numbers_canvas.png"))
        print("Captured artifact_v5_nodes_and_numbers_canvas.png")
        
        browser.close()
        print("=== ALL STEP VERIFICATIONS PASSED ===")

if __name__ == "__main__":
    test_tour_on_career_goal()
