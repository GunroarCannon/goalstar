import asyncio
import os
from playwright.async_api import async_playwright

async def capture():
    art_dir = r'C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7'
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1400, 'height': 900})
        
        # 1. Home page light
        await page.goto('http://localhost:8000/home')
        await page.wait_for_timeout(800)
        await page.screenshot(path=os.path.join(art_dir, 'curr_home_light.png'))
        print('[OK] Captured curr_home_light.png')
        
        # 2. Toggle to dark mode
        await page.click('#themeSwitch')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(art_dir, 'curr_home_dark.png'))
        print('[OK] Captured curr_home_dark.png')
        
        # 3. Scroll down on home
        await page.evaluate('window.scrollTo(0, 1600)')
        await page.wait_for_timeout(800)
        await page.screenshot(path=os.path.join(art_dir, 'curr_home_scrolled.png'))
        print('[OK] Captured curr_home_scrolled.png')
        
        # 4. Open planner from home
        await page.click('button.launch-btn')
        await page.wait_for_url('http://localhost:8000/', timeout=5000)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(art_dir, 'curr_planner_main.png'))
        print('[OK] Captured curr_planner_main.png')
        
        # 5. Check the tour popup step 1 in planner
        await page.click('#tourBtn')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(art_dir, 'curr_tour_step1.png'))
        print('[OK] Captured curr_tour_step1.png')
        
        # 6. Step 2 in tour
        await page.click('#tourNextBtn')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(art_dir, 'curr_tour_step2.png'))
        print('[OK] Captured curr_tour_step2.png')
        
        # 7. Step 3 in tour (A* node pointing)
        await page.click('#tourNextBtn')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(art_dir, 'curr_tour_step3.png'))
        print('[OK] Captured curr_tour_step3.png')

        await browser.close()
        print('All views captured successfully!')

asyncio.run(capture())
