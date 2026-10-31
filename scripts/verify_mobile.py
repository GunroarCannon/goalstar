import os
from playwright.sync_api import sync_playwright

BRAIN_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 375, "height": 667})
        
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.evaluate("""() => {
            localStorage.setItem('goalstar_user', JSON.stringify({ name: 'Guest Builder #493', isGuest: true, id: 'g_493' }));
        }""")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_timeout(1000)
        
        page.evaluate("() => { if (window.tour) window.tour.start(true); }")
        page.wait_for_timeout(400)
        
        for i in range(1, 7):
            r = page.evaluate("""() => {
                const el = document.querySelector('.sketch-card-container');
                if (!el) return null;
                const b = el.getBoundingClientRect();
                return { top: b.top, bottom: b.bottom, left: b.left, right: b.right, w: b.width, h: b.height };
            }""")
            print(f"Mobile Step {i}: top={r['top']:.1f}, bottom={r['bottom']:.1f}, left={r['left']:.1f}, right={r['right']:.1f}, w={r['w']:.1f}, h={r['h']:.1f}")
            assert r['bottom'] <= 667, f"Clipped at bottom in mobile step {i}: {r['bottom']}"
            assert r['right'] <= 375, f"Clipped at right in mobile step {i}: {r['right']}"
            
            if i == 3:
                shot_path = os.path.join(BRAIN_DIR, "artifact_v8_step3_mobile_375x667.png")
                page.screenshot(path=shot_path)
                print(f"Saved mobile step 3 screenshot: {shot_path}")
            elif i == 6:
                shot_path = os.path.join(BRAIN_DIR, "artifact_v8_step6_mobile_375x667.png")
                page.screenshot(path=shot_path)
                print(f"Saved mobile step 6 screenshot: {shot_path}")
                
            if i < 6:
                page.locator("#tourNextBtn").click()
                page.wait_for_timeout(300)
                
        browser.close()
        print("Mobile test passed with ZERO clipping!")

if __name__ == "__main__":
    main()
