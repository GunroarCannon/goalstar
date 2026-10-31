from playwright.sync_api import sync_playwright
import os

def test_tour_replay():
    out_dir = r"C:\Users\hmmm\goalstar-recall\tour_screenshots"
    os.makedirs(out_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        # Mark tour as completed so it does NOT auto-launch
        page.goto("http://localhost:8000")
        page.evaluate("localStorage.setItem('goalstar_walkthrough_completed', 'true')")
        page.reload()
        page.wait_for_timeout(1000)
        
        # Verify overlay is not present
        assert page.query_selector(".sketch-tour-overlay") is None, "Tour should not be open yet"
        
        # 1. Test clicking the header Replay Tour button
        print("Clicking header #tourBtn...")
        page.click("#tourBtn")
        page.wait_for_timeout(400)
        
        # Step 1
        page.screenshot(path=os.path.join(out_dir, "step_1_product.png"))
        print("Step 1 captured")
        
        # Steps 2-5
        step_names = ["step_2_product.png", "step_3_product.png", "step_4_product.png", "step_5_product.png"]
        for idx, sname in enumerate(step_names, start=2):
            page.click("#tourNextBtn")
            page.wait_for_timeout(400)
            page.screenshot(path=os.path.join(out_dir, sname))
            print(f"Step {idx} captured: {sname}")
            
        # Finish tour
        page.click("#tourNextBtn")
        page.wait_for_timeout(300)
        assert page.query_selector(".sketch-tour-overlay") is None, "Tour should be closed after last step"
        print("Tour finished and closed cleanly.")
        
        # 2. Test clicking #sideTourBtn in the sidebar to ensure replay works!
        print("Testing replay via #sideTourBtn in sidebar...")
        side_btn = page.query_selector("#sideTourBtn")
        assert side_btn is not None, "sideTourBtn must exist in DOM"
        side_btn.scroll_into_view_if_needed()
        side_btn.click()
        page.wait_for_timeout(400)
        overlay = page.query_selector(".sketch-tour-overlay")
        assert overlay is not None, "Tour overlay should re-open after #sideTourBtn click"
        print("Tour successfully re-opened via sidebar button!")
        page.screenshot(path=os.path.join(out_dir, "replayed_from_sidebar.png"))
            
        browser.close()

if __name__ == "__main__":
    test_tour_replay()
