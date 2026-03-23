
import asyncio
import subprocess
import time
import os
from playwright.async_api import async_playwright

async def verify_organism():
    # Setup directories
    verification_dir = os.path.join(os.getcwd(), "verification")
    video_dir = os.path.join(verification_dir, "video")
    os.makedirs(video_dir, exist_ok=True)

    print("🚀 Starting Backend and Frontend...")
    # Start Backend
    backend_proc = subprocess.Popen(["python3", "-m", "backend.main"])
    # Start Frontend
    frontend_proc = subprocess.Popen(["npm", "run", "dev", "--", "--port", "8080"])

    # Wait for servers to start
    print("⏳ Waiting for servers to initialize (20s)...")
    time.sleep(20)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Record video
        context = await browser.new_context(record_video_dir=video_dir)
        page = await context.new_page()
        try:
            # Navigate to the local dashboard
            print("🔗 Navigating to http://localhost:8080...")
            await page.goto("http://localhost:8080", timeout=60000)
            await page.wait_for_timeout(2000)

            # Interact with the dashboard - trigger Sense
            print("👁️ Triggering Sense Engine...")
            await page.get_by_role("button", name="Sense").click()
            await page.wait_for_timeout(3000)

            # Trigger Decision
            print("🧠 Triggering Decision Core...")
            await page.get_by_role("button", name="Decision").click()
            await page.wait_for_timeout(3000)

            # Capture final screenshot
            screenshot_path = os.path.join(verification_dir, "dashboard_verification.png")
            await page.screenshot(path=screenshot_path)
            print(f"✅ Dashboard screenshot saved to {screenshot_path}")

            content = await page.content()
            if "Autonomous Life System" in content:
                print("✨ Verification SUCCESS: 'Autonomous Life System' detected.")
            else:
                print("❌ Verification FAILED: Dashboard text not found.")

        except Exception as e:
            print(f"❌ Verification ERROR: {e}")
        finally:
            await context.close()
            await browser.close()
            print("🛑 Shutting down servers...")
            backend_proc.terminate()
            frontend_proc.terminate()
            backend_proc.wait()
            frontend_proc.wait()

if __name__ == "__main__":
    asyncio.run(verify_organism())
