import httpx
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from ..models import ProblemRaw, ProblemClean, EngineLog
from datetime import datetime
import json

async def scrape_hackernews(db: Session, run_id: int):
    url = "https://news.ycombinator.com/show"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code != 200:
                return 0

            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('tr', class_='athing')

            count = 0
            for item in items[:20]:
                title_tag = item.find('span', class_='titleline')
                if not title_tag: continue

                title = title_tag.text
                link_tag = title_tag.find('a')
                link = link_tag['href'] if link_tag else ""
                ext_id = f"hn_{item.get('id', 'unknown')}"

                exists = db.query(ProblemRaw).filter(ProblemRaw.external_id == ext_id).first()
                if not exists:
                    raw = ProblemRaw(
                        source="hackernews",
                        external_id=ext_id,
                        title=title,
                        url=link,
                        content=title
                    )
                    db.add(raw)
                    db.flush()

                    clean = ProblemClean(
                        raw_id=raw.id,
                        text_clean=title
                    )
                    db.add(clean)
                    count += 1

            db.commit()
            return count
        except Exception as e:
            print(f"HN Scrape Error: {e}")
            return 0

async def scrape_reddit(db: Session, run_id: int, subreddit: str = "startups"):
    url = f"https://www.reddit.com/r/{subreddit}/new.json"
    headers = {"User-Agent": "OrganismSense/1.0"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code != 200:
                return 0

            data = response.json()
            posts = data.get('data', {}).get('children', [])

            count = 0
            for post in posts[:15]:
                pdata = post['data']
                ext_id = f"reddit_{pdata['id']}"
                title = pdata['title']
                content = pdata.get('selftext', '')
                url_post = f"https://reddit.com{pdata['permalink']}"

                exists = db.query(ProblemRaw).filter(ProblemRaw.external_id == ext_id).first()
                if not exists:
                    raw = ProblemRaw(
                        source=f"reddit/r/{subreddit}",
                        external_id=ext_id,
                        title=title,
                        url=url_post,
                        content=f"{title}\n\n{content}"
                    )
                    db.add(raw)
                    db.flush()

                    clean = ProblemClean(
                        raw_id=raw.id,
                        text_clean=f"{title} {content}"[:5000]
                    )
                    db.add(clean)
                    count += 1

            db.commit()
            return count
        except Exception as e:
            print(f"Reddit Scrape Error: {e}")
            return 0

async def run_sense(db: Session, run_id: int):
    log = EngineLog(run_id=run_id, level="info", source="SENSE", message="Sense Engine: Infiltrating HackerNews and Reddit...")
    db.add(log)
    db.commit()

    hn_count = await scrape_hackernews(db, run_id)
    rd_count = await scrape_reddit(db, run_id, "startups")
    rd_count2 = await scrape_reddit(db, run_id, "problems")

    total = hn_count + rd_count + rd_count2
    log = EngineLog(run_id=run_id, level="success", source="SENSE", message=f"Sense Engine Complete. Total new problems detected: {total}")
    db.add(log)
    db.commit()
    return total
