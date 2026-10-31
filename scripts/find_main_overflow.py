from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 375, "height": 667})
    page.goto("http://localhost:8000/home", wait_until="networkidle")

    direct_children = page.evaluate('''() => {
        return Array.from(document.body.children).map(el => {
            const r = el.getBoundingClientRect();
            return {
                tag: el.tagName,
                id: el.id,
                className: el.className,
                left: Math.round(r.left),
                right: Math.round(r.right),
                width: Math.round(r.width),
                scrollWidth: el.scrollWidth
            };
        });
    }''')

    for c in direct_children:
        print(c)

    main_children = page.evaluate('''() => {
        const m = document.querySelector('.landing-main');
        if (!m) return [];
        return Array.from(m.children).map(el => {
            const r = el.getBoundingClientRect();
            return {
                tag: el.tagName,
                id: el.id,
                className: el.className,
                left: Math.round(r.left),
                right: Math.round(r.right),
                width: Math.round(r.width),
                scrollWidth: el.scrollWidth
            };
        });
    }''')

    print("\n--- Main children ---")
    for c in main_children:
        print(c)

    browser.close()
