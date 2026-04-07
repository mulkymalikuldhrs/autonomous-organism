import asyncio
import subprocess
import os
import time
from playwright.async_api import async_playwright

async def run_verification():
    print("Starting Organism Verification Script...")

    # 1. Setup Directories
    v_dir = os.path.join(os.getcwd(), "verification")
    os.makedirs(os.path.join(v_dir, "videos"), exist_ok=True)
    os.makedirs(os.path.join(v_dir, "screenshots"), exist_ok=True)

    # 2. Start Backend
    print("Launching Backend...")
    backend_proc = subprocess.Popen(
        ["python3", "-m", "backend.main"],
        env={**os.environ, "PYTHONPATH": os.getcwd()},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 3. Start Frontend
    print("Launching Frontend...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for servers to start
    time.sleep(20)

    # 4. Playwright E2E
    async with async_playwright() as p:
        print("Launching Browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir=os.path.join(v_dir, "videos"),
            viewport={'width': 1280, 'height': 720}
        )
        page = await context.new_page()

        try:
            print("Navigating to Dashboard...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_timeout(5000) # Wait for animations

            # Screenshot 1: Vital Signs
            print("Capturing Vital Signs...")
            await page.screenshot(path=os.path.join(v_dir, "screenshots", "vital_signs.png"))

            # Try to trigger a Sense cycle via UI
            print("Triggering Sense Cycle via UI...")
            sense_button = page.get_by_role("button", name="Sense", exact=True)
            if await sense_button.is_visible():
                await sense_button.click()
                await page.wait_for_timeout(3000)
                await page.screenshot(path=os.path.join(v_dir, "screenshots", "after_sense.png"))

            # Check for revenue section
            print("Checking Revenue Engine...")
            revenue_text = page.get_by_text("Revenue Engine")
            if await revenue_text.is_visible():
                print("Revenue Engine section found.")

            # Final Dashboard state
            await page.screenshot(path=os.path.join(v_dir, "screenshots", "final_dashboard.png"), full_page=True)
            print("Verification artifacts captured.")

        except Exception as e:
            print(f"Playwright error: {e}")
            await page.screenshot(path=os.path.join(v_dir, "screenshots", "error.png"))
        finally:
            await browser.close()

    # Cleanup
    print("Shutting down servers...")
    backend_proc.terminate()
    frontend_proc.terminate()
    print("Verification complete.")

if __name__ == "__main__":
    asyncio.run(run_verification())
