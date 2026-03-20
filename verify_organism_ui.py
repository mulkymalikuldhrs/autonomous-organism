import asyncio
import subprocess
import time
import os
from playwright.async_api import async_playwright

async def verify_ui():
    print("Starting backend and frontend servers for verification...")
    # Start Backend
    backend_proc = subprocess.Popen(["python3", "-m", "backend.main"], env=os.environ)
    # Start Frontend
    frontend_proc = subprocess.Popen(["npm", "run", "dev"], env=os.environ)

    time.sleep(10) # Give them time to start

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_selector("text=Autonomous Life System", timeout=30000)

            # Take a screenshot
            os.makedirs("verification", exist_ok=True)
            screenshot_path = "verification/dashboard_verification.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            # Verify metrics are visible (even if 0)
            await page.wait_for_selector("text=Problems Scanned", timeout=10000)
            await page.wait_for_selector("text=Total Revenue", timeout=10000)

            print("UI Verification SUCCESSFUL")

        except Exception as e:
            print(f"UI Verification FAILED: {e}")
            # Try to capture whatever is on the screen
            try:
                await page.screenshot(path="verification/failed_dashboard.png")
            except:
                pass
        finally:
            await browser.close()
            backend_proc.terminate()
            frontend_proc.terminate()

if __name__ == "__main__":
    asyncio.run(verify_ui())
