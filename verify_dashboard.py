import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        try:
            print("Navigating to dashboard...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_load_state("networkidle")

            # Check for core elements
            await page.wait_for_selector("text=ORGANISM-ALPHA")
            print("Dashboard loaded successfully.")

            # Take a screenshot
            await page.screenshot(path="dashboard_verification.png", full_page=True)
            print("Screenshot saved as dashboard_verification.png")

        except Exception as e:
            print(f"Verification failed: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
