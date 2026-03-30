import asyncio
import subprocess
import time
import os
from playwright.async_api import async_playwright

async def verify_organism_ui():
    # 1. Start Backend
    print("Starting backend...")
    backend_proc = subprocess.Popen(
        ["uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 2. Start Frontend
    print("Starting frontend...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for servers to be ready
    time.sleep(10)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                record_video_dir="/home/jules/verification/videos"
            )
            page = await context.new_page()

            # Navigate to the dashboard
            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080", timeout=60000)

            # Wait for content to load
            await page.wait_for_selector("text=Vital Signs", timeout=30000)

            # Take screenshot of the dashboard
            print("Capturing dashboard screenshot...")
            await page.screenshot(path="/home/jules/verification/screenshots/dashboard_verification.png", full_page=True)

            # Verify Agents section
            print("Verifying Agents section...")
            await page.wait_for_selector("text=Agents Status", timeout=10000)

            # Verify Revenue section
            print("Verifying Revenue section...")
            await page.wait_for_selector("text=Revenue Engine", timeout=10000)

            # Trigger Spawner manually to see it work
            print("Triggering Spawner...")
            await page.click("text=Spawner")
            await asyncio.sleep(2) # Wait for toast/update

            await page.screenshot(path="/home/jules/verification/screenshots/dashboard_after_spawner.png", full_page=True)

            print("Verification successful!")

            await context.close()
            await browser.close()

    except Exception as e:
        print(f"Verification FAILED: {e}")
    finally:
        # Kill processes
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    asyncio.run(verify_organism_ui())
