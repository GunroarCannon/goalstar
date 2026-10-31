from playwright.sync_api import sync_playwright

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto('http://localhost:8000')
        page.evaluate('localStorage.setItem("goalstar_walkthrough_completed", "true")')
        page.reload()
        page.wait_for_timeout(2000)
        page.screenshot(path='tour_screenshots/raw_page.png')
        browser.close()

if __name__ == '__main__':
    capture()
