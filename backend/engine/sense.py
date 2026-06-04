import time
import requests
from bs4 import BeautifulSoup
from ..database import SessionLocal, ProblemRaw, LifeLog
import newspaper

SOURCES = [
    {"name": "HackerNews", "url": "https://news.ycombinator.com", "selector": ".titleline > a"},
    {"name": "IndieHackers", "url": "https://www.indiehackers.com/groups/ideas-and-validation", "selector": ".feed-item__title-link"},
    {"name": "Kaskus", "url": "https://www.kaskus.co.id/forum/21/berita-dan-politik", "selector": "a.thread-title"},
    {"name": "DiskusiWeb", "url": "https://diskusiweb.com/discussions", "selector": ".DiscussionListItem-title"},
    {"name": "SubstackTech", "url": "https://substack.com/discover/category/technology", "selector": "a.post-preview-title"}
]

NOISE_KEYWORDS = [
    "promo", "iklan", "jual", "diskon", "murah", "gratis", "bonus", "cashback",
    "giveaway", "vouch", "prediksi", "togel", "slot", "gacor", "open bo",
    "spam", "click here", "daftar sekarang"
]

def run_sense():
    db = SessionLocal()
    try:
        db.add(LifeLog(engine="sense", type="info", message="Starting real sense cycle with noise filtering"))
        db.commit()

        for source in SOURCES:
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                resp = requests.get(source["url"], headers=headers, timeout=15)
                if resp.status_code != 200:
                    continue

                soup = BeautifulSoup(resp.text, 'html.parser')
                links = soup.select(source["selector"])

                for link in links[:5]:
                    href = link.get('href')
                    if not href: continue
                    if not href.startswith('http'):
                        if "kaskus.co.id" in source["url"]:
                            href = "https://www.kaskus.co.id" + href
                        elif "diskusiweb.com" in source["url"]:
                            href = "https://diskusiweb.com" + href
                        else:
                            domain = source["url"].split('//')[1].split('/')[0]
                            href = f"https://{domain}{href}"

                    title = link.get_text().strip()

                    # Noise Filtering
                    if any(kw in title.lower() for kw in NOISE_KEYWORDS):
                        continue

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

                    if not content or len(content) < 50:
                        content = title

                    # Secondary noise check on content
                    if any(kw in content.lower() for kw in NOISE_KEYWORDS):
                        continue

                    db.add(ProblemRaw(
                        source=source["name"],
                        external_id=f"{source['name']}_{int(time.time())}_{hash(href)}",
                        title=title,
                        content=content,
                        url=href
                    ))
            except Exception as e:
                db.add(LifeLog(engine="sense", type="error", message=f"Failed to scrape {source['name']}: {str(e)}"))

        db.commit()
    finally:
        db.close()
