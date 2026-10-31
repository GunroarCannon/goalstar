import os
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def main():
    print("=== STARTING V11 TOUR & BUTTONS VERIFICATION ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}") if msg.type in ['error', 'warn'] else None)

        # 1. Login as guest
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.evaluate("""() => {
            localStorage.setItem('goalstar_user', JSON.stringify({ name: 'Guest Builder #493', isGuest: true, id: 'g_493' }));
        }""")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_selector(".node", timeout=10000)
        page.wait_for_timeout(1000)

        # 2. Switch to Blueprint theme (as in user screenshot)
        page.select_option("#themeSelect", "blueprint")
        page.wait_for_timeout(500)

        # 3. Launch tour directly to Step 2 (Dream with AI)
        page.evaluate("""() => {
            if (window.tour) {
                window.tour.start(true);
                window.tour.goToStep(1); // Step 2 (index 1)
            }
        }""")
        page.wait_for_timeout(700)

        # Inspect Step 2 spotlight and #dreamBtn bounds
        dream_btn = page.query_selector("#dreamBtn")
        assert dream_btn is not None, "Dream button not found!"
        d_box = dream_btn.bounding_box()
        print(f"Dream Button Rect: left={d_box['x']:.1f}, top={d_box['y']:.1f}, w={d_box['width']:.1f}, h={d_box['height']:.1f}")

        # Spotlight element in SVG
        spot_rect = page.query_selector(".tour-spotlight-ring")
        assert spot_rect is not None, "Spotlight ring not found!"
        s_box = spot_rect.bounding_box()
        print(f"Spotlight Ring Rect: left={s_box['x']:.1f}, top={s_box['y']:.1f}, w={s_box['width']:.1f}, h={s_box['height']:.1f}")

        # Check spotlight frames #dreamBtn
        assert abs(s_box['x'] - (d_box['x'] - 5)) < 15, "Spotlight X should align with #dreamBtn"
        assert s_box['y'] < 25, f"Spotlight Y must be in topbar (< 25px), got: {s_box['y']}"

        # Inspect Back button styling (secondary)
        back_btn = page.query_selector(".sketch-btn.secondary")
        assert back_btn is not None, "Back button not found!"
        back_styles = page.evaluate("""() => {
            const btn = document.querySelector('.sketch-btn.secondary');
            if (!btn) return null;
            const cs = getComputedStyle(btn);
            return { color: cs.color, background: cs.backgroundColor };
        }""")
        print(f"Back button styles in Blueprint theme: color='{back_styles['color']}', background='{back_styles['background']}'")
        # Ensure it is NOT white text on white background!
        assert back_styles['background'] != "rgb(255, 255, 255)", f"Back button must not have white background in dark themes! Got: {back_styles['background']}"

        # Screenshot Step 2 Blueprint
        out_step2 = os.path.join(ARTIFACT_DIR, "artifact_v11_step2_dream_blueprint.png")
        page.screenshot(path=out_step2)
        print(f"Saved: {out_step2}")

        # 4. Advance to Step 3 (Best Path)
        page.evaluate("""() => {
            if (window.tour) window.tour.goToStep(2); // Step 3 (index 2)
        }""")
        page.wait_for_timeout(700)

        # Inspect Step 3 spotlight bounds
        bp_section = page.query_selector("#bestPathSection")
        assert bp_section is not None, "#bestPathSection not found!"
        bp_box = bp_section.bounding_box()
        print(f"Best Path Section Rect: left={bp_box['x']:.1f}, top={bp_box['y']:.1f}, w={bp_box['width']:.1f}, h={bp_box['height']:.1f}")

        s_box3 = page.query_selector(".tour-spotlight-ring").bounding_box()
        print(f"Step 3 Spotlight Ring Rect: left={s_box3['x']:.1f}, top={s_box3['y']:.1f}, w={s_box3['width']:.1f}, h={s_box3['height']:.1f}")

        # Ensure spotlight does NOT enclose entire sidebar (> 650px)
        assert s_box3['height'] < 550, f"Spotlight should only frame Best Path, not whole sidebar! Height was {s_box3['height']}"

        # Screenshot Step 3 Blueprint
        out_step3 = os.path.join(ARTIFACT_DIR, "artifact_v11_step3_bestpath_blueprint.png")
        page.screenshot(path=out_step3)
        print(f"Saved: {out_step3}")

        # 5. Test Notebook theme Step 2
        page.select_option("#themeSelect", "notebook")
        page.wait_for_timeout(500)
        page.evaluate("""() => {
            if (window.tour) window.tour.goToStep(1);
        }""")
        page.wait_for_timeout(700)
        out_step2_note = os.path.join(ARTIFACT_DIR, "artifact_v11_step2_dream_notebook.png")
        page.screenshot(path=out_step2_note)
        print(f"Saved: {out_step2_note}")

        browser.close()
        print("=== ALL V11 VERIFICATION CHECKS PASSED ===")

if __name__ == "__main__":
    main()
