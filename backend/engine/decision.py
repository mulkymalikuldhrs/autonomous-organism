from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
import asyncio

def get_sia():
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    return SentimentIntensityAnalyzer()

async def run_decision(db: Session):
    log = models.EngineLog(level="info", source="Decision", message="Decision core started")
    db.add(log)
    db.commit()

    sia = get_sia()

    # Load clean problems
    problems = db.query(models.ProblemClean).order_by(models.ProblemClean.created_at.desc()).limit(100).all()
    if not problems:
        db.add(models.EngineLog(level="warning", source="Decision", message="No clean problems found to analyze."))
        db.commit()
        return

    texts = [p.text_clean for p in problems]

    # 1. Clustering (to find themes)
    n_clusters = min(5, len(texts))
    if n_clusters > 1:
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(texts)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(X)

        # Group by cluster
        df = pd.DataFrame({'text': texts, 'cluster': kmeans.labels_})
    else:
        df = pd.DataFrame({'text': texts, 'cluster': [0]*len(texts)})

    # 2. Sentiment Analysis & Clustering Data
    clusters_data = []
    for i in range(n_clusters):
        cluster_texts = df[df['cluster'] == i]['text'].tolist()
        combined_text = "\n".join(cluster_texts)
        sent = sia.polarity_scores(combined_text)

        clusters_data.append({
            "id": i,
            "volume": len(cluster_texts),
            "neg_sentiment": sent['neg'],
            "content": combined_text[:1500]
        })

    # 3. LLM Analysis for each cluster to get estimates
    best_idea = None
    max_score = -1

    for cluster in clusters_data:
        prompt = f"""Analyze these grouped complaints and suggest a SaaS MVP idea.
Complaints:
{cluster['content']}

Return format:
THEME: <title>
SUMMARY: <description>
AUTOMATION_POTENTIAL: <0.0 to 1.0>
REVENUE_POTENTIAL: <0.0 to 1.0>
"""
        llm_output = await llm.generate(prompt, system="You are the Decision Core of an autonomous SaaS organism.")

        # Parse LLM output
        import re
        theme_match = re.search(r"THEME:\s*(.*)", llm_output, re.I)
        summary_match = re.search(r"SUMMARY:\s*(.*)", llm_output, re.S | re.I)
        auto_match = re.search(r"AUTOMATION_POTENTIAL:\s*([\d\.]+)", llm_output)
        rev_match = re.search(r"REVENUE_POTENTIAL:\s*([\d\.]+)", llm_output)

        theme = theme_match.group(1).strip() if theme_match else "Unknown Idea"
        summary = summary_match.group(1).strip() if summary_match else "No summary provided"
        # Split summary if it contains other fields
        summary = summary.split("AUTOMATION_POTENTIAL")[0].strip()

        auto_est = float(auto_match.group(1)) if auto_match else 0.5
        rev_est = float(rev_match.group(1)) if rev_match else 0.5

        # Formula: score = (volume * 0.4) + (neg_sentiment * 0.2) + (auto_est * 0.2) + (rev_est * 0.2)
        # Normalize volume (cap at 50 for scoring purposes)
        norm_volume = min(cluster['volume'] / 50.0, 1.0)

        score = (norm_volume * 40) + (cluster['neg_sentiment'] * 20) + (auto_est * 20) + (rev_est * 20)

        if score > max_score:
            max_score = score
            best_idea = {
                "theme": theme,
                "summary": summary,
                "score": score,
                "evidence": {"cluster_id": cluster['id'], "llm_raw": llm_output}
            }

    if best_idea:
        idea = models.IdeaCandidate(
            theme=best_idea['theme'],
            score=best_idea['score'],
            summary=best_idea['summary'],
            evidence=best_idea['evidence']
        )
        db.add(idea)
        db.add(models.EngineLog(level="info", source="Decision", message=f"New idea generated: {best_idea['theme']} (Score: {best_idea['score']:.2f})"))
        db.commit()
