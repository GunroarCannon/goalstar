from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1200, "height": 800})
    
    # Pre-set logged in guest in localStorage with correct key 'goalstar_user'
    page.goto("http://localhost:8000/home", wait_until="networkidle")
    page.evaluate('''() => {
        localStorage.setItem("goalstar_user", JSON.stringify({
            type: "demo_guest",
            name: "Guest Builder #101",
            address: "0x123456",
            connectedAt: new Date().toISOString()
        }));
    }''')

    # Now navigate to / (planner)
    page.goto("http://localhost:8000/", wait_until="networkidle")
    print("Current URL:", page.url)
    assert page.url == "http://localhost:8000/", f"Expected to remain on /, got {page.url}"

    # Dismiss tour if present
    page.wait_for_timeout(400)
    try:
        page.evaluate("() => { const o = document.querySelector('.sketch-tour-overlay'); if (o) o.remove(); }")
    except:
        pass

    # Open settings
    page.locator("#settingsBtn").click()
    page.wait_for_timeout(300)

    # Check Groq pane
    page.locator("input[name='dreamer'][value='groq']").check()
    page.wait_for_timeout(200)

    groq_api_inputs = page.locator("div[data-pane='groq'] input[name='groq.apiKey']").count()
    print("Groq apiKey inputs count:", groq_api_inputs)
    assert groq_api_inputs == 0, "No apiKey input should exist in Groq pane"

    box_txt = page.locator(".configured-token-box").text_content()
    print("Token box text:", box_txt)
    assert "Token Pre-Configured" in box_txt, "Configured token box text missing"

    artifact_shot = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7\artifact_groq_settings_configured.png"
    page.screenshot(path=artifact_shot)
    print("Screenshot saved to:", artifact_shot)

    browser.close()
    print("\nSUCCESS: Groq settings and token default verified with zero errors!")
