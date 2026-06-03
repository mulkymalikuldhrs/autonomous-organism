import time
import requests
from bs4 import BeautifulSoup
from ..database import SessionLocal, ProblemRaw, LifeLog
import newspaper

SOURCES = [
    {"name": "HackerNews", "url": "https://news.ycombinator.com", "selector": ".titleline > a"},
    {"name": "IndieHackers", "url": "https://www.indiehackers.com/groups/ideas-and-validation", "selector": ".feed-item__title-link"},
]

def run_sense():
    db = SessionLocal()
    try:
        db.add(LifeLog(engine="sense", type="info", message="Starting real sense cycle"))
        db.commit()

        for source in SOURCES:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                resp = requests.get(source["url"], headers=headers, timeout=15)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, 'html.parser')
                links = soup.select(source["selector"])

                for link in links[:5]:
                    href = link.get('href')
                    if not href: continue
                    if not href.startswith('http'):
                        if source["name"] == "HackerNews":
                            href = "https://news.ycombinator.com/" + href
                        else:
                            href = source["url"].split('.com')[0] + '.com' + href

                    title = link.get_text().strip()

                    # Avoid duplicates
                    if db.query(ProblemRaw).filter(ProblemRaw.url == href).first():
                        continue

                    # Extract content using newspaper
                    try:
                        article = newspaper.Article(href)
                        article.download()
                        article.parse()
                        content = article.text
                    except:
                        content = title

                    db.add(ProblemRaw(
                        source=source["name"],
                        external_id=f"{source['name']}_{hash(href)}",
                        title=title,
                        content=content,
                        url=href
                    ))
            except Exception as e:
                db.add(LifeLog(engine="sense", type="error", message=f"Failed to scrape {source['name']}: {str(e)}"))

        db.commit()
    finally:
        db.close()
