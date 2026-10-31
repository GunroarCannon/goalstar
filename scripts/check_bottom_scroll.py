import sys
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto('http://localhost:8000/home')
    page.wait_for_load_state('networkidle')
    
    # Scroll to absolute bottom
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1000)
    
    info = page.evaluate("""() => {
        const btn = document.getElementById('card5LaunchBtn');
        const arrow = document.getElementById('travelingArrow');
        const activePath = document.getElementById('journeyActivePath');
        const track = document.getElementById('journeyTrack');
        
        const br = btn.getBoundingClientRect();
        const ar = arrow.getBoundingClientRect();
        const tr = track.getBoundingClientRect();
        const totalLen = activePath.getTotalLength();
        const endPt = activePath.getPointAtLength(totalLen);
        
        return {
            scrollY: window.scrollY,
            maxScroll: document.body.scrollHeight - window.innerHeight,
            btnTopInViewport: br.top,
            winH: window.innerHeight,
            arrowX: ar.left + ar.width/2,
            arrowY: ar.top + ar.height/2,
            btnX: br.left + br.width/2,
            btnY: br.top + br.height/2,
            pathEndX: tr.left + endPt.x,
            pathEndY: tr.top + endPt.y,
            dashArray: activePath.style.strokeDasharray,
            totalLen: totalLen
        };
    }""")
    
    print("Scroll info at bottom of page:")
    for k, v in info.items():
        print(f"  {k}: {v}")
        
    browser.close()
