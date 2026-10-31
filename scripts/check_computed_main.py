from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 375, "height": 667})
    page.goto("http://localhost:8000/home", wait_until="networkidle")

    res = page.evaluate('''() => {
        const m = document.querySelector('.landing-main');
        const comp = window.getComputedStyle(m);
        return {
            display: comp.display,
            flexDirection: comp.flexDirection,
            flexWrap: comp.flexWrap,
            width: comp.width
        };
    }''')
    print(res)
    browser.close()
