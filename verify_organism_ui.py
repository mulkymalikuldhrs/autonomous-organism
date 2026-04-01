import subprocess
import time
import os
from playwright.sync_api import sync_playwright

def run_verification():
    print("Starting backend...")
    backend_proc = subprocess.Popen(["python3", "-m", "backend.main"], env=os.environ)

    print("Starting frontend...")
    frontend_proc = subprocess.Popen(["npm", "run", "dev", "--", "--port", "8080"], env=os.environ)

    time.sleep(10) # Wait for servers to start

    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="/home/jules/verification/videos")
        page = context.new_page()

        try:
            print("Navigating to dashboard...")
            page.goto("http://localhost:8080", timeout=60000)
            page.wait_for_timeout(5000)

            # Click Sense
            print("Triggering Sense...")
            page.get_by_role("button", name="Sense").click()
            page.wait_for_timeout(2000)

            # Click Spawner
            print("Triggering Spawner...")
            page.get_by_role("button", name="Spawner").click()
            page.wait_for_timeout(2000)

            # Take screenshot
            print("Capturing screenshot...")
            page.screenshot(path="/home/jules/verification/screenshots/dashboard_verification.png", full_page=True)
            page.wait_for_timeout(2000)

        except Exception as e:
            print(f"Verification error: {e}")
        finally:
            context.close()
            browser.close()
            backend_proc.terminate()
            frontend_proc.terminate()

if __name__ == "__main__":
    run_verification()
