import httpx
from bs4 import BeautifulSoup
import re

def scrape_reddit_sideprojectideas():
    """
    Scrapes the r/SideProjectIdeas subreddit for new posts.
    """
    url = "https://old.reddit.com/r/SideProjectIdeas/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.find_all("div", class_="thing")

            results = []
            for post in posts:
                title_tag = post.find("a", class_="title")
                if title_tag:
                    title = title_tag.get_text()
                    # Basic cleaning
                    title = re.sub(r'\s+', ' ', title).strip()
                    results.append(title)

            return results

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        raise e

if __name__ == "__main__":
    ideas = scrape_reddit_sideprojectideas()
    if ideas:
        print(f"Found {len(ideas)} ideas:")
        for i, idea in enumerate(ideas, 1):
            print(f"{i}. {idea}")
    else:
        print("No ideas found or an error occurred.")
