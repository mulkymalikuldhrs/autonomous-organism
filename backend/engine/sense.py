import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import datetime
import re
from ..models import SessionLocal, ProblemRaw, ProblemClean, EngineLog, Base, engine as db_engine

class SenseEngine:
    def __init__(self):
        self.sources = [
            {"name": "Reddit Indonesia", "url": "https://www.reddit.com/r/indonesia/new/", "type": "reddit"},
            {"name": "Kaskus Bisnis", "url": "https://www.kaskus.co.id/forum/21/bisnis", "type": "kaskus"},
            {"name": "Quora ID", "url": "https://id.quora.com/search?q=masalah", "type": "quora"}
        ]

    async def scrape_source(self, browser, source):
        page = await browser.new_page()
        print(f"   👁️ Scraping {source['name']}...")
        try:
            await page.goto(source['url'], timeout=60000)
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')

            problems = []
            if source['type'] == 'reddit':
                # Simplified reddit parsing
                posts = soup.find_all('shreddit-post')
                for post in posts:
                    title = post.get('post-title', '')
                    if title:
                        problems.append({
                            "source": source['name'],
                            "text": title,
                            "external_id": post.get('id', str(hash(title)))
                        })

            elif source['type'] == 'kaskus':
                # Simplified kaskus parsing
                threads = soup.find_all('a', class_='thread-title')
                for thread in threads:
                    title = thread.get_text().strip()
                    if title:
                        problems.append({
                            "source": source['name'],
                            "text": title,
                            "external_id": str(hash(title))
                        })

            else:
                # Generic fallback
                texts = soup.find_all(['h1', 'h2', 'h3', 'p'])
                for t in texts:
                    txt = t.get_text().strip()
                    if len(txt) > 20 and any(kw in txt.lower() for kw in ['susah', 'masalah', 'bagaimana', 'help', 'tolong']):
                        problems.append({
                            "source": source['name'],
                            "text": txt,
                            "external_id": str(hash(txt))
                        })

            return problems
        except Exception as e:
            print(f"   ❌ Error scraping {source['name']}: {e}")
            return []
        finally:
            await page.close()

    def clean_text(self, text):
        # Remove noise
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip().lower()

    async def run(self):
        print("\n" + "="*50)
        print("👁️ SENSE ENGINE (INDRA) STARTING")
        print("="*50)

        Base.metadata.create_all(bind=db_engine)

        db = SessionLocal()
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)

                all_problems = []
                for source in self.sources:
                    problems = await self.scrape_source(browser, source)
                    all_problems.extend(problems)

                await browser.close()

                inserted = 0
                for p in all_problems:
                    # Check if exists
                    exists = db.query(ProblemRaw).filter(ProblemRaw.external_id == p['external_id']).first()
                    if not exists:
                        new_raw = ProblemRaw(
                            source=p['source'],
                            text=p['text'],
                            external_id=p['external_id']
                        )
                        db.add(new_raw)
                        db.flush() # Get ID

                        clean_txt = self.clean_text(p['text'])
                        new_clean = ProblemClean(
                            raw_id=new_raw.id,
                            text_clean=clean_txt
                        )
                        db.add(new_clean)
                        inserted += 1

                db.commit()

                log = EngineLog(
                    level="success",
                    source="SENSE",
                    message=f"Scanned {len(all_problems)} items, inserted {inserted} new problems."
                )
                db.add(log)
                db.commit()

                print(f"✅ SENSE ENGINE COMPLETE: {inserted} new problems found.")
                return inserted

        except Exception as e:
            print(f"🔥 SENSE ENGINE CRITICAL ERROR: {e}")
            log = EngineLog(
                level="error",
                source="SENSE",
                message=f"Critical failure: {str(e)}"
            )
            db.add(log)
            db.commit()
            return 0
        finally:
            db.close()

if __name__ == "__main__":
    engine = SenseEngine()
    asyncio.run(engine.run())
