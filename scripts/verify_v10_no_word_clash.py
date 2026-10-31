import os
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def main():
    print("=== STARTING V10 WORD CLASH VERIFICATION ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}") if msg.type in ['error', 'warn'] else None)

        # Ensure guest auth
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.evaluate("""() => {
            localStorage.setItem('goalstar_user', JSON.stringify({ name: 'Guest Builder #493', isGuest: true, id: 'g_493' }));
        }""")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_selector(".node", timeout=10000)
        page.wait_for_timeout(1000)

        # Mark first state node done directly via toggleDone or pointerdown
        page.evaluate("""() => {
            const firstStateNode = document.querySelector('.node.k-state');
            if (firstStateNode) {
                const tick = firstStateNode.querySelector('.tick');
                if (tick) {
                    tick.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true, button: 0 }));
                }
            }
        }""")
        page.wait_for_timeout(600)

        target_node = page.query_selector(".node.k-state")
        is_done = target_node.evaluate("el => el.classList.contains('done')")
        print(f"Node marked done: {is_done}")
        
        # If not done yet, try clicking directly on the canvas handler
        if not is_done:
            page.evaluate("""() => {
                const firstStateNode = document.querySelector('.node.k-state');
                if (firstStateNode && window.canvas) {
                    window.canvas.h.onToggleDone(firstStateNode.dataset.id);
                }
            }""")
            page.wait_for_timeout(600)
            is_done = target_node.evaluate("el => el.classList.contains('done')")
            print(f"Node marked done after onToggleDone: {is_done}")

        assert is_done, "Node must have class 'done'"

        tick_btn = target_node.query_selector(".tick")
        # Verify tick button does NOT have text 'Done'
        btn_text = tick_btn.inner_text().strip()
        print(f"Tick button text: '{btn_text}'")
        assert btn_text == "", f"Tick button must not have text, got: '{btn_text}'"

        # Verify svg checkmark
        svg = tick_btn.query_selector("svg.tick-svg")
        assert svg is not None, "SVG checkmark icon must be present"
        print("SVG checkmark present: True")

        # Check bounding boxes for clearance
        tick_box = tick_btn.bounding_box()
        nl_el = target_node.query_selector(".nl")
        nl_box = nl_el.bounding_box()

        print(f"Tick Box: left={tick_box['x']:.1f}, right={tick_box['x'] + tick_box['width']:.1f}")
        print(f"Label Box: left={nl_box['x']:.1f}, right={nl_box['x'] + nl_box['width']:.1f}")

        clearance = nl_box['x'] - (tick_box['x'] + tick_box['width'])
        print(f"Clearance between tick button and label: {clearance:.1f}px")
        assert clearance >= 4.0, f"Clearance too small: {clearance}px"

        # Screenshot completed milestone in notebook theme
        out1 = os.path.join(ARTIFACT_DIR, "artifact_v10_done_milestone_no_clash.png")
        target_node.screenshot(path=out1)
        print(f"Saved: {out1}")

        # Switch to night theme and screenshot
        page.select_option("#themeSelect", "night")
        page.wait_for_timeout(500)
        out2 = os.path.join(ARTIFACT_DIR, "artifact_v10_done_milestone_night_no_clash.png")
        target_node.screenshot(path=out2)
        print(f"Saved: {out2}")

        browser.close()
        print("=== ALL V10 VERIFICATION CHECKS PASSED ===")

if __name__ == "__main__":
    main()
