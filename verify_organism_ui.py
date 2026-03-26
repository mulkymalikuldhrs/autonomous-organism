import asyncio
import os
import subprocess
import time
from playwright.async_api import async_playwright

async def verify_ui():
    print("Starting backend and frontend for verification...")
    # Start Backend
    backend_proc = subprocess.Popen(
        ["python3", "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Start Frontend
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "8080"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Wait for servers to start
    time.sleep(10)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            print("Navigating to dashboard...")
            await page.goto("http://127.0.0.1:8080", timeout=60000)
            await page.wait_for_timeout(5000)

            # Take screenshot
            os.makedirs("verification", exist_ok=True)
            screenshot_path = "verification/dashboard_verification.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            # Check for key elements
            title = await page.title()
            print(f"Page title: {title}")

            content = await page.content()
            if "Vital Signs" in content:
                print("SUCCESS: Dashboard loaded and 'Vital Signs' section found.")
            else:
                print("FAILURE: Dashboard content missing expected markers.")

            await browser.close()
    finally:
        print("Cleaning up processes...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    asyncio.run(verify_ui())
