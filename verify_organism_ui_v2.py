import asyncio
import subprocess
import time
import os
import signal
from playwright.async_api import async_playwright

async def verify_ui():
    print("Starting backend and frontend for verification...")

    # Start Backend
    backend_process = subprocess.Popen(
        ["python3", "backend/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Start Frontend
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for both to start
    print("Waiting for servers to initialize (10s)...")
    await asyncio.sleep(10)

    os.makedirs("/home/jules/verification/video", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(record_video_dir="/home/jules/verification/video")
        page = await context.new_page()

        try:
            print("Navigating to http://localhost:8080...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_timeout(1000)

            # Wait for content to load (check for vital signs card)
            await page.wait_for_selector("text=Vital Signs", timeout=30000)
            print("Dashboard loaded successfully.")

            # Interact with the UI (Sense button)
            await page.click("button:has-text('Sense')")
            print("Clicked Sense button.")
            await page.wait_for_timeout(2000)

            # Take a screenshot
            screenshot_path = "/home/jules/verification/verification.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Verification failed: {e}")
        finally:
            await context.close()
            await browser.close()

    # Cleanup processes
    print("Terminating servers...")
    os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
    os.killpg(os.getpgid(frontend_process.pid), signal.SIGTERM)

if __name__ == "__main__":
    asyncio.run(verify_ui())
