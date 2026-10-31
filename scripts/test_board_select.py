from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8000/home')
    page.evaluate('() => localStorage.setItem("goalstar_user", JSON.stringify({ name: "Guest Builder #493", isGuest: true, id: "g_493" }))')
    page.goto('http://localhost:8000/')
    page.wait_for_timeout(1000)
    
    # Check boards
    opts = page.locator('#boardPick option').all_inner_texts()
    print('Board pick options:', opts)
    
    if len(opts) > 1:
        page.locator('#boardPick').select_option(index=1)
        page.wait_for_timeout(500)
    
    # Check if selectFirstStateNode works
    res = page.evaluate('() => window.selectFirstStateNode ? window.selectFirstStateNode() : "no function"')
    print('selectFirstStateNode returned:', res)
    page.wait_for_timeout(300)
    
    inspector_hidden = page.evaluate('() => document.querySelector("#inspector").hidden')
    inspector_html = page.evaluate('() => document.querySelector("#inspector").innerHTML')
    print('inspector hidden:', inspector_hidden)
    print('inspector text:', page.locator('#inspector').inner_text()[:200])
    
    browser.close()
