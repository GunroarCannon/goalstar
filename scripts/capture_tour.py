from playwright.sync_api import sync_playwright
import time
import os

def capture_tour():
    out_dir = r"C:\Users\hmmm\goalstar-recall\tour_screenshots"
    os.makedirs(out_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        # Load page and ensure walkthrough is triggered
        page.goto("http://localhost:8000")
        page.wait_for_timeout(1000)
        
        # Trigger tour
        page.evaluate("() => { if (window.tour) window.tour.start(true); }")
        page.wait_for_timeout(500)
        
        # Capture step 1
        page.screenshot(path=os.path.join(out_dir, "step_1_banner.png"))
        print("Captured step 1")
        
        # Click Next for steps 2 to 5
        steps = ["step_2_astar.png", "step_3_escalation.png", "step_4_sui.png", "step_5_cli.png"]
        for idx, filename in enumerate(steps, start=2):
            btn = page.query_selector("#tourNextBtn")
            if btn:
                btn.click()
                page.wait_for_timeout(500)
                page.screenshot(path=os.path.join(out_dir, filename))
                print(f"Captured step {idx}: {filename}")
        
        browser.close()

if __name__ == "__main__":
    capture_tour()
