import asyncio
import os
from playwright.async_api import async_playwright

async def test_switches():
    art_dir = r'C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7'
    os.makedirs(art_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1400, 'height': 900})
        
        print('[1] Navigating to http://localhost:8000/home ...')
        await page.goto('http://localhost:8000/home')
        await page.wait_for_timeout(600)
        
        # Check initial state of theme switch (LIGHT)
        theme_sw = page.locator('#themeSwitch')
        sound_sw = page.locator('#soundSwitch')
        
        theme_txt = (await theme_sw.locator('.track-label').text_content()).strip()
        sound_txt = (await sound_sw.locator('.track-label').text_content()).strip()
        print(f'Initial states -> Theme: {theme_txt}, Sound: {sound_txt}')
        assert theme_txt == 'LIGHT', f'Expected LIGHT, got {theme_txt}'
        assert sound_txt == 'AUDIO', f'Expected AUDIO, got {sound_txt}'
        
        # Capture close-up of initial light switches
        switches_container = page.locator('.landing-actions')
        await switches_container.screenshot(path=os.path.join(art_dir, 'artifact_switch_light.png'))
        print('[OK] Saved artifact_switch_light.png (Light state)')
        
        # Click Theme Switch -> Should change to DARK
        print('[2] Clicking #themeSwitch ...')
        await theme_sw.click()
        await page.wait_for_timeout(400)
        
        paper_attr = await page.evaluate('document.body.dataset.paper')
        theme_txt_after = (await theme_sw.locator('.track-label').text_content()).strip()
        print(f'After 1 click -> paper: {paper_attr}, Theme label: {theme_txt_after}')
        assert paper_attr == 'night', f'Expected paper=night, got {paper_attr}'
        assert theme_txt_after == 'DARK', f'Expected DARK, got {theme_txt_after}'
        
        # Capture close-up of dark switches
        await switches_container.screenshot(path=os.path.join(art_dir, 'artifact_switch_dark.png'))
        print('[OK] Saved artifact_switch_dark.png (Dark state)')
        
        # Click Theme Switch again -> Should toggle back to LIGHT
        print('[3] Clicking #themeSwitch again ...')
        await theme_sw.click()
        await page.wait_for_timeout(400)
        
        paper_attr2 = await page.evaluate('document.body.dataset.paper')
        theme_txt_back = (await theme_sw.locator('.track-label').text_content()).strip()
        print(f'After 2nd click -> paper: {paper_attr2}, Theme label: {theme_txt_back}')
        assert paper_attr2 == 'lined', f'Expected paper=lined, got {paper_attr2}'
        assert theme_txt_back == 'LIGHT', f'Expected LIGHT, got {theme_txt_back}'
        
        # Click Sound Switch -> Should toggle to MUTE
        print('[4] Clicking #soundSwitch ...')
        await sound_sw.click()
        await page.wait_for_timeout(400)
        
        sound_txt_after = (await sound_sw.locator('.track-label').text_content()).strip()
        sound_enabled = await page.evaluate('window.sound ? window.sound.enabled : null')
        print(f'After 1 sound click -> enabled: {sound_enabled}, Sound label: {sound_txt_after}')
        assert sound_txt_after == 'MUTE', f'Expected MUTE, got {sound_txt_after}'
        assert sound_enabled is False, f'Expected sound.enabled=False, got {sound_enabled}'
        
        # Click Sound Switch again -> Should toggle back to AUDIO
        print('[5] Clicking #soundSwitch again ...')
        await sound_sw.click()
        await page.wait_for_timeout(400)
        
        sound_txt_back = (await sound_sw.locator('.track-label').text_content()).strip()
        sound_enabled2 = await page.evaluate('window.sound ? window.sound.enabled : null')
        print(f'After 2nd sound click -> enabled: {sound_enabled2}, Sound label: {sound_txt_back}')
        assert sound_txt_back == 'AUDIO', f'Expected AUDIO, got {sound_txt_back}'
        assert sound_enabled2 is True, f'Expected sound.enabled=True, got {sound_enabled2}'
        
        # Now verify on the Planner page (index.html)
        print('[6] Navigating to Planner / ...')
        await page.evaluate("localStorage.setItem('goalstar_user', JSON.stringify({id: 'test_user', name: 'Tester', authType: 'guest'}))")
        await page.goto('http://localhost:8000/')
        await page.wait_for_timeout(600)
        
        # Close tour overlay if active
        if await page.locator('.sketch-tour-overlay').is_visible():
            await page.click('.sketch-tour-close')
            await page.wait_for_timeout(200)
            
        planner_theme_sw = page.locator('header.topbar #themeSwitch')
        planner_sound_sw = page.locator('header.topbar #soundSwitch')
        
        assert await planner_theme_sw.is_visible(), 'Planner theme switch not visible!'
        assert await planner_sound_sw.is_visible(), 'Planner sound switch not visible!'
        
        # Toggle theme on planner
        await planner_theme_sw.click()
        await page.wait_for_timeout(300)
        assert await page.evaluate("document.body.dataset.paper === 'night'"), 'Planner dark mode toggle failed!'
        
        # Toggle back on planner
        await planner_theme_sw.click()
        await page.wait_for_timeout(300)
        assert await page.evaluate("document.body.dataset.paper === 'lined'"), 'Planner light mode toggle failed!'
        
        await browser.close()
        print('=== ALL SWITCH & WORD TESTS PASSED 100%! ===')

asyncio.run(test_switches())
