import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def capture_visuals():
    print("=== CAPTURING V4 VISUAL EVIDENCE ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Capture Workspace Tour Step 1 (Pointing to Goal, not login!)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        # Set logged in user so guest state is active
        page.goto("http://localhost:8000/home")
        page.evaluate("() => localStorage.setItem('goalstar_user', JSON.stringify({ type: 'guest', id: 'Guest#454' }))")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_timeout(1000)
        
        # Check if tour is open on load
        tour_overlay = page.locator(".sketch-tour-overlay")
        print("tour_overlay count:", tour_overlay.count())
        
        if tour_overlay.count() > 0:
            card_title = page.locator(".sketch-title").inner_text()
            card_text = page.locator(".sketch-text").inner_text()
            print("Tour Step 1 Title:", card_title)
            print("Tour Step 1 Text:", card_text)
            
            page.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v4_tour_step1_goal.png"))
            print("Captured artifact_v4_tour_step1_goal.png")
            
            # Close tour by clicking skip
            page.locator("#tourSkipBtn").click(force=True)
            page.wait_for_timeout(500)
        
        # Capture top bar showing bouncing tour button
        tour_btn = page.locator("#tourBtn")
        print("tour_btn count:", tour_btn.count())
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v4_tour_button_bounce.png"))
        print("Captured artifact_v4_tour_button_bounce.png")
        
        # Open UI Guide Dialog
        guide_btn = page.locator("#uiGuideBtn")
        guide_btn.click(force=True)
        page.wait_for_timeout(600)
        
        page.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v4_guide_modal_concise.png"))
        print("Captured artifact_v4_guide_modal_concise.png")
        page.locator("#closeGuideDlgBtn").click(force=True)
        page.wait_for_timeout(400)
        
        # 2. Capture /home Walkthrough ("How GoalStar Works")
        page_home = browser.new_page(viewport={"width": 1280, "height": 800})
        page_home.goto("http://localhost:8000/home", wait_until="networkidle")
        page_home.wait_for_timeout(800)
        
        # Click Walkthrough in nav
        page_home.locator("#navTourBtn").click(force=True)
        page_home.wait_for_timeout(600)
        
        home_title = page_home.locator("#homeTourTitle").inner_text()
        home_body = page_home.locator("#homeTourBody").inner_text()
        print("Home Tour Title:", home_title)
        print("Home Tour Body:", home_body)
        
        page_home.screenshot(path=os.path.join(ARTIFACT_DIR, "artifact_v4_home_tour_concise.png"))
        print("Captured artifact_v4_home_tour_concise.png")
        
        browser.close()
        print("=== ALL VISUAL EVIDENCE CAPTURED SUCCESSFULLY ===")

if __name__ == "__main__":
    capture_visuals()
