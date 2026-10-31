import time
import os
from playwright.sync_api import sync_playwright

BRAIN_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def test_viewport(page, width, height, name):
    print(f"\n--- Testing Viewport {width}x{height} ({name}) ---")
    page.set_viewport_size({"width": width, "height": height})
    page.wait_for_timeout(400)

    # Launch tour
    page.evaluate("() => { if (window.tour) window.tour.start(true); }")
    page.wait_for_timeout(300)

    for step_idx in range(1, 7):
        page.wait_for_timeout(300)

        # 1. Check card bounds - MUST NEVER BE CLIPPED OUT
        card_rect = page.evaluate("""() => {
            const card = document.querySelector('.sketch-card-container');
            if (!card) return null;
            const r = card.getBoundingClientRect();
            return { top: r.top, bottom: r.bottom, left: r.left, right: r.right, height: r.height, width: r.width };
        }""")

        assert card_rect is not None, f"Card must exist in step {step_idx}"
        print(f"  Step {step_idx}: card top={card_rect['top']:.1f}, bottom={card_rect['bottom']:.1f} (window H={height}), left={card_rect['left']:.1f}, right={card_rect['right']:.1f} (window W={width})")

        # Zero clipping assertions!
        assert card_rect['bottom'] <= height - 8, f"Card bottom ({card_rect['bottom']:.1f}) MUST NOT exceed viewport height ({height})! CLIPPED OUT!"
        assert card_rect['top'] >= 70, f"Card top ({card_rect['top']:.1f}) MUST NOT clip into header!"
        assert card_rect['right'] <= width - 8, f"Card right ({card_rect['right']:.1f}) MUST NOT exceed viewport width ({width})!"
        assert card_rect['left'] >= 8, f"Card left ({card_rect['left']:.1f}) MUST NOT clip off left screen!"

        # 2. Check spotlight bounds - MUST ACTUALLY CIRCLE SOMETHING AND NEVER CLIP
        spot_info = page.evaluate("""() => {
            const r = document.querySelector('#sketch-mask rect:nth-child(2)');
            if (!r) return null;
            return {
                x: parseFloat(r.getAttribute('x') || '0'),
                y: parseFloat(r.getAttribute('y') || '0'),
                w: parseFloat(r.getAttribute('width') || '0'),
                h: parseFloat(r.getAttribute('height') || '0')
            };
        }""")

        assert spot_info is not None, f"Spotlight must exist in step {step_idx}"
        print(f"    Spotlight: x={spot_info['x']:.1f}, y={spot_info['y']:.1f}, w={spot_info['w']:.1f}, h={spot_info['h']:.1f}")

        assert spot_info['y'] >= 72, f"Spotlight y ({spot_info['y']:.1f}) MUST NOT clip into header (< 72px)!"
        assert spot_info['w'] >= 25, f"Spotlight width ({spot_info['w']:.1f}) must be >= 25px!"
        assert spot_info['h'] >= 20, f"Spotlight height ({spot_info['h']:.1f}) must be >= 20px!"

        # Step-specific content checks
        if step_idx == 3:
            # Step 3 must circle action cost pill
            shot_path = os.path.join(BRAIN_DIR, f"artifact_v8_step3_{name}.png")
            page.screenshot(path=shot_path)
            print(f"    Saved Step 3 screenshot: {shot_path}")
        elif step_idx == 6:
            # Step 6 must circle Sui inspector
            shot_path = os.path.join(BRAIN_DIR, f"artifact_v8_step6_{name}.png")
            page.screenshot(path=shot_path)
            print(f"    Saved Step 6 screenshot: {shot_path}")

        if step_idx < 6:
            page.locator("#tourNextBtn").click()

    # Close tour
    page.locator("#tourNextBtn").click()
    page.wait_for_timeout(300)

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("[1] Seeding guest session ...")
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.evaluate("""() => {
            localStorage.setItem('goalstar_user', JSON.stringify({ name: 'Guest Builder #493', isGuest: true, id: 'g_493' }));
        }""")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Test standard desktop: 1280x800
        test_viewport(page, 1280, 800, "desktop_1280x800")

        # Test compact laptop / smaller height (the exact user scenario where Finish Tour was clipped): 1024x640
        test_viewport(page, 1024, 640, "laptop_1024x640")

        # Test tablet / narrow desktop: 800x700
        test_viewport(page, 800, 700, "tablet_800x700")

        browser.close()
        print("\nALL SCENARIOS AND CLIPPING CHECKS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_tests()
