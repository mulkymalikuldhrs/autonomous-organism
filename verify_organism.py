import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
import time

async def verify_organism():
    print("Starting backend and frontend for verification...")
    # Start backend
    backend_proc = subprocess.Popen(["python3", "-m", "backend.main"], env=os.environ)
    # Start frontend
    frontend_proc = subprocess.Popen(["npm", "run", "dev"], env=os.environ)

    time.sleep(10) # Wait for servers to start

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_timeout(5000) # Wait for data to load

            # Click some buttons to see if they work (background tasks)
            print("Testing 'Spawn' button...")
            spawn_btn = page.locator("button:has-text('Spawn')")
            if await spawn_btn.is_visible():
                await spawn_btn.click()
                await page.wait_for_timeout(2000)

            print("Capturing screenshot...")
            await page.screenshot(path="dashboard_verification.png", full_page=True)
            print("Screenshot saved to dashboard_verification.png")
        except Exception as e:
            print(f"Verification error: {e}")
        finally:
            await browser.close()
            backend_proc.terminate()
            frontend_proc.terminate()

if __name__ == "__main__":
    asyncio.run(verify_organism())
