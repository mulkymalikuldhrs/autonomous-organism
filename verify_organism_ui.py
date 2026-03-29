import asyncio
import os
import subprocess
import time
from playwright.async_api import async_playwright

async def verify_ui():
    print("Starting backend and frontend for verification...")
    # Start backend
    backend_proc = subprocess.Popen(["python3", "-m", "backend.main"], env={**os.environ, "PYTHONPATH": "."})
    # Start frontend
    frontend_proc = subprocess.Popen(["npm", "run", "dev"])

    # Wait for servers to be up
    time.sleep(10)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(record_video_dir="verification/")
            page = await context.new_page()

            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080")

            # Wait for metrics to load
            await page.wait_for_selector("text=Problems Scanned")

            # Take screenshot
            await page.screenshot(path="verification/dashboard_verification.png")
            print("Screenshot saved to verification/dashboard_verification.png")

            # Check if metrics are being pulled from backend
            # Based on test_organism.py, we should have at least 1 idea and 1 product
            problems_text = await page.locator("text=Problems Scanned").inner_text()
            ideas_text = await page.locator("text=Ideas Generated").inner_text()
            products_text = await page.locator("text=Products Built").inner_text()

            print(f"Metrics found: {problems_text}, {ideas_text}, {products_text}")

            await browser.close()
    finally:
        print("Cleaning up processes...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    if not os.path.exists("verification"):
        os.makedirs("verification")
    asyncio.run(verify_ui())
