from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 375, "height": 667})
    page.goto("http://localhost:8000/home", wait_until="networkidle")

    overflowing = page.evaluate('''() => {
        const docW = document.documentElement.clientWidth;
        const bad = [];
        document.querySelectorAll('*').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.right > docW + 1 || rect.width > docW + 1) {
                bad.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    width: Math.round(rect.width),
                    right: Math.round(rect.right),
                    scrollWidth: el.scrollWidth
                });
            }
        });
        return bad;
    }''')

    print(f"Total overflowing elements: {len(overflowing)}")
    for b in overflowing[:20]:
        print(b)
    browser.close()
