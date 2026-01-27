import httpx
from bs4 import BeautifulSoup

def scrape_text(url: str) -> str:
    """
    Scrapes the text content from a given URL.
    """
    try:
        response = httpx.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()
    except httpx.RequestError as exc:
        return f"An error occurred while requesting {exc.request.url!r}."
    except httpx.HTTPStatusError as exc:
        return f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."

if __name__ == "__main__":
    # Example usage
    text = scrape_text("https://example.com")
    print(text)
