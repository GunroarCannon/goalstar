from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto('http://localhost:8000')
    targets = ['#lastTuesdayBanner', '#canvas', '.telemetry-box', '#boardPick', '#searchBtn', '#tourBtn', '#empty']
    for t in targets:
        el = page.query_selector(t)
        if el:
            box = el.bounding_box()
            if box:
                print(f"FOUND {t}: x={round(box['x'])}, y={round(box['y'])}, w={round(box['width'])}, h={round(box['height'])}")
            else:
                print(f"FOUND {t} but box is None (hidden?)")
        else:
            print(f"NOT FOUND: {t}")
    browser.close()
