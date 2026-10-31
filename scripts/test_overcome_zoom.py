import sys, os, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        
        print("=== Test 1: Loading /home ===")
        page.goto('http://localhost:8000/home', wait_until='networkidle')
        time.sleep(1)
        
        print("=== Test 2: Scroll to Approach 'Engineered to Overcome' Box ===")
        # Scroll so the box just enters from the bottom of the viewport
        page.evaluate("""() => {
            const box = document.getElementById('overcomeHeaderBox');
            const rect = box.getBoundingClientRect();
            // Position it near bottom of viewport
            window.scrollTo(0, window.scrollY + rect.top - window.innerHeight + 120);
        }""")
        time.sleep(0.6)
        
        entering_state = page.evaluate("""() => {
            const box = document.getElementById('overcomeHeaderBox');
            const transform = box.style.transform;
            const opacity = parseFloat(box.style.opacity);
            return { transform, opacity };
        }""")
        print(f"Entering state: transform={entering_state['transform']}, opacity={entering_state['opacity']}")
        assert entering_state['opacity'] < 1.0, f"Expected opacity < 1.0, got {entering_state['opacity']}"
        assert 'scale(1.' in entering_state['transform'], f"Expected scale > 1.0, got {entering_state['transform']}"
        
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_overcome_entering.png'))
        print("Saved artifact_overcome_entering.png")
        
        print("=== Test 3: Scroll so 'Engineered to Overcome' Box is Settled in Original Position ===")
        page.evaluate("""() => {
            const box = document.getElementById('overcomeHeaderBox');
            box.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }""")
        time.sleep(1)
        
        settled_state = page.evaluate("""() => {
            const box = document.getElementById('overcomeHeaderBox');
            const transform = box.style.transform;
            const opacity = parseFloat(box.style.opacity);
            return { transform, opacity };
        }""")
        print(f"Settled state: transform={settled_state['transform']}, opacity={settled_state['opacity']}")
        assert settled_state['opacity'] >= 0.98, f"Expected opacity >= 0.98, got {settled_state['opacity']}"
        assert 'scale(1)' in settled_state['transform'] or 'scale(1.0' in settled_state['transform'], f"Expected scale ≈ 1.0, got {settled_state['transform']}"
        assert 'translate3d(0' in settled_state['transform'], f"Expected og pos, got {settled_state['transform']}"
        
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_overcome_settled.png'))
        print("Saved artifact_overcome_settled.png")
        
        print("=== Test 4: Verify Dark Mode Plaque Appearance ===")
        page.click('#themeSwitch')
        time.sleep(0.5)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_overcome_dark.png'))
        print("Saved artifact_overcome_dark.png")
        page.click('#themeSwitch')
        time.sleep(0.5)
        
        print("=== Test 5: Verify Mobile 375px Zoom & Alignment ===")
        mobile_page = browser.new_page(viewport={'width': 375, 'height': 667})
        mobile_page.goto('http://localhost:8000/home', wait_until='networkidle')
        time.sleep(1)
        
        mobile_page.evaluate("""() => {
            const box = document.getElementById('overcomeHeaderBox');
            box.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }""")
        time.sleep(1)
        
        scroll_w = mobile_page.evaluate("document.documentElement.scrollWidth")
        client_w = mobile_page.evaluate("document.documentElement.clientWidth")
        print(f"Mobile widths: scrollWidth={scroll_w}, clientWidth={client_w}")
        assert scroll_w <= client_w, f"Horizontal overflow! {scroll_w} > {client_w}"
        
        mobile_page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_overcome_mobile_375.png'))
        print("Saved artifact_overcome_mobile_375.png")
        
        browser.close()
        print("\nALL ZOOM-IN & FADE-IN VERIFICATIONS PASSED WITH ZERO ERRORS!")

if __name__ == '__main__':
    run_tests()
