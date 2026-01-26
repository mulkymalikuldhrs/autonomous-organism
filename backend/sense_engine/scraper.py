from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def scrape_reddit(subreddit: str):
    url = f"https://www.reddit.com/r/{subreddit}/new/"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')

        # Scroll down to load more content
        for _ in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, 'html.parser')
    posts = []
    for post in soup.find_all("div", {"data-testid": "post-container"}):
        title_element = post.find("h3")
        title = title_element.text.strip() if title_element else "No Title"

        # This is a simplified selector, might need adjustment based on Reddit's current structure
        p_elements = post.find_all("p")
        post_text = "\n".join([p.text for p in p_elements])

        posts.append({"title": title, "text": post_text})

    return posts
