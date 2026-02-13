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

    # 2. Sentiment Analysis & Scoring
    cluster_scores = []
    for i in range(n_clusters):
        cluster_texts = df[df['cluster'] == i]['text'].tolist()
        combined_text = "\n".join(cluster_texts)

        # Sentiment
        sent = sia.polarity_scores(combined_text)
        neg_score = sent['neg']

        # Simple scoring formula: neg_score * 40 + volume * 2
        score = (neg_score * 40) + (len(cluster_texts) * 2)
        cluster_scores.append((i, score, combined_text[:1000]))

    # Sort by score
    cluster_scores.sort(key=lambda x: x[1], reverse=True)
    top_cluster = cluster_scores[0]

    # 3. LLM Refinement
    prompt = f"Analyze these grouped complaints and suggest a SaaS MVP idea.\nComplaints:\n{top_cluster[2]}\n\nReturn format:\nTHEME: <title>\nSCORE: <0-100>\nSUMMARY: <description>"
    llm_output = await llm.generate(prompt, system="You are the Decision Core of an autonomous SaaS organism.")

    # Parse LLM output
    import re
    theme = (re.search(r"THEME:\s*(.*)", llm_output, re.I).group(1) if re.search(r"THEME:\s*(.*)", llm_output, re.I) else "Unknown").strip()
    score_raw = (re.search(r"SCORE:\s*(\d+)", llm_output).group(1) if re.search(r"SCORE:\s*(\d+)", llm_output) else str(top_cluster[1])).strip()
    summary = (re.search(r"SUMMARY:\s*(.*)", llm_output, re.S).group(1) if re.search(r"SUMMARY:\s*(.*)", llm_output, re.S) else "No summary").strip()

    # Save idea
    idea = models.IdeaCandidate(
        theme=theme,
        score=float(score_raw),
        summary=summary,
        evidence={"cluster_data": top_cluster[2], "raw_llm": llm_output}
    )
    db.add(idea)
    db.add(models.EngineLog(level="info", source="Decision", message=f"New idea generated: {theme} (Score: {score_raw})"))
    db.commit()
