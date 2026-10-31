from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto('http://localhost:8000')
        
        items = page.evaluate('''() => {
            const side = document.querySelector('.side');
            return Array.from(side.children).map(c => ({
                tag: c.tagName,
                className: c.className,
                id: c.id,
                rect: c.getBoundingClientRect(),
                visible: c.offsetParent !== null
            }));
        }''')
        
        print("Side bar height/scroll:", page.evaluate('() => { const s = document.querySelector(".side"); return { height: s.clientHeight, scrollHeight: s.scrollHeight, scrollTop: s.scrollTop }; }'))
        for item in items:
            print(item)
            
        browser.close()

if __name__ == '__main__':
    inspect()
