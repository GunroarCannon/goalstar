import sys, os, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_DIR = r"C:\Users\hmmm\.gemini\antigravity-cli\brain\bc449170-5592-49dd-893c-ab2b5bd73ca7"

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        
        # Pre-seed auth so navigating to / doesn't bounce back to /home
        context.add_init_script("""
            localStorage.setItem('goalstar_user', JSON.stringify({
                type: 'demo_guest',
                name: 'Guest Builder #454',
                address: '0x454abc',
                loginAt: Date.now()
            }));
        """)
        
        page = context.new_page()
        
        print("=== Test 1: Loading /home ===")
        page.goto('http://localhost:8000/home', wait_until='networkidle')
        time.sleep(1)
        
        # Screenshot Hero initial state
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_hero_initial.png'))
        print("Saved artifact_v2_hero_initial.png")
        
        # Test Dark Mode toggle with #themeSwitch
        page.click('#themeSwitch')
        time.sleep(0.5)
        paper_mode = page.evaluate("() => document.body.dataset.paper")
        is_dark_class = page.evaluate("() => document.documentElement.classList.contains('dark-mode')")
        print(f"Dark mode state: paper={paper_mode}, dark_class={is_dark_class}")
        assert paper_mode == 'night' and is_dark_class, f"Dark mode toggle failed! paper={paper_mode}"
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_hero_dark.png'))
        print("Saved artifact_v2_hero_dark.png")
        
        # Toggle back to light
        page.click('#themeSwitch')
        time.sleep(0.5)
        paper_mode_after = page.evaluate("() => document.body.dataset.paper")
        assert paper_mode_after == 'lined', f"Light mode toggle back failed: paper={paper_mode_after}"
        
        # Test Sound toggle with #soundSwitch
        page.click('#soundSwitch')
        time.sleep(0.3)
        sound_status = page.evaluate("() => window.sound ? window.sound.enabled : null")
        print(f"Sound status after click: {sound_status}")
        page.click('#soundSwitch')
        time.sleep(0.3)
        
        print("=== Test 2: Scroll to Simulator & Test Interaction ===")
        page.evaluate("() => { const el = document.getElementById('simulator'); el ? el.scrollIntoView({behavior: 'smooth'}) : window.scrollTo(0, 700); }")
        time.sleep(1.2)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_simulator.png'))
        print("Saved artifact_v2_simulator.png")
        
        print("=== Test 3: Scroll to Use Cases & Verify Arrow Precision & Solid Cards ===")
        # Scroll to Card 1
        page.evaluate("() => { const el = document.getElementById('card1'); el.scrollIntoView({behavior: 'smooth'}); }")
        time.sleep(1.5)
        
        # Check Card 1 solid opacity
        c1_opacity = page.evaluate("() => window.getComputedStyle(document.getElementById('card1')).opacity")
        print(f"Card 1 opacity: {c1_opacity}")
        assert float(c1_opacity) >= 0.95, f"Card 1 opacity too low: {c1_opacity}"
        
        # Scroll to Card 5 launch button
        page.evaluate("() => { const el = document.getElementById('card5LaunchBtn'); el.scrollIntoView({behavior: 'smooth', block: 'center'}); }")
        time.sleep(2)
        
        # Check Card 5 solid opacity
        c5_opacity = page.evaluate("() => window.getComputedStyle(document.getElementById('card5')).opacity")
        print(f"Card 5 opacity: {c5_opacity}")
        assert float(c5_opacity) >= 0.95, f"Card 5 opacity too low: {c5_opacity}"
        
        # Verify Arrow & Path End Point
        arrow_data = page.evaluate("""() => {
            const arrow = document.getElementById('travelingArrow');
            const targetRing = document.getElementById('card5TargetRing');
            const launchBtn = document.getElementById('card5LaunchBtn');
            const activePath = document.getElementById('journeyActivePath');
            const track = document.getElementById('journeyTrack');
            
            const arrowRect = arrow.getBoundingClientRect();
            const ringRect = targetRing.getBoundingClientRect();
            const btnRect = launchBtn.getBoundingClientRect();
            const trackRect = track.getBoundingClientRect();
            
            const totalLen = activePath.getTotalLength();
            const endPoint = activePath.getPointAtLength(totalLen);
            
            return {
                arrowX: arrowRect.left + arrowRect.width / 2,
                arrowY: arrowRect.top + arrowRect.height / 2,
                ringX: ringRect.left + ringRect.width / 2,
                ringY: ringRect.top + ringRect.height / 2,
                btnX: btnRect.left + btnRect.width / 2,
                btnY: btnRect.top + btnRect.height / 2,
                trackTop: trackRect.top,
                trackLeft: trackRect.left,
                pathEndX: trackRect.left + endPoint.x,
                pathEndY: trackRect.top + endPoint.y
            };
        }""")
        print(f"Arrow coords: X={arrow_data['arrowX']:.1f}, Y={arrow_data['arrowY']:.1f}")
        print(f"Path end coords: X={arrow_data['pathEndX']:.1f}, Y={arrow_data['pathEndY']:.1f}")
        print(f"Ring target coords: X={arrow_data['ringX']:.1f}, Y={arrow_data['ringY']:.1f}")
        print(f"Card 5 button coords: X={arrow_data['btnX']:.1f}, Y={arrow_data['btnY']:.1f}")
        
        # Distance between arrow and path end
        dx = abs(arrow_data['arrowX'] - arrow_data['pathEndX'])
        dy = abs(arrow_data['arrowY'] - arrow_data['pathEndY'])
        print(f"Arrow to path end delta: dx={dx:.1f}px, dy={dy:.1f}px")
        assert dx <= 5 and dy <= 5, f"Arrow disconnected from path end! dx={dx}, dy={dy}"
        
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_usecases_card5_end.png'))
        print("Saved artifact_v2_usecases_card5_end.png")
        
        print("=== Test 4: Progressive Simulation Walkthrough Modal ===")
        # Scroll back to Card 1
        page.evaluate("() => { const el = document.getElementById('card1'); el.scrollIntoView({behavior: 'smooth'}); }")
        time.sleep(1)
        
        # Click "Simulate Route" on Card 1
        page.click("#card1 .scenario-launch-btn")
        time.sleep(0.5)
        
        # Modal should be open
        is_modal_open = page.is_visible('#scenarioModal')
        print(f"Scenario Walkthrough Modal open: {is_modal_open}")
        assert is_modal_open, "Modal did not open!"
        
        # Stage 1 Screenshot
        stage_num = page.inner_text('#scenarioStepNum')
        print(f"Current stage: {stage_num}")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_modal_stage1.png'))
        print("Saved artifact_v2_modal_stage1.png")
        
        # Advance to Stage 2
        page.click('#nextScenarioStepBtn')
        time.sleep(0.5)
        stage_num = page.inner_text('#scenarioStepNum')
        print(f"Current stage: {stage_num}")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_modal_stage2_hurdle.png'))
        print("Saved artifact_v2_modal_stage2_hurdle.png")
        
        # Advance to Stage 3
        page.click('#nextScenarioStepBtn')
        time.sleep(0.5)
        stage_num = page.inner_text('#scenarioStepNum')
        print(f"Current stage: {stage_num}")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_modal_stage3_reroute.png'))
        print("Saved artifact_v2_modal_stage3_reroute.png")
        
        # Advance to Stage 4 (Path Profile Breakdown)
        page.click('#nextScenarioStepBtn')
        time.sleep(0.5)
        stage_num = page.inner_text('#scenarioStepNum')
        print(f"Current stage: {stage_num}")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_modal_stage4_profile.png'))
        print("Saved artifact_v2_modal_stage4_profile.png")
        
        # Advance to Stage 5 (Sui Proof)
        page.click('#nextScenarioStepBtn')
        time.sleep(0.5)
        stage_num = page.inner_text('#scenarioStepNum')
        print(f"Current stage: {stage_num}")
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_modal_stage5_sui_proof.png'))
        print("Saved artifact_v2_modal_stage5_sui_proof.png")
        
        # Click "Open in Full Planner" and wait for navigation
        with page.expect_navigation(timeout=10000):
            page.click('#openFullPlannerBtn')
            
        print(f"Navigated to URL: {page.url}")
        assert page.url in ['http://localhost:8000/', 'http://localhost:8000/index.html'], f"Failed to navigate to planner: {page.url}"
        
        # Wait for Planner elements
        page.wait_for_selector('#canvas', timeout=5000)
        page.wait_for_selector('#side', timeout=5000)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_planner_loaded.png'))
        print("Saved artifact_v2_planner_loaded.png")
        
        print("=== Test 5: Verify Planner Design & Hierarchy (Image 1 Style) ===")
        # Check settings
        page.click('#settingsBtn')
        time.sleep(0.5)
        page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_planner_settings.png'))
        print("Saved artifact_v2_planner_settings.png")
        page.click('#settingsDlg .actions button[value="cancel"]')
        time.sleep(0.5)
        
        print("=== Test 6: Mobile 375px Responsiveness ===")
        mobile_page = context.new_page()
        mobile_page.set_viewport_size({'width': 375, 'height': 667})
        mobile_page.goto('http://localhost:8000/home', wait_until='networkidle')
        time.sleep(1)
        
        mobile_scroll_w = mobile_page.evaluate("document.documentElement.scrollWidth")
        mobile_client_w = mobile_page.evaluate("document.documentElement.clientWidth")
        print(f"Mobile widths: scrollWidth={mobile_scroll_w}, clientWidth={mobile_client_w}")
        assert mobile_scroll_w <= mobile_client_w, f"Horizontal overflow! {mobile_scroll_w} > {mobile_client_w}"
        
        mobile_page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_mobile_hero.png'))
        print("Saved artifact_v2_mobile_hero.png")
        
        # Scroll to Use Cases on Mobile
        mobile_page.evaluate("() => { const el = document.getElementById('card1'); el.scrollIntoView(); }")
        time.sleep(1)
        mobile_page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_mobile_usecases.png'))
        print("Saved artifact_v2_mobile_usecases.png")
        
        # Open Modal on Mobile
        mobile_page.click("#card1 .scenario-launch-btn")
        time.sleep(0.5)
        mobile_page.screenshot(path=os.path.join(ARTIFACT_DIR, 'artifact_v2_mobile_modal.png'))
        print("Saved artifact_v2_mobile_modal.png")
        
        browser.close()
        print("\nALL VERIFICATIONS PASSED WITH ZERO ERRORS!")

if __name__ == '__main__':
    run_tests()
