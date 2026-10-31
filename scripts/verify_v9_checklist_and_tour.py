import os
import time
from playwright.sync_api import sync_playwright

BRAIN_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
        page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}") if msg.type in ['error', 'warn'] else None)

        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.evaluate("""() => {
            localStorage.setItem('goalstar_user', JSON.stringify({ name: 'Guest Builder #493', isGuest: true, id: 'g_493' }));
        }""")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_timeout(1000)

        print("\n=== TEST 1: Checklist Ticking & Dynamic Node Progress Bar ===")
        # Select first edge and explicitly set 3 checklist steps
        page.evaluate("""() => {
            if (window.selectFirstEdge) window.selectFirstEdge();
            const b = window.canvas?.board;
            const selId = window.canvas?.o?.sel?.id;
            if (b && selId && b.edges[selId]) {
                b.edges[selId].steps = [
                    { text: '1. Architecture & schema design', done: false },
                    { text: '2. Implementation & test suites', done: false },
                    { text: '3. Production deployment & verify', done: false }
                ];
                if (b.nodes[b.edges[selId].to]) {
                    b.nodes[b.edges[selId].to].done = false;
                }
                if (window.canvas) window.canvas.render(b, window.canvas.o);
            }
        }""")
        page.wait_for_timeout(500)

        # Re-select edge to re-render inspector with the 3 steps
        page.evaluate("() => { if (window.selectFirstEdge) window.selectFirstEdge(); }")
        page.wait_for_timeout(500)

        # Check initial progress bar width on target node
        initial_info = page.evaluate("""() => {
            const edge = window.canvas?.board?.edges[window.canvas?.o?.sel?.id];
            const toNodeId = edge ? edge.to : null;
            const nodeEl = toNodeId ? document.querySelector(`.node[data-id="${toNodeId}"]`) : null;
            const barI = nodeEl ? nodeEl.querySelector('.near i') : null;
            const badge = nodeEl ? nodeEl.querySelector('.card-step-badge') : null;
            return {
                toNodeId,
                width: barI ? barI.style.width : 'none',
                badgeText: badge ? badge.textContent : 'none'
            };
        }""")
        print(f"Initial State Node ({initial_info['toNodeId']}): width={initial_info['width']}, badge={initial_info['badgeText']}")
        assert initial_info['width'] == "0%", f"Initial width should be 0%, got {initial_info['width']}"
        assert initial_info['badgeText'] == "0/3", f"Initial badge should be 0/3, got {initial_info['badgeText']}"

        # Tick 1st checklist step
        print("Ticking step 1 of 3...")
        page.locator("#inspector input[data-step='0']").check()
        page.wait_for_timeout(350)
        p1 = page.evaluate("""() => {
            const edge = window.canvas?.board?.edges[window.canvas?.o?.sel?.id];
            const nodeEl = document.querySelector(`.node[data-id="${edge.to}"]`);
            const barI = nodeEl ? nodeEl.querySelector('.near i') : null;
            const badge = nodeEl ? nodeEl.querySelector('.card-step-badge') : null;
            return { width: barI ? barI.style.width : 'none', badge: badge ? badge.textContent : 'none' };
        }""")
        print(f"After step 1 checked: width={p1['width']}, badge={p1['badge']}")
        assert "33%" in p1['width'] or "34%" in p1['width'], f"Width should be ~33%, got {p1['width']}"
        assert p1['badge'] == "1/3", f"Badge should be 1/3, got {p1['badge']}"

        # Tick 2nd checklist step
        print("Ticking step 2 of 3...")
        page.locator("#inspector input[data-step='1']").check()
        page.wait_for_timeout(350)
        p2 = page.evaluate("""() => {
            const edge = window.canvas?.board?.edges[window.canvas?.o?.sel?.id];
            const nodeEl = document.querySelector(`.node[data-id="${edge.to}"]`);
            const barI = nodeEl ? nodeEl.querySelector('.near i') : null;
            const badge = nodeEl ? nodeEl.querySelector('.card-step-badge') : null;
            return { width: barI ? barI.style.width : 'none', badge: badge ? badge.textContent : 'none' };
        }""")
        print(f"After step 2 checked: width={p2['width']}, badge={p2['badge']}")
        assert "67%" in p2['width'] or "66%" in p2['width'], f"Width should be ~67%, got {p2['width']}"
        assert p2['badge'] == "2/3", f"Badge should be 2/3, got {p2['badge']}"

        # Tick 3rd checklist step (all done!)
        print("Ticking step 3 of 3 (all done)...")
        page.locator("#inspector input[data-step='2']").check()
        page.wait_for_timeout(450)
        p3 = page.evaluate("""() => {
            const edge = window.canvas?.board?.edges[window.canvas?.o?.sel?.id];
            const nodeEl = document.querySelector(`.node[data-id="${edge.to}"]`);
            const barI = nodeEl ? nodeEl.querySelector('.near i') : null;
            const badge = nodeEl ? nodeEl.querySelector('.card-step-badge') : null;
            return { width: barI ? barI.style.width : 'none', badge: badge ? badge.textContent : 'none', isDone: nodeEl?.classList.contains('done') };
        }""")
        print(f"After step 3 checked: width={p3['width']}, badge={p3['badge']}, isDone={p3['isDone']}")
        assert "100%" in p3['width'], f"Width should be 100%, got {p3['width']}"
        assert p3['isDone'] is True, "Node should be marked achieved (done) when all steps are ticked!"

        # Take screenshot of ticked milestone card
        shot1 = os.path.join(BRAIN_DIR, "artifact_v9_checklist_ticked_node.png")
        page.screenshot(path=shot1)
        print(f"Saved: {shot1}")

        # Untick step 3
        print("Unticking step 3 (reverting back to 2/3)...")
        page.locator("#inspector input[data-step='2']").uncheck()
        page.wait_for_timeout(350)
        p_revert = page.evaluate("""() => {
            const edge = window.canvas?.board?.edges[window.canvas?.o?.sel?.id];
            const nodeEl = document.querySelector(`.node[data-id="${edge.to}"]`);
            const barI = nodeEl ? nodeEl.querySelector('.near i') : null;
            const badge = nodeEl ? nodeEl.querySelector('.card-step-badge') : null;
            return { width: barI ? barI.style.width : 'none', badge: badge ? badge.textContent : 'none', isDone: nodeEl?.classList.contains('done') };
        }""")
        print(f"After unticking step 3: width={p_revert['width']}, badge={p_revert['badge']}, isDone={p_revert['isDone']}")
        assert "67%" in p_revert['width'] or "66%" in p_revert['width'], f"Width should revert to 67%, got {p_revert['width']}"
        assert p_revert['isDone'] is False, "Node should no longer be marked achieved!"

        print("\n=== TEST 2: Testing Connect Banner UX ===")
        page.evaluate("() => { if (window.selectFirstStateNode) window.selectFirstStateNode(); }")
        page.wait_for_timeout(300)
        page.locator("#inspector button[data-act='link']").click()
        page.wait_for_timeout(300)
        banner_visible = page.evaluate("() => !document.getElementById('linkBanner')?.hidden")
        print(f"Connect banner visible: {banner_visible}")
        assert banner_visible is True, "Connect banner must be visible during connect mode"
        page.locator("#cancelLinkBtn").click()
        page.wait_for_timeout(200)
        banner_hidden = page.evaluate("() => document.getElementById('linkBanner')?.hidden")
        assert banner_hidden is True, "Connect banner must hide when cancelled"
        print("Connect banner UX passed!")

        print("\n=== TEST 3: Testing 8-Step Walkthrough Tour ===")
        # Launch tour
        page.evaluate("() => { if (window.tour) window.tour.start(true); }")
        page.wait_for_selector(".sketch-card-container", timeout=6000)
        page.wait_for_timeout(300)

        for step_idx in range(1, 9):
            page.wait_for_selector(".sketch-card-container", timeout=4000)
            page.wait_for_timeout(250)
            step_info = page.evaluate(f"""() => {{
                const card = document.querySelector('.sketch-card-container');
                const cr = card ? card.getBoundingClientRect() : null;
                const spot = document.querySelector('#sketch-mask rect:nth-child(2)');
                const title = document.querySelector('.sketch-title')?.textContent;
                return {{
                    step: {step_idx},
                    title: title,
                    cardTop: cr ? cr.top : null,
                    cardBottom: cr ? cr.bottom : null,
                    cardLeft: cr ? cr.left : null,
                    cardRight: cr ? cr.right : null,
                    spotX: spot ? parseFloat(spot.getAttribute('x')) : null,
                    spotY: spot ? parseFloat(spot.getAttribute('y')) : null,
                    spotW: spot ? parseFloat(spot.getAttribute('width')) : null,
                    spotH: spot ? parseFloat(spot.getAttribute('height')) : null
                }};
            }}""")

            print(f"Step {step_idx} [{step_info['title']}]:")
            print(f"  Card: top={step_info['cardTop']:.1f}, bottom={step_info['cardBottom']:.1f}, left={step_info['cardLeft']:.1f}, right={step_info['cardRight']:.1f}")
            print(f"  Spot: x={step_info['spotX']:.1f}, y={step_info['spotY']:.1f}, w={step_info['spotW']:.1f}, h={step_info['spotH']:.1f}")

            # Verify no clipping
            assert step_info['cardBottom'] <= 800 - 8, f"Card bottom ({step_info['cardBottom']}) exceeds viewport!"
            assert step_info['cardTop'] >= 65, f"Card top ({step_info['cardTop']}) clips into top!"
            assert step_info['spotY'] >= 65, f"Spotlight y ({step_info['spotY']}) clips header!"
            assert step_info['spotW'] >= 20, f"Spotlight width ({step_info['spotW']}) too small!"

            # Take screenshot of key steps
            if step_idx in [2, 3, 5, 6, 7, 8]:
                shot_path = os.path.join(BRAIN_DIR, f"artifact_v9_tour_step_{step_idx}.png")
                page.screenshot(path=shot_path)
                print(f"  Saved screenshot: {shot_path}")

            if step_idx < 8:
                page.locator("#tourNextBtn").click()

        # Finish tour
        page.locator("#tourNextBtn").click()
        page.wait_for_timeout(300)

        # Test Laptop Viewport (1024x640) for zero clipping on all 8 steps
        print("\n=== TEST 4: Testing Laptop (1024x640) Zero Clipping on all 8 Steps ===")
        page.set_viewport_size({"width": 1024, "height": 640})
        page.wait_for_timeout(400)
        page.evaluate("() => { if (window.tour) window.tour.start(true); }")
        page.wait_for_selector(".sketch-card-container", timeout=6000)
        page.wait_for_timeout(250)

        for step_idx in range(1, 9):
            page.wait_for_selector(".sketch-card-container", timeout=4000)
            page.wait_for_timeout(200)
            r = page.evaluate("""() => {
                const c = document.querySelector('.sketch-card-container');
                const b = c ? c.getBoundingClientRect() : null;
                return { top: b?.top, bottom: b?.bottom };
            }""")
            print(f"Laptop Step {step_idx}: card top={r['top']:.1f}, bottom={r['bottom']:.1f} (max 640)")
            assert r['bottom'] <= 640 - 8, f"Laptop Step {step_idx} clipped at bottom: {r['bottom']}"
            assert r['top'] >= 65, f"Laptop Step {step_idx} clipped at top: {r['top']}"
            if step_idx == 3:
                page.screenshot(path=os.path.join(BRAIN_DIR, "artifact_v9_laptop_step3_bestpath.png"))
            elif step_idx == 5:
                page.screenshot(path=os.path.join(BRAIN_DIR, "artifact_v9_laptop_step5_checklist.png"))
            elif step_idx == 8:
                page.screenshot(path=os.path.join(BRAIN_DIR, "artifact_v9_laptop_step8_sui_optional.png"))

            if step_idx < 8:
                page.locator("#tourNextBtn").click()

        browser.close()
        print("\nALL V9 VERIFICATIONS COMPLETED WITH 100% SUCCESS!")

if __name__ == "__main__":
    main()
