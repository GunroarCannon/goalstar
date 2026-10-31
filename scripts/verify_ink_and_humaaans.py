import asyncio
import os
from playwright.async_api import async_playwright

async def verify():
    art_dir = r'C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7'
    os.makedirs(art_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1400, 'height': 900})
        
        print('[1] Navigating to http://localhost:8000/home ...')
        await page.goto('http://localhost:8000/home')
        await page.wait_for_timeout(1000)
        
        # Verify hero elements
        assert await page.locator('.ink-swash-svg').is_visible(), 'ink-swash-svg not visible!'
        assert await page.locator('.hero-humaaan-badge').is_visible(), 'hero-humaaan-badge not visible!'
        assert await page.locator('#sculptureCard').is_visible(), 'sculptureCard not visible!'
        
        # 1. Capture Hero Section (Ink underline + refined face + hero humaaan)
        await page.screenshot(path=os.path.join(art_dir, 'artifact_ink_hero.png'))
        print('[OK] Saved artifact_ink_hero.png')
        
        # 2. Test Thinker Statue Toggle
        await page.click('#toggleThinkerBtn')
        await page.wait_for_timeout(400)
        assert await page.locator('#thinkerOverlay').is_visible(), 'Thinker overlay not shown after click!'
        await page.screenshot(path=os.path.join(art_dir, 'artifact_thinker_statue.png'))
        print('[OK] Saved artifact_thinker_statue.png')
        
        # Toggle back to papercut mind
        await page.click('#toggleThinkerBtn')
        await page.wait_for_timeout(400)
        
        # 3. Scroll down to Use Cases with Humaaans & reduced text
        await page.evaluate('window.scrollTo(0, 1500)')
        await page.wait_for_timeout(800)
        
        # Verify humaaan images loaded in cards
        cards = await page.locator('.uc-card').count()
        print(f'[INFO] Found {cards} use case cards.')
        assert cards == 5, f'Expected 5 cards, got {cards}'
        
        humaaans = await page.locator('.uc-humaaan-img').count()
        print(f'[INFO] Found {humaaans} humaaans figures in cards.')
        assert humaaans == 5, f'Expected 5 humaaans, got {humaaans}'
        
        await page.screenshot(path=os.path.join(art_dir, 'artifact_humaaans_usecases.png'))
        print('[OK] Saved artifact_humaaans_usecases.png')
        
        # 4. Scroll further down to show Card 4 & 5 with Humaaans
        await page.evaluate('window.scrollTo(0, 2400)')
        await page.wait_for_timeout(800)
        await page.screenshot(path=os.path.join(art_dir, 'artifact_humaaans_scroll_end.png'))
        print('[OK] Saved artifact_humaaans_scroll_end.png')
        
        # 5. Dark Mode Verification
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(400)
        await page.click('#themeSwitch')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(art_dir, 'artifact_ink_hero_dark.png'))
        print('[OK] Saved artifact_ink_hero_dark.png')
        
        await browser.close()
        print('=== ALL VERIFICATIONS PASSED SUCCESSFULLY! ===')

asyncio.run(verify())
