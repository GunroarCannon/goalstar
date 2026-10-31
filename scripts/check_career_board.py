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
    
    # Switch to "Get a good paying job" (second board)
    page.locator("#boardPick").select_option(index=1)
    page.wait_for_timeout(800)
    
    # Check elements on this board
    print("Nodes on board:", page.locator('.node').count())
    print("Elabels on board:", page.locator('.elabel').count())
    print("Hot elabels on board:", page.locator('.elabel.hot').count())
    
    for i in range(page.locator('.elabel').count()):
        el = page.locator('.elabel').nth(i)
        print(f"elabel {i}: visible={el.is_visible()}, bbox={el.bounding_box()}")
        
    browser.close()
