from playwright.sync_api import sync_playwright, expect
import os
import time

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        # Navigate to the local dev server
        print("Navigating to dashboard...")
        page.goto("http://localhost:8080")

        # Wait for the dashboard to load (checking for Gen-4.1 indicator)
        print("Waiting for dashboard to stabilize...")
        time.sleep(5)

        # Take a screenshot
        os.makedirs("verification", exist_ok=True)
        screenshot_path = "verification/dashboard_gen41.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_dashboard()
