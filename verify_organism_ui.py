import asyncio
import subprocess
import time
import os
from playwright.async_api import async_playwright

async def verify_dashboard():
    # 1. Start Backend
    print("Starting backend...")
    backend_proc = subprocess.Popen(
        ["python3", "-m", "backend.main"],
        env={**os.environ, "PYTHONPATH": "."}
    )

    # 2. Start Frontend
    print("Starting frontend...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        env={**os.environ}
    )

    # Wait for servers to start
    time.sleep(10)

    try:
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_timeout(5000)

            print("Capturing screenshot...")
            os.makedirs("verification", exist_ok=True)
            screenshot_path = "verification/dashboard_verification.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            await browser.close()
    except Exception as e:
        print(f"Verification error: {e}")
    finally:
        print("Cleaning up processes...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    asyncio.run(verify_dashboard())
