import asyncio
import subprocess
import time
import os
from playwright.async_api import async_playwright

async def verify_dashboard():
    print("Starting verification servers...")

    # Start Backend
    backend_proc = subprocess.Popen(
        ["python3", "-m", "backend.main"],
        env={**os.environ, "PYTHONPATH": os.getcwd()}
    )

    # Start Frontend
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "8080"]
    )

    try:
        print("Waiting for servers to start...")
        time.sleep(10) # Give them some time

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_timeout(5000) # Wait for animations/data

            # Check for key elements
            print("Checking dashboard elements...")
            # Using text content to verify elements
            content = await page.content()

            has_vital_signs = "Vital Signs" in content
            has_revenue_engine = "Revenue Engine" in content
            has_sense_engine = "Sense Engine" in content

            print(f"Vital Signs found: {has_vital_signs}")
            print(f"Revenue Engine found: {has_revenue_engine}")
            print(f"Sense Engine found: {has_sense_engine}")

            # Capture screenshot
            screenshot_path = "dashboard_verification.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            if has_vital_signs and has_revenue_engine:
                print("E2E Verification SUCCESSFUL")
            else:
                print("E2E Verification FAILED - Missing elements")

            await browser.close()

    finally:
        print("Stopping servers...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    asyncio.run(verify_dashboard())
