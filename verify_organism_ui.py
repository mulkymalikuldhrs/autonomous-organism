import asyncio
import subprocess
import time
import os
import signal
from playwright.async_api import async_playwright

async def run_verification():
    print("Starting backend...")
    backend_proc = subprocess.Popen(
        ["python3", "-m", "backend.main"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    print("Starting frontend...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    time.sleep(10) # Wait for servers to start

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = await context.new_page()

        try:
            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080")
            await page.wait_for_timeout(5000)

            # Interact with the dashboard to trigger some real data if needed
            # Run Spawner to see agents
            print("Triggering Spawner...")
            await page.get_by_role("button", name="Run Spawner").click()
            await page.wait_for_timeout(2000)

            # Run Sense
            print("Triggering Sense...")
            await page.get_by_role("button", name="Sense", exact=True).click()
            await page.wait_for_timeout(2000)

            # Take screenshot
            print("Taking screenshot...")
            await page.screenshot(path="/home/jules/verification/screenshots/dashboard_verification.png", full_page=True)

            print("Verification steps complete.")

        except Exception as e:
            print(f"Verification error: {e}")
        finally:
            await context.close()
            await browser.close()

            # Cleanup processes
            os.killpg(os.getpgid(backend_proc.pid), signal.SIGTERM)
            os.killpg(os.getpgid(frontend_proc.pid), signal.SIGTERM)

if __name__ == "__main__":
    asyncio.run(run_verification())
