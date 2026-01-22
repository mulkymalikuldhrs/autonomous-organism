
interface ScrapedProblem {
  source: string;
  text: string;
}

/**
 * Cleans the scraped text by removing spam, duplicates, and noise.
 *
 * @param problems An array of ScrapedProblem objects.
 * @returns A new array of ScrapedProblem objects with cleaned text.
 */
export function cleanProblems(problems: ScrapedProblem[]): ScrapedProblem[] {
  console.log(`Cleaning ${problems.length} problems...`);

  const cleanedProblems: ScrapedProblem[] = [];
  const seenTexts = new Set<string>();

  for (const problem of problems) {
    let cleanedText = problem.text;

    // Remove common spam phrases (simple example)
    cleanedText = cleanedText.replace(/buy now|limited offer/gi, '');

    // Trim whitespace
    cleanedText = cleanedText.trim();

    // Remove duplicates
    if (seenTexts.has(cleanedText)) {
      continue;
    }

    // Filter out low-quality or very short posts
    if (cleanedText.length < 20 || !cleanedText.includes(' ')) {
      continue;
    }

    seenTexts.add(cleanedText);
    cleanedProblems.push({
      ...problem,
      text: cleanedText,
    });
  }

  console.log(`Finished cleaning. ${cleanedProblems.length} problems remaining.`);
  return cleanedProblems;
}
