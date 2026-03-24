import asyncio
import subprocess
import time
import os
import signal
from playwright.async_api import async_playwright

async def run_verification():
    print("Starting backend server...")
    backend_proc = subprocess.Popen(["python3", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("Starting frontend server...")
    frontend_proc = subprocess.Popen(["npm", "run", "dev", "--", "--port", "8080", "--host", "0.0.0.0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for servers to start
    print("Waiting 20s for servers to initialize...")
    time.sleep(20)

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            print("Navigating to dashboard...")
            # Try both localhost and 127.0.0.1
            await page.goto("http://127.0.0.1:8080", timeout=60000)

            # Wait for meaningful content
            await page.wait_for_selector("h2:has-text('Gen-4 Autonomous Organism')", timeout=30000)

            # Check metrics
            print("Verifying metrics display...")
            await page.wait_for_selector("text=Problems Scanned")

            # Check agents
            print("Verifying agents section...")
            await page.wait_for_selector("text=Autonomous Agents")

            # Take a screenshot
            os.makedirs("/home/jules/verification", exist_ok=True)
            screenshot_path = "/home/jules/verification/dashboard_verification.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            print("E2E Verification SUCCESSFUL.")
        except Exception as e:
            print(f"E2E Verification FAILED: {e}")
        finally:
            # Kill subprocesses correctly
            os.kill(backend_proc.pid, signal.SIGTERM)
            os.kill(frontend_proc.pid, signal.SIGTERM)
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_verification())
