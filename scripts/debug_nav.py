from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8000/home')
    page.evaluate('() => localStorage.setItem("goalstar_user", JSON.stringify({ name: "Guest Builder #493", isGuest: true, id: "g_493" }))')
    page.goto('http://localhost:8000/')
    page.wait_for_timeout(1000)
    print('Final URL:', page.url)
    print('tourBtn count:', page.locator('#tourBtn').count())
    print('tourBtn classes:', page.locator('#tourBtn').get_attribute('class'))
    browser.close()
