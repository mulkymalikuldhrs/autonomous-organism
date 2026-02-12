import httpx
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .. import models
import datetime

SOURCES = [
    {"name": "HackerNews Newest", "url": "https://news.ycombinator.com/newest", "type": "hn"},
    {"name": "HackerNews Show", "url": "https://news.ycombinator.com/show", "type": "hn"},
]

async def scrape_source(url: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        async with httpx.AsyncClient(headers=headers, timeout=15.0, follow_redirects=True) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Status {response.status_code} for {url}")
    except Exception as e:
        print(f"Scraping error for {url}: {e}")
    return None

def parse_hn(html: str):
    if not html: return []
    soup = BeautifulSoup(html, 'html.parser')
    entries = []
    for span in soup.select('span.titleline'):
        a = span.find('a')
        if a:
            entries.append(a.get_text())
    return entries

async def run_sense(db: Session):
    log = models.EngineLog(level="info", source="Sense", message="Sense engine started (HN mode)")
    db.add(log)
    db.commit()

    all_findings = []
    for source in SOURCES:
        html = await scrape_source(source["url"])
        if html:
            if source["type"] == "hn":
                findings = parse_hn(html)
                all_findings.extend([(source["url"], text) for text in findings])

    new_count = 0
    clean_count = 0
    for src, text in all_findings:
        exists = db.query(models.ProblemRaw).filter(models.ProblemRaw.text == text).first()
        if not exists:
            prob = models.ProblemRaw(source=src, text=text)
            db.add(prob)
            new_count += 1

        # Auto-clean
        clean_text = text.strip()
        if len(clean_text) > 10:
            exists_clean = db.query(models.ProblemClean).filter(models.ProblemClean.text_clean == clean_text).first()
            if not exists_clean:
                clean = models.ProblemClean(text_clean=clean_text)
                db.add(clean)
                clean_count += 1

    db.commit()
    log_msg = f"Sense finished. Scanned {len(all_findings)} items, {new_count} new raw, {clean_count} new clean."
    db.add(models.EngineLog(level="info", source="Sense", message=log_msg))
    db.commit()
