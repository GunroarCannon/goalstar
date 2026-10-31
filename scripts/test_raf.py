from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 900})
    page.goto("http://localhost:8000/home", wait_until="networkidle")

    t0 = page.locator("#heroPhoto").evaluate("el => el.style.transform")
    print("t0:", t0)

    # Scroll
    page.evaluate("window.scrollTo(0, 1000)")
    # Wait for RAF
    page.evaluate("() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")

    t1 = page.locator("#heroPhoto").evaluate("el => el.style.transform")
    print("t1:", t1)

    scrollY = page.evaluate("window.scrollY")
    print("scrollY:", scrollY)

    browser.close()
