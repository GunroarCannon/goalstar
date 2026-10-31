import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto('http://localhost:8000/home')
    page.evaluate("() => localStorage.setItem('goalstar_user', JSON.stringify({ type: 'guest', id: 'Guest#454' }))")
    page.goto('http://localhost:8000/', wait_until='networkidle')
    page.wait_for_timeout(1000)
    
    # Check what elabel and cost exist
    elabels = page.locator('.elabel').count()
    print('Total .elabel count:', elabels)
    costs = page.locator('.cost').count()
    print('Total .cost count:', costs)
    
    for i in range(min(5, costs)):
        c = page.locator('.cost').nth(i)
        box = c.bounding_box()
        text = c.inner_text()
        print(f'Cost {i} [{text}]: {box}')
        
    hot_cost = page.locator('.elabel.hot .cost')
    print('hot_cost count:', hot_cost.count())
    if hot_cost.count() > 0:
        print('hot_cost bbox:', hot_cost.first.bounding_box())

    browser.close()
