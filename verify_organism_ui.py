from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    page.goto("http://localhost:8080")
    page.wait_for_timeout(2000)

    # Check for "SYSTEM ONLINE" or similar indicators of the new Gen-4.1
    # Note: Header.tsx might still say "online" but state generation should be 4.1

    # Click "Run Sense" to see activity in logs
    page.get_by_role("button", name="Run Sense").click()
    page.wait_for_timeout(3000)

    # Take screenshot of the dashboard
    page.screenshot(path="verification/screenshots/dashboard_gen4_1.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
