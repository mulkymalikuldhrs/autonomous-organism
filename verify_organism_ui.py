import asyncio
import os
import signal
import subprocess
import time
import httpx
from playwright.async_api import async_playwright

async def check_url(url: str, timeout: int = 30):
    start = time.time()
    async with httpx.AsyncClient() as client:
        while time.time() - start < timeout:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    return True
            except Exception:
                pass
            await asyncio.sleep(1)
    return False

async def verify_organism():
    print("Starting visual verification for ORGANISME SAAS OTONOM...")

    # Ensure dirs exist
    os.makedirs("/home/jules/verification/videos/", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots/", exist_ok=True)

    # 1. Start Backend on port 8000
    backend_proc = subprocess.Popen(
        ["uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=open("/home/jules/verification/backend.log", "w"),
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid
    )

    # 2. Start Frontend on port 8080
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "8080", "--host"],
        stdout=open("/home/jules/verification/frontend.log", "w"),
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid
    )

    # Wait for servers to start
    print("Waiting for servers to initialize (timeout 60s)...")
    backend_ready = await check_url("http://127.0.0.1:8000/api/metrics")
    frontend_ready = await check_url("http://127.0.0.1:8080")

    if not (backend_ready and frontend_ready):
        print(f"Server readiness failure: Backend={backend_ready}, Frontend={frontend_ready}")
        # Log content for debugging
        with open("/home/jules/verification/frontend.log", "r") as f:
            print(f"Frontend log tail:\n{f.read()[-500:]}")
    else:
        print("Servers ready. Launching Playwright...")

    # 3. Playwright screenshot
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Record video properly
        context = await browser.new_context(record_video_dir="/home/jules/verification/videos/")
        page = await context.new_page()

        try:
            print("Navigating to dashboard at http://localhost:8080...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_timeout(5000) # Wait for animation/data load

            screenshot_path = "/home/jules/verification/screenshots/dashboard_v4.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot captured: {screenshot_path}")

            # Interact with the UI - trigger a cycle
            print("Attempting to trigger a Decision cycle via UI...")
            # Dashboard is cyan/violet slate themed
            # We look for a button containing "Decision"
            button = page.get_by_text("Decision", exact=True)
            if await button.count() > 0:
                await button.first.click()
                await page.wait_for_timeout(3000)
                await page.screenshot(path="/home/jules/verification/screenshots/dashboard_after_click.png")
                print("Dashboard updated screenshot captured.")
            else:
                print("Decision button not found. Checking for alternative controls.")
                await page.screenshot(path="/home/jules/verification/screenshots/dashboard_not_found.png")

        except Exception as e:
            print(f"Playwright error: {e}")
        finally:
            await browser.close()

    # Cleanup
    os.killpg(os.getpgid(backend_proc.pid), signal.SIGTERM)
    os.killpg(os.getpgid(frontend_proc.pid), signal.SIGTERM)
    print("Verification complete. Servers stopped.")

if __name__ == "__main__":
    asyncio.run(verify_organism())
