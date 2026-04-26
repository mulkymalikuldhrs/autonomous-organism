import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import datetime
import xml.etree.ElementTree as ET

SOURCES = [
    {"name": "HackerNews Newest", "url": "https://news.ycombinator.com/newest", "type": "hn"},
    {"name": "HackerNews Show", "url": "https://news.ycombinator.com/show", "type": "hn"},
    {"name": "Reddit SaaS", "url": "https://www.reddit.com/r/saas/.rss", "type": "rss"},
    {"name": "Reddit Startups", "url": "https://www.reddit.com/r/startups/.rss", "type": "rss"},
    {"name": "Reddit Entrepreneur", "url": "https://www.reddit.com/r/entrepreneur/.rss", "type": "rss"},
    {"name": "ProductHunt", "url": "https://www.producthunt.com/", "type": "dynamic"},
    {"name": "IndieHackers", "url": "https://www.indiehackers.com/", "type": "dynamic"},
    {"name": "Kaskus Bisnis", "url": "https://www.kaskus.co.id/forum/21/bisnis", "type": "dynamic"},
    {"name": "Kaskus Tech", "url": "https://www.kaskus.co.id/forum/20/technology", "type": "dynamic"},
    {"name": "Quora ID Search", "url": "https://id.quora.com/search?q=masalah", "type": "dynamic"},
    {"name": "YouTube ID Trending", "url": "https://www.youtube.com/feed/trending?gl=ID", "type": "dynamic"},
]

async def scrape_dynamic(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=30000)
            await page.wait_for_timeout(5000) # Wait for content
            content = await page.content()
            return content
        except Exception as e:
            print(f"Dynamic scraping error for {url}: {e}")
        finally:
            await browser.close()
    return None

async def scrape_source(url: str, is_dynamic: bool = False):
    if is_dynamic:
        return await scrape_dynamic(url)

    import httpx
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        async with httpx.AsyncClient(headers=headers, timeout=15.0, follow_redirects=True) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.text
    except Exception as e:
        print(f"Scraping error for {url}: {e}")
    return None

def parse_hn(html: str):
    if not html: return []
    soup = BeautifulSoup(html, 'lxml')
    entries = []
    for span in soup.select('span.titleline'):
        a = span.find('a')
        if a:
            entries.append(a.get_text())
    return entries

def parse_rss(xml_content: str):
    if not xml_content: return []
    try:
        root = ET.fromstring(xml_content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            if title is not None:
                entries.append(title.text)
        return entries
    except Exception as e:
        print(f"RSS parse error: {e}")
        return []

def parse_generic(html: str):
    if not html: return []
    soup = BeautifulSoup(html, 'lxml')
    # Try to find common headline elements
    entries = []
    # Common selectors for titles/problems across various sites
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        text = h.get_text().strip()
        if len(text) > 20 and len(text) < 300:
            entries.append(text)

    # Specific for Kaskus/Forum structures if h2/h3 are not used
    for a in soup.select('a.thread-title, a.title, .q-text.qu-dynamicFontSize--regular'):
        text = a.get_text().strip()
        if len(text) > 20 and len(text) < 300:
            entries.append(text)

    return list(set(entries))

async def noise_filter(text: str) -> bool:
    """Uses LLM to decide if a text is a real problem/complaint or just noise."""
    prompt = f"Is the following text a user complaint or a potential SaaS opportunity? Answer with only 'YES' or 'NO'.\nText: {text}"
    response = await llm.generate(prompt, system="You are a noise filter for a SaaS organism.")
    return "YES" in response.upper()

async def run_sense(db: Session):
    log = models.EngineLog(level="info", source="Sense", message="Sense engine started (Gen-4 Playwright mode)")
    db.add(log)
    db.commit()

    all_findings = []
    for source in SOURCES:
        is_dyn = source["type"] == "dynamic"
        content = await scrape_source(source["url"], is_dynamic=is_dyn)
        if content:
            findings = []
            if source["type"] == "hn":
                findings = parse_hn(content)
            elif source["type"] == "rss":
                findings = parse_rss(content)
            else:
                findings = parse_generic(content)

            all_findings.extend([(source["url"], text) for text in findings])

    new_count = 0
    clean_count = 0
    for src, text in all_findings:
        if not text: continue
        exists = db.query(models.ProblemRaw).filter(models.ProblemRaw.text == text).first()
        if not exists:
            prob = models.ProblemRaw(source=src, text=text)
            db.add(prob)
            new_count += 1

            # Noise filter and clean
            if len(text) > 15:
                if await noise_filter(text):
                    clean_text = text.strip()
                    exists_clean = db.query(models.ProblemClean).filter(models.ProblemClean.text_clean == clean_text).first()
                    if not exists_clean:
                        clean = models.ProblemClean(text_clean=clean_text)
                        db.add(clean)
                        clean_count += 1

    db.commit()
    log_msg = f"Sense finished. Scanned {len(all_findings)} items, {new_count} new raw, {clean_count} new clean (filtered)."
    db.add(models.EngineLog(level="info", source="Sense", message=log_msg))
    db.commit()
    return {"scanned": len(all_findings), "new": new_count}
