from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto("http://localhost:8000/home", wait_until="networkidle")
        
        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(600)
        
        # Check arrow state
        is_circle = page.evaluate("""() => {
            const arr = document.getElementById('travelingArrow');
            return arr ? arr.classList.contains('is-circle') : false;
        }""")
        print(f"Traveling arrow is-circle class present: {is_circle}")
        
        # Take screenshot of bottom terminal area
        page.screenshot(path=r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7\artifact_v8_home_bottom_circle.png")
        print("Captured artifact_v8_home_bottom_circle.png")
        browser.close()

if __name__ == "__main__":
    main()
