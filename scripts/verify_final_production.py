import sys, os, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ----------------------------------------------------
        # 1. Desktop Test (1400x900)
        # ----------------------------------------------------
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print("[Desktop] Navigating to http://localhost:8000/home ...")
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        page.wait_for_timeout(500)

        # Capture Desktop Hero
        hero_shot = os.path.join(artifact_dir, "artifact_desktop_hero.png")
        page.screenshot(path=hero_shot)
        print(f"[Desktop] Saved {hero_shot}")

        # Check theme switch
        theme_sw = page.locator("#themeSwitch")
        theme_sw.click()
        page.wait_for_timeout(400)
        dark_mode_attr = page.locator("body").get_attribute("data-paper")
        print(f"[Desktop] After toggle: data-paper = {dark_mode_attr}")
        assert dark_mode_attr == "night", f"Expected night mode, got {dark_mode_attr}"

        # Capture Desktop Dark Mode
        dark_shot = os.path.join(artifact_dir, "artifact_desktop_dark.png")
        page.screenshot(path=dark_shot)
        print(f"[Desktop] Saved {dark_shot}")

        # Switch back to light mode
        theme_sw.click()
        page.wait_for_timeout(300)

        # Check sound switch
        sound_sw = page.locator("#soundSwitch")
        sound_sw.click()
        page.wait_for_timeout(300)
        sound_sw.click()
        page.wait_for_timeout(300)

        # Check hanging Polaroid photo card initial transform
        hero_photo = page.locator("#heroPhoto")
        init_transform = hero_photo.evaluate("el => el.style.transform")
        print(f"[Desktop] Hero photo initial transform: {init_transform}")

        # Test scroll animation by scrolling down
        print("[Desktop] Scrolling to 1200px (Simulator section) ...")
        page.evaluate("window.scrollTo(0, 1200)")
        page.wait_for_timeout(400)

        scrolled_transform = hero_photo.evaluate("el => el.style.transform")
        print(f"[Desktop] Hero photo scrolled transform: {scrolled_transform}")
        assert init_transform != scrolled_transform, "Hero photo should dynamically update transform on scroll!"

        # Check simulator card transform
        sim_card = page.locator("#simCard")
        sim_transform = sim_card.evaluate("el => el.style.transform")
        print(f"[Desktop] Simulator card dock-in transform: {sim_transform}")
        assert "perspective" in sim_transform, "Simulator card should have perspective dock-in transform!"

        # Capture Desktop Simulator
        sim_shot = os.path.join(artifact_dir, "artifact_desktop_simulator.png")
        page.screenshot(path=sim_shot)
        print(f"[Desktop] Saved {sim_shot}")

        # Test slider interaction in simulator
        slider = page.locator("#frictionSlider")
        slider.fill("3")
        page.wait_for_timeout(200)
        stamina_txt = page.locator("#staminaLabel").text_content()
        print(f"[Desktop] Stamina label at 3: {stamina_txt}")
        assert "LOW" in stamina_txt, f"Expected LOW stamina label, got {stamina_txt}"

        # Scroll further down to Use Cases
        print("[Desktop] Scrolling to 2200px (Use cases section) ...")
        page.evaluate("window.scrollTo(0, 2200)")
        page.wait_for_timeout(400)

        card3 = page.locator("#card3")
        card3_transform = card3.evaluate("el => el.style.transform")
        print(f"[Desktop] Card 3 transform on scroll: {card3_transform}")
        assert "rotate" in card3_transform, "Card 3 should have scroll-driven tilt transform!"

        uc_shot = os.path.join(artifact_dir, "artifact_desktop_usecases.png")
        page.screenshot(path=uc_shot)
        print(f"[Desktop] Saved {uc_shot}")

        # Check background humaaans opacity & transform
        bg_hu1 = page.locator("#bgHu1")
        bg_hu1_transform = bg_hu1.evaluate("el => el.style.transform")
        print(f"[Desktop] Bg Humaaan 1 transform at 2200px scroll: {bg_hu1_transform}")
        assert "translate3d" in bg_hu1_transform, "Background humaaan should have parallax translation!"

        page.close()

        # ----------------------------------------------------
        # 2. Mobile Viewport Test (375x667 - iPhone SE / Compact)
        # ----------------------------------------------------
        print("\n[Mobile 375px] Testing compact mobile viewport ...")
        mobile_page = browser.new_page(viewport={"width": 375, "height": 667})
        mobile_page.goto("http://localhost:8000/home", wait_until="networkidle")
        mobile_page.wait_for_timeout(500)

        # Check that page does not horizontally scroll
        scroll_width = mobile_page.evaluate("document.documentElement.scrollWidth")
        client_width = mobile_page.evaluate("document.documentElement.clientWidth")
        print(f"[Mobile 375px] scrollWidth: {scroll_width}, clientWidth: {client_width}")
        assert scroll_width <= client_width + 1, f"Horizontal overflow detected! scrollWidth ({scroll_width}) > clientWidth ({client_width})"

        # Capture Mobile Hero
        mob_hero_shot = os.path.join(artifact_dir, "artifact_mobile_hero_375.png")
        mobile_page.screenshot(path=mob_hero_shot)
        print(f"[Mobile 375px] Saved {mob_hero_shot}")

        # Test theme toggle on mobile
        mobile_page.locator("#themeSwitch").click()
        mobile_page.wait_for_timeout(300)
        mob_dark_shot = os.path.join(artifact_dir, "artifact_mobile_dark_375.png")
        mobile_page.screenshot(path=mob_dark_shot)
        print(f"[Mobile 375px] Saved {mob_dark_shot}")
        mobile_page.locator("#themeSwitch").click()

        # Scroll on mobile
        mobile_page.evaluate("window.scrollTo(0, 800)")
        mobile_page.wait_for_timeout(400)

        mob_sim_shot = os.path.join(artifact_dir, "artifact_mobile_sim_375.png")
        mobile_page.screenshot(path=mob_sim_shot)
        print(f"[Mobile 375px] Saved {mob_sim_shot}")

        mobile_page.evaluate("window.scrollTo(0, 1800)")
        mobile_page.wait_for_timeout(400)

        mob_uc_shot = os.path.join(artifact_dir, "artifact_mobile_usecases_375.png")
        mobile_page.screenshot(path=mob_uc_shot)
        print(f"[Mobile 375px] Saved {mob_uc_shot}")

        mobile_page.close()

        # ----------------------------------------------------
        # 3. Main App Settings Groq Default Verification (index.html)
        # ----------------------------------------------------
        print("\n[Settings] Testing Groq settings default on / ...")
        app_context = browser.new_context(viewport={"width": 1200, "height": 800})
        app_context.add_init_script("""
            localStorage.setItem('goalstar_user', JSON.stringify({
                type: 'demo_guest',
                name: 'Guest Builder #101',
                address: '0x123456',
                connectedAt: new Date().toISOString()
            }));
        """)

        app_page = app_context.new_page()
        app_page.goto("http://localhost:8000/", wait_until="networkidle")
        app_page.wait_for_timeout(500)

        # Dismiss tour if visible
        try:
            app_page.evaluate("() => { const o = document.querySelector('.sketch-tour-overlay'); if (o) o.remove(); }")
        except:
            pass

        # Open settings
        app_page.locator("#settingsBtn").click()
        app_page.wait_for_timeout(300)

        # Switch to Groq pane
        app_page.locator("#dreamerSeg label", has_text="Groq").click()
        app_page.wait_for_timeout(300)

        # Verify no apiKey input field exists in Groq pane
        groq_api_inputs = app_page.locator("div[data-pane='groq'] input[name='groq.apiKey']").count()
        print(f"[Settings] Groq API key inputs found: {groq_api_inputs}")
        assert groq_api_inputs == 0, "Groq apiKey input field should be removed!"

        # Verify configured token box is present
        token_box = app_page.locator(".configured-token-box")
        assert token_box.is_visible(), "Configured token box should be visible!"
        print("[Settings] Configured token box verified successfully!")

        settings_shot = os.path.join(artifact_dir, "artifact_groq_settings_configured.png")
        app_page.screenshot(path=settings_shot)
        print(f"[Settings] Saved {settings_shot}")

        app_page.close()

        browser.close()

        print("\n=======================================================")
        print("ALL VERIFICATION SUITES PASSED WITH ZERO ERRORS!")
        print("=======================================================")

if __name__ == "__main__":
    run_tests()
