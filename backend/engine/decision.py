from sqlalchemy.orm import Session
from ..models import ProblemClean, IdeaCandidate, EngineLog, ProblemRaw
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import warnings

# Ignore sklearn warnings for small datasets
warnings.filterwarnings("ignore", category=UserWarning)

def run_decision(db: Session, run_id: int):
    log = EngineLog(run_id=run_id, level="info", source="DECISION", message="Decision Core: Analyzing collective human pain patterns...")
    db.add(log)
    db.commit()

    problems = db.query(ProblemClean).all()
    if len(problems) < 3:
        log = EngineLog(run_id=run_id, level="warning", source="DECISION", message="Insufficient data for clustering (minimum 3 problems required).")
        db.add(log)
        db.commit()
        return 0

    texts = [p.text_clean for p in problems]
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(texts)

    # Determine cluster count
    n_clusters = min(5, len(problems))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X)

    clusters = kmeans.labels_
    analyzer = SentimentIntensityAnalyzer()

    results_count = 0
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(n_clusters):
        cluster_indices = np.where(clusters == i)[0]
        cluster_texts = [texts[idx] for idx in cluster_indices]

        neg_sentiments = [analyzer.polarity_scores(txt)['neg'] for txt in cluster_texts]
        avg_neg = np.mean(neg_sentiments) if neg_sentiments else 0
        volume = len(cluster_indices)

        # Formula: score = (volume * 0.4) + (neg * 0.2) + (autom * 0.2) + (money * 0.2)
        # We normalize volume (0-10) and neg sentiment (0-1)
        # Here we scale for visibility in UI
        score_val = (volume * 2.0) + (avg_neg * 50.0) + 10.0

        top_terms = [terms[ind] for ind in order_centroids[i, :5]]
        theme = " ".join(top_terms).title()

        summary = f"Identified a cluster of {volume} related issues focused on: {theme}. " \
                  f"Sentiment analysis shows an average negativity of {avg_neg:.2f}."

        candidate = IdeaCandidate(
            theme=theme,
            score=round(score_val, 2),
            summary=summary,
            evidence={
                "cluster_size": volume,
                "top_terms": top_terms,
                "neg_sentiment": float(avg_neg),
                "sources": [problems[idx].raw_id for idx in cluster_indices[:3]]
            }
        )
        db.add(candidate)
        results_count += 1

    db.commit()

    log = EngineLog(run_id=run_id, level="success", source="DECISION", message=f"Decision Core: Successfully processed {len(problems)} problems into {results_count} idea candidates.")
    db.add(log)
    db.commit()
    return results_count
