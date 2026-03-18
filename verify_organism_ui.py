import asyncio
from playwright.async_api import async_playwright
import subprocess
import time
import os
import signal

async def verify_organism():
    # 1. Start backend
    print("Starting backend...")
    backend_proc = subprocess.Popen(["python3", "-m", "backend.main"], env=os.environ)
    time.sleep(5) # Wait for backend to start

    # 2. Start frontend (Vite)
    print("Starting frontend...")
    frontend_proc = subprocess.Popen(["npm", "run", "dev", "--", "--port", "8080"], env=os.environ)
    time.sleep(10) # Wait for frontend to start

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_timeout(5000)

            # Take screenshot
            await page.screenshot(path="dashboard_verification.png")
            print("Screenshot saved to dashboard_verification.png")

            # Check for key metrics
            content = await page.content()
            if "Problems Scanned" in content:
                print("SUCCESS: Found 'Problems Scanned' on dashboard.")
            else:
                print("FAILURE: 'Problems Scanned' not found on dashboard.")

            if "IDEAS GENERATED" in content or "Ideas Generated" in content:
                 print("SUCCESS: Found 'Ideas Generated' on dashboard.")

        except Exception as e:
            print(f"Verification error: {e}")
        finally:
            await browser.close()

    # Cleanup
    print("Cleaning up...")
    os.kill(backend_proc.pid, signal.SIGTERM)
    os.kill(frontend_proc.pid, signal.SIGTERM)

if __name__ == "__main__":
    asyncio.run(verify_organism())
