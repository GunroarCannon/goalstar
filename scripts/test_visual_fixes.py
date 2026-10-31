import time
from playwright.sync_api import sync_playwright

def test_fixes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Test 1: Desktop Viewport (1280px)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        time.sleep(0.5)

        # Verify scrollHud opacity is 0 at scroll 0
        hud = page.query_selector("#scrollHud")
        assert hud is not None, "scrollHud element missing!"
        hud_opacity = float(page.evaluate("() => getComputedStyle(document.getElementById('scrollHud')).opacity"))
        print("HUD opacity at top of page:", hud_opacity)
        assert hud_opacity == 0.0, f"Expected HUD opacity 0 at top, got {hud_opacity}"

        # Verify header nav links
        nav = page.query_selector(".landing-nav")
        assert nav is not None, "landing-nav missing!"
        nav_links = page.query_selector_all(".landing-nav a")
        link_texts = [a.inner_text().strip() for a in nav_links]
        print("Nav links:", link_texts)
        assert "A* Simulator" not in link_texts, "A* Simulator should be shortened to Simulator"
        
        # Check nav bounding boxes to ensure none wrap into multiple lines
        for a in nav_links:
            box = a.bounding_box()
            print(f"Nav item '{a.inner_text()}' height: {box['height']}px")
            # In single line it should be ~20px, wrapped would be ~36px+
            assert box['height'] < 28, f"Nav item '{a.inner_text()}' wrapped unexpectedly! Height: {box['height']}"

        # Check Infrastructure Deck
        deck = page.query_selector(".infra-console-deck")
        assert deck is not None, "infra-console-deck missing!"
        print("Found unified infra-console-deck!")

        # Verify Step 4 nodes do NOT overflow/come out of container
        deck_box = deck.bounding_box()
        stages = page.query_selector_all(".icd-stage[data-stage='4']")
        for s in stages:
            label = s.query_selector(".icd-label")
            s_box = s.bounding_box()
            l_box = label.bounding_box()
            print(f"Stage 4 label '{label.inner_text()}' right edge: {l_box['x'] + l_box['width']}, deck right: {deck_box['x'] + deck_box['width']}")
            assert l_box['x'] + l_box['width'] <= deck_box['x'] + deck_box['width'] + 5, "Stage 4 label overflows deck!"

        # Scroll to infrastructure section
        page.evaluate("() => document.getElementById('infrastructure').scrollIntoView()")
        time.sleep(0.5)

        # Check progress tracks filled
        walrus_width = page.evaluate("() => document.getElementById('walrusScrollTrackFill').style.width")
        tatum_width = page.evaluate("() => document.getElementById('tatumScrollTrackFill').style.width")
        print("Walrus track width on scroll:", walrus_width)
        print("Tatum track width on scroll:", tatum_width)
        assert walrus_width != "0%" and walrus_width != "", "Walrus track did not fill on scroll!"
        assert tatum_width != "0%" and tatum_width != "", "Tatum track did not fill on scroll!"

        # Take screenshot of header and infra console deck
        page.screenshot(path="scratch_infra_deck.png")
        print("Screenshot saved to scratch_infra_deck.png")

        # Test 2: Moderate width viewport (1050px) where wrapping previously occurred
        page.set_viewport_size({"width": 1050, "height": 900})
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        time.sleep(0.5)
        nav_links_1050 = page.query_selector_all(".landing-nav a")
        for a in nav_links_1050:
            box = a.bounding_box()
            assert box['height'] < 28, f"Nav item '{a.inner_text()}' wrapped at 1050px width!"
        print("1050px viewport nav wrap test passed!")

        browser.close()
        print("ALL VISUAL AND LAYOUT VERIFICATIONS PASSED!")

if __name__ == "__main__":
    test_fixes()
