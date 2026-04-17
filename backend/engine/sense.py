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
    {"name": "Reddit SaaS", "url": "https://www.reddit.com/r/saas/.rss", "type": "rss"},
    {"name": "Reddit Indonesia", "url": "https://www.reddit.com/r/indonesia/.rss", "type": "rss"},
    {"name": "Kaskus Bisnis", "url": "https://www.kaskus.co.id/forum/21/bisnis", "type": "dynamic"},
    {"name": "Kaskus Tech", "url": "https://www.kaskus.co.id/forum/20/technology", "type": "dynamic"},
    {"name": "Quora ID Search", "url": "https://id.quora.com/search?q=masalah", "type": "dynamic"},
    {"name": "YouTube Trends ID", "url": "https://www.youtube.com/feed/trending?gl=ID", "type": "dynamic"},
    {"name": "ProductHunt", "url": "https://www.producthunt.com/", "type": "dynamic"},
    {"name": "IndieHackers", "url": "https://www.indiehackers.com/", "type": "dynamic"},
]

async def scrape_dynamic(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use a real-looking user agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            await page.goto(url, timeout=60000, wait_until="networkidle")
            await page.wait_for_timeout(5000) # Wait extra for client-side rendering
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
        # Handle both standard RSS and Atom (Reddit uses Atom)
        entries = []

        # Atom parsing
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('.//atom:entry', ns):
            title = entry.find('atom:title', ns)
            if title is not None:
                entries.append(title.text)

        # Standard RSS parsing
        for item in root.findall('.//item'):
            title = item.find('title')
            if title is not None:
                entries.append(title.text)

        return entries
    except Exception as e:
        print(f"RSS parse error: {e}")
        return []

def parse_generic(html: str):
    if not html: return []
    soup = BeautifulSoup(html, 'lxml')
    entries = []

    # Target Kaskus thread titles
    for title in soup.select('.thread-title, .entry-title, h1, h2, h3'):
        text = title.get_text().strip()
        if len(text) > 20:
            entries.append(text)

    # Target YouTube video titles
    for video in soup.select('#video-title'):
        text = video.get_text().strip()
        if len(text) > 15:
            entries.append(text)

    return list(set(entries))

async def noise_filter(text: str) -> bool:
    """Uses LLM to decide if a text is a real problem/complaint or just noise."""
    prompt = f"Is the following text a user complaint, a problem, or a potential SaaS opportunity? Answer with only 'YES' or 'NO'.\nText: {text}"
    response = await llm.generate(prompt, system="You are a noise filter for an Indonesian-focused SaaS organism. You understand both English and Indonesian.")
    return "YES" in response.upper()

async def run_sense(db: Session):
    log = models.EngineLog(level="info", source="Sense", message="Sense engine started (Gen-4 Regional Mode)")
    db.add(log)
    db.commit()

    all_findings = []
    for source in SOURCES:
        is_dyn = source["type"] == "dynamic"
        print(f"Sensing: {source['name']}...")
        content = await scrape_source(source["url"], is_dynamic=is_dyn)
        if content:
            findings = []
            if source["type"] == "hn":
                findings = parse_hn(content)
            elif source["type"] == "rss":
                findings = parse_rss(content)
            else:
                findings = parse_generic(content)

            print(f"  Found {len(findings)} items in {source['name']}")
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
