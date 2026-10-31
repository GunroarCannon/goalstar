import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1200, "height": 800})
    
    context.add_init_script("""
        localStorage.setItem('goalstar_user', JSON.stringify({
            type: 'demo_guest',
            name: 'Guest Builder #101',
            address: '0x123456',
            connectedAt: new Date().toISOString()
        }));
    """)

    page = context.new_page()
    page.goto("http://localhost:8000/", wait_until="networkidle")
    print("Page loaded, URL:", page.url)

    # Dismiss any tour overlay immediately
    page.evaluate("() => { const o = document.querySelector('.sketch-tour-overlay'); if (o) o.remove(); }")

    # Click settings button
    print("Clicking #settingsBtn ...")
    page.locator("#settingsBtn").click()
    page.wait_for_timeout(300)

    # Click the visible Groq label in the segmented control
    print("Clicking Groq label ...")
    page.locator("#dreamerSeg label", has_text="Groq").click()
    page.wait_for_timeout(300)

    # Verify Groq pane is visible
    groq_pane = page.locator("div[data-pane='groq']")
    is_vis = groq_pane.is_visible()
    print("Groq pane is visible:", is_vis)
    assert is_vis, "Groq pane should be visible"

    # Verify no apiKey input field exists in Groq pane
    groq_api_inputs = page.locator("div[data-pane='groq'] input[name='groq.apiKey']").count()
    print("Groq apiKey inputs count:", groq_api_inputs)
    assert groq_api_inputs == 0, "No apiKey input should exist in Groq pane"

    # Verify configured token box
    box_txt = page.locator(".configured-token-box").text_content()
    print("Token box text:", box_txt.strip().replace('\n', ' '))
    assert "Token Pre-Configured" in box_txt, "Configured token box text missing"

    artifact_shot = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7\artifact_groq_settings_configured.png"
    page.screenshot(path=artifact_shot)
    print("Screenshot saved to:", artifact_shot)

    browser.close()
    print("\nSUCCESS: Groq settings and token default verified with zero errors!")
