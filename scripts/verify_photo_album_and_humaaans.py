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
        await page.wait_for_timeout(800)
        
        # 1. Verify face sculpture is gone
        face_count = await page.locator('#sculptureCard').count()
        assert face_count == 0, f'Expected 0 face sculptures, found {face_count}!'
        print('[OK] Verified face sculpture is completely removed.')
        
        # 2. Verify Hanging Photo Album Card is visible
        assert await page.locator('#heroPhoto').is_visible(), 'Hanging Photo Card not visible!'
        assert await page.locator('.photo-pin-top').is_visible(), 'Clothespin clip not visible!'
        assert await page.locator('.polaroid-humaaan-hero').is_visible(), 'Hero Humaaan in Polaroid not visible!'
        print('[OK] Verified Hanging Photo Album Card with clothesline clip.')
        
        # 3. Verify Background Humaaans layer exists
        bg_items = await page.locator('.bg-humaaan-item').count()
        print(f'[INFO] Found {bg_items} background Humaaans figures.')
        assert bg_items >= 4, f'Expected at least 4 background Humaaans, found {bg_items}'
        
        # Capture Hero Photo Album screenshot
        await page.screenshot(path=os.path.join(art_dir, 'artifact_photo_album_hero.png'))
        print('[OK] Saved artifact_photo_album_hero.png')
        
        # 4. Scroll to test Parallax / Tween on Background Humaaans
        print('[2] Scrolling down to 1000px to test Humaaan 2 tween ...')
        await page.evaluate('window.scrollTo(0, 1000)')
        await page.wait_for_timeout(600)
        
        h2_transform = await page.evaluate("document.getElementById('bgHumaaan2').style.transform")
        h2_opacity = await page.evaluate("document.getElementById('bgHumaaan2').style.opacity")
        print(f'Humaaan 2 at scroll 1000px -> transform: {h2_transform}, opacity: {h2_opacity}')
        assert 'scale' in h2_transform, f'Expected scale tween, got {h2_transform}'
        assert 'rotate' in h2_transform, f'Expected rotate tween, got {h2_transform}'
        
        await page.screenshot(path=os.path.join(art_dir, 'artifact_bg_humaaans_scroll1.png'))
        print('[OK] Saved artifact_bg_humaaans_scroll1.png')
        
        # 5. Scroll further to 2200px to test Humaaan 3 & 4 tween
        print('[3] Scrolling down to 2200px to test Humaaan 3 & 4 tween ...')
        await page.evaluate('window.scrollTo(0, 2200)')
        await page.wait_for_timeout(600)
        
        h4_transform = await page.evaluate("document.getElementById('bgHumaaan4').style.transform")
        h4_opacity = await page.evaluate("document.getElementById('bgHumaaan4').style.opacity")
        print(f'Humaaan 4 at scroll 2200px -> transform: {h4_transform}, opacity: {h4_opacity}')
        assert 'scale' in h4_transform, f'Expected scale tween, got {h4_transform}'
        
        await page.screenshot(path=os.path.join(art_dir, 'artifact_bg_humaaans_scroll2.png'))
        print('[OK] Saved artifact_bg_humaaans_scroll2.png')
        
        # 6. Verify Photo Album Dark Mode
        print('[4] Testing Dark Mode ...')
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(400)
        await page.click('#themeSwitch')
        await page.wait_for_timeout(500)
        
        assert await page.evaluate("document.body.dataset.paper === 'night'"), 'Dark mode failed!'
        await page.screenshot(path=os.path.join(art_dir, 'artifact_photo_album_dark.png'))
        print('[OK] Saved artifact_photo_album_dark.png')
        
        await browser.close()
        print('=== ALL PHOTO ALBUM & BACKGROUND HUMAAANS TESTS PASSED 100%! ===')

asyncio.run(verify())
