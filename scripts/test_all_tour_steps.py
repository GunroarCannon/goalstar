import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        # Set guest user in localStorage
        page.goto('http://localhost:8000/home')
        page.evaluate("""() => {
            localStorage.setItem('goalstar_user', JSON.stringify({
                name: 'Guest Builder',
                mode: 'guest',
                walrusBlobId: 'demo-guest-blob'
            }));
        }""")

        page.goto('http://localhost:8000/')
        page.wait_for_selector('#paper', timeout=10000)
        time.sleep(1)

        # Start tour
        page.evaluate('() => { window.tour?.start(); }')
        time.sleep(0.5)

        total_steps = page.evaluate('() => window.tour?.steps?.length || 0')
        print(f"Total tour steps: {total_steps}")

        os.makedirs('tour_audit_run', exist_ok=True)

        for step_idx in range(total_steps):
            step_info = page.evaluate("""(idx) => {
                const tour = window.tour;
                const step = tour.steps[idx];
                const card = document.getElementById('tour-card');
                const spotlight = document.getElementById('tour-spotlight');
                const target = step.targetSelector ? step.targetSelector() : null;
                const tRect = target ? target.getBoundingClientRect() : null;
                const cRect = card ? card.getBoundingClientRect() : null;
                const sRect = spotlight ? spotlight.getBoundingClientRect() : null;
                return {
                    id: step.id,
                    title: step.title,
                    targetFound: !!target,
                    targetTag: target ? target.tagName : null,
                    targetClass: target ? target.className : null,
                    tRect: tRect ? { left: tRect.left, top: tRect.top, width: tRect.width, height: tRect.height } : null,
                    cRect: cRect ? { left: cRect.left, top: cRect.top, width: cRect.width, height: cRect.height } : null,
                    sRect: sRect ? { left: sRect.left, top: sRect.top, width: sRect.width, height: sRect.height } : null,
                };
            }""", step_idx)

            print(f"Step {step_idx+1}/{total_steps} [{step_info['id']}]: {step_info['title']}")
            print(f"  Target found: {step_info['targetFound']}, tag: {step_info['targetTag']}, sRect: {step_info['sRect']}")
            print(f"  Card rect: {step_info['cRect']}")

            cr = step_info['cRect']
            if cr:
                clipped = cr['left'] < 0 or cr['top'] < 0 or (cr['left'] + cr['width'] > 1285) or (cr['top'] + cr['height'] > 805)
                if clipped:
                    print(f"  WARNING: CARD CLIPPED! {cr}")

            page.screenshot(path=f"tour_audit_run/step_{step_idx+1}_{step_info['id']}.png")

            if step_idx < total_steps - 1:
                page.evaluate('() => { window.tour?.next(); }')
                time.sleep(0.4)

        browser.close()

if __name__ == '__main__':
    run()
