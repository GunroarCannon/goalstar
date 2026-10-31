import time
from playwright.sync_api import sync_playwright

def test_home_page():
    print("=== TESTING HOME PAGE ENHANCEMENTS ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        
        # 1. Check Hero Badge
        hero_badge = page.query_selector("#heroBadge")
        assert hero_badge is not None, "Hero badge missing!"
        badge_text = hero_badge.inner_text()
        print("Hero Badge Text:", badge_text)
        assert "WALRUS MEMORY" in badge_text, "Walrus missing from hero badge!"
        assert "TATUM RPC" in badge_text, "Tatum missing from hero badge!"
        
        # 2. Check Infrastructure Section
        infra_sec = page.query_selector("#infrastructure")
        assert infra_sec is not None, "Infrastructure section missing!"
        print("Found Infrastructure section! Bounding box:", infra_sec.bounding_box())
        
        walrus_card = page.query_selector(".walrus-showcase")
        assert walrus_card is not None, "Walrus showcase card missing!"
        print("Found Walrus showcase card:", walrus_card.inner_text()[:60], "...")
        
        tatum_card = page.query_selector(".tatum-showcase")
        assert tatum_card is not None, "Tatum showcase card missing!"
        print("Found Tatum showcase card:", tatum_card.inner_text()[:60], "...")
        
        # 3. Check Tech Pills on Use Cases
        pills = page.query_selector_all(".uc-tech-pill")
        print(f"Found {len(pills)} use-case tech attribution pills!")
        assert len(pills) >= 5, f"Expected at least 5 tech pills on use case cards, got {len(pills)}"
        
        # 4. Check Footer Status Strip
        footer_status = page.query_selector(".footer-tech-status-row")
        assert footer_status is not None, "Footer tech status strip missing!"
        print("Footer status strip:", footer_status.inner_text())
        
        # 5. Check Tooltip Animation on Home Page
        print("\n--- Testing Tooltip Animations on Home Page ---")
        btn = page.query_selector("#heroLaunchBtn")
        btn.hover()
        # showTimer is 120ms debounce
        page.evaluate("() => new Promise(r => setTimeout(r, 160))")
        
        in_info = page.evaluate("""() => {
            const tip = document.querySelector('.gs-tip');
            if (!tip) return null;
            const anim = tip.getAnimations()[0];
            return {
                classes: tip.className,
                opacity: window.getComputedStyle(tip).opacity,
                transform: window.getComputedStyle(tip).transform,
                duration: anim ? anim.effect.getTiming().duration : null,
                easing: anim ? anim.effect.getTiming().easing : null,
            };
        }""")
        print("Tooltip during show animation:", in_info)
        assert in_info is not None, "Tooltip element not created!"
        assert "gs-tip" in in_info["classes"], "Missing .gs-tip class"
        assert in_info["duration"] == 280, f"Expected 280ms duration, got {in_info['duration']}"
        assert in_info["easing"] == "cubic-bezier(0.55, 0.085, 0.68, 0.53)", f"Expected in-quad easing, got {in_info['easing']}"
        
        # Wait for animation to finish (280ms + buffer)
        page.evaluate("""async () => {
            const tip = document.querySelector('.gs-tip');
            const anim = tip ? tip.getAnimations()[0] : null;
            if (anim) await anim.finished;
        }""")
        settled_info = page.evaluate("""() => {
            const tip = document.querySelector('.gs-tip');
            const anim = tip ? tip.getAnimations()[0] : null;
            return {
                classes: tip.className,
                opacity: window.getComputedStyle(tip).opacity,
                transform: window.getComputedStyle(tip).transform,
                anim_time: anim ? anim.currentTime : null,
                anim_state: anim ? anim.playState : null,
            };
        }""")
        print("Tooltip settled:", settled_info)
        assert settled_info["opacity"] == "1", "Settled opacity should be 1"
        assert "matrix(1, 0, 0, 1, 0, 0)" in settled_info["transform"], "Settled transform should be scale(1) rotate(0deg)"
        
        # Test out-animation
        page.mouse.move(10, 10) # Move away
        page.wait_for_timeout(60) # Right when hide begins
        out_info = page.evaluate("""() => {
            const tip = document.querySelector('.gs-tip');
            const anim = tip ? tip.getAnimations()[0] : null;
            return {
                classes: tip ? tip.className : null,
                duration: anim ? anim.effect.getTiming().duration : null,
            };
        }""")
        print("Tooltip during hide out-bounce:", out_info)
        assert "out" in out_info["classes"], "Should have .out class"
        assert out_info["duration"] == 400, f"Expected 400ms duration, got {out_info['duration']}"
        
        # Take a screenshot of the new infrastructure section
        page.screenshot(path="tour_screenshots/infrastructure_showcase.png")
        print("Saved screenshot: tour_screenshots/infrastructure_showcase.png")
        
        browser.close()
    print("=== HOME PAGE VERIFICATION PASSED! ===\n")

def test_app_page():
    print("=== TESTING PLANNER APP PAGE ENHANCEMENTS ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        
        # Login guest and go to app
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.evaluate("""() => {
            localStorage.setItem('goalstar_user', JSON.stringify({ name: 'Guest Builder #493', isGuest: true, id: 'g_493' }));
        }""")
        page.goto("http://localhost:8000/", wait_until="networkidle")
        page.wait_for_selector(".node", timeout=10000)
        page.wait_for_timeout(1000)
        
        # Check seed button
        seed_btn = page.query_selector("#seedMemoryBtn")
        assert seed_btn is not None, "#seedMemoryBtn missing from telemetry section!"
        print("Found Seed 10 Memories button:", seed_btn.inner_text())
        
        # Check telemetry pills
        walrus_badge = page.query_selector("#walrusCountBadge")
        assert walrus_badge is not None, "#walrusCountBadge missing!"
        print("Walrus telemetry badge:", walrus_badge.inner_text())
        
        tatum_badge = page.query_selector("#tatumRpcBadge")
        assert tatum_badge is not None, "#tatumRpcBadge missing!"
        print("Tatum RPC badge:", tatum_badge.inner_text())
        
        # Check Tuesday banner
        tuesday_banner = page.query_selector("#lastTuesdayBanner")
        assert tuesday_banner is not None, "Tuesday banner missing!"
        print("Tuesday banner tag:", tuesday_banner.query_selector(".tuesday-tag").inner_text())
        
        # Test tooltip on app page
        dream_btn = page.query_selector("#dreamBtn")
        dream_btn.hover()
        page.wait_for_timeout(150)
        app_tip = page.query_selector(".gs-tip")
        assert app_tip is not None, "Tooltip failed on app page!"
        print("App page tooltip text:", app_tip.inner_text())
        
        page.screenshot(path="tour_screenshots/app_telemetry_enhanced.png")
        print("Saved screenshot: tour_screenshots/app_telemetry_enhanced.png")
        
        browser.close()
    print("=== PLANNER APP VERIFICATION PASSED! ===\n")

if __name__ == "__main__":
    test_home_page()
    test_app_page()
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
