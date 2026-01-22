import { chromium } from 'playwright';
import * as cheerio from 'cheerio';

interface ScrapedProblem {
  source: string;
  text: string;
}

/**
 * Scrapes a given URL for potential user problems.
 * This implementation is a basic example targeting a subreddit.
 *
 * @param url The URL of the subreddit to scrape.
 * @returns A promise that resolves to an array of ScrapedProblem objects.
 */
export async function scrapeProblems(url: string): Promise<ScrapedProblem[]> {
  console.log(`Scraping problems from: ${url}`);
  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    await page.goto(url, { waitUntil: 'networkidle' });

    // Wait for the posts to be loaded on the page.
    // Reddit uses dynamic class names, so we need a robust selector.
    // Let's target the post container element `shreddit-post`.
    await page.waitForSelector('shreddit-post', { timeout: 10000 });

    const content = await page.content();
    await browser.close();

    const $ = cheerio.load(content);
    const problems: ScrapedProblem[] = [];

    // Target `shreddit-post` and then look for the title within it.
    $('shreddit-post').each((_index, element) => {
      const title = $(element).find('h3').text().trim();
      if (title) {
        problems.push({
          source: url,
          text: title,
        });
      }
    });

    console.log(`Found ${problems.length} potential problems.`);
    return problems;
  } catch (error) {
    console.error(`Error scraping ${url}:`, error);
    await browser.close();
    return [];
  }
}
