
import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # Wait for frontend to be ready on port 8080 (assuming it will be started)
            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_timeout(5000)

            # Capture screenshot
            screenshot_path = "dashboard_verification.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            # Basic checks
            title = await page.title()
            print(f"Page title: {title}")

        except Exception as e:
            print(f"Verification error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
