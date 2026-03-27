import asyncio
import subprocess
import os
import time
import signal
from playwright.async_api import async_playwright

async def verify_dashboard():
    print("🚀 Starting E2E verification of Organisme SaaS Otonom Dashboard...")

    # 1. Start Backend on port 8000
    backend_proc = subprocess.Popen(
        ["python3", "-m", "backend.main"],
        env={**os.environ, "PYTHONPATH": os.getcwd()},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("   ✅ Backend process started (Port 8000)")

    # 2. Start Frontend on port 8080
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("   ✅ Frontend process started (Port 8080)")

    # Wait for services to be ready
    print("   ⏳ Waiting for services to initialize (15s)...")
    await asyncio.sleep(15)

    verification_dir = "/home/jules/verification"
    os.makedirs(verification_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigate to Dashboard
            print("   🌐 Navigating to http://localhost:8080/")
            await page.goto("http://localhost:8080/", timeout=60000)
            await page.wait_for_load_state("networkidle")

            # Take screenshot
            screenshot_path = f"{verification_dir}/dashboard_verification.png"
            await page.screenshot(path=screenshot_path)
            print(f"   📸 Dashboard screenshot captured: {screenshot_path}")

            # Verify core elements
            header_text = await page.inner_text("header")
            if "ORGANISM-ALPHA" in header_text:
                print("   ✅ Header 'ORGANISM-ALPHA' verified.")
            else:
                print("   ❌ Header 'ORGANISM-ALPHA' not found.")

            # Check for Metrics
            metrics_section = await page.query_selector("main")
            metrics_text = await metrics_section.inner_text()
            if "Vital Signs" in metrics_text and "Revenue Engine" in metrics_text:
                 print("   ✅ Vital Signs and Revenue Engine sections verified.")
            else:
                 print("   ❌ Key metrics sections missing.")

            # Check for Agents
            agents_text = await page.inner_text("h3:has-text('Autonomous Agents') + div")
            if "No active agents" in agents_text or "Agent" in agents_text:
                 print("   ✅ Autonomous Agents status verified.")

            print("   ✨ E2E Verification SUCCESSFUL.")

        except Exception as e:
            print(f"   ❌ Verification FAILED: {e}")
        finally:
            await browser.close()

    # 3. Cleanup
    print("   🧹 Cleaning up subprocesses...")
    backend_proc.terminate()
    frontend_proc.terminate()

    # Ensure they are killed
    try:
        os.kill(backend_proc.pid, signal.SIGKILL)
        os.kill(frontend_proc.pid, signal.SIGKILL)
    except:
        pass

if __name__ == "__main__":
    asyncio.run(verify_dashboard())
