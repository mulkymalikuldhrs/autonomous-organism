import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # Start frontend
            print("Starting frontend...")
            proc = await asyncio.create_subprocess_shell(
                "npm run dev -- --port 8080",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Wait for frontend to be ready
            await asyncio.sleep(10)

            print("Navigating to dashboard...")
            await page.goto("http://127.0.0.1:8080", timeout=60000)
            await page.wait_for_timeout(5000)

            screenshot_path = "dashboard_verification.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            # Verify metrics are visible (not just 0 if possible, but at least checking they exist)
            metrics = await page.query_selector_all(".metric-value")
            print(f"Found {len(metrics)} metrics on page.")

        except Exception as e:
            print(f"Verification error: {e}")
        finally:
            await browser.close()
            # Clean up processes
            os.system("pkill -f 'npm run dev'")
            os.system("lsof -t -i :8080 | xargs kill -9 2>/dev/null || true")

if __name__ == "__main__":
    asyncio.run(verify())
