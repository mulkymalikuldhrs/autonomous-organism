from sqlalchemy.orm import Session
from .. import models
from .llm import llm
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
import asyncio
import re

def get_sia():
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    return SentimentIntensityAnalyzer()

async def run_decision(db: Session):
    log = models.EngineLog(level="info", source="Decision", message="Decision core started (Gen-4 Weighted Formula)")
    db.add(log)
    db.commit()

    sia = get_sia()

    # Load settings/weights
    def get_weight(key, default):
        s = db.query(models.SystemSetting).filter(models.SystemSetting.key == key).first()
        return s.value if s else default

    w_neg = get_weight("decision_neg_weight", 40.0)
    w_vol = get_weight("decision_volume_weight", 2.0)
    w_auto = get_weight("decision_automation_weight", 20.0)
    w_rev = get_weight("decision_revenue_weight", 20.0)

    # Load clean problems
    problems = db.query(models.ProblemClean).order_by(models.ProblemClean.created_at.desc()).limit(200).all()
    if not problems:
        db.add(models.EngineLog(level="warning", source="Decision", message="No clean problems found to analyze."))
        db.commit()
        return

    texts = [p.text_clean for p in problems]

    # 1. Clustering
    n_clusters = min(8, len(texts))
    if n_clusters > 1:
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(texts)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(X)
        df = pd.DataFrame({'text': texts, 'cluster': kmeans.labels_})
    else:
        df = pd.DataFrame({'text': texts, 'cluster': [0]*len(texts)})

    # 2. Analysis & Initial Scoring
    cluster_stats = []
    for i in range(n_clusters):
        c_texts = df[df['cluster'] == i]['text'].tolist()
        combined = "\n".join(c_texts)
        sent = sia.polarity_scores(combined)

        # Initial score based on volume and sentiment
        base_score = (sent['neg'] * w_neg) + (len(c_texts) * w_vol)
        cluster_stats.append({
            "id": i,
            "texts": combined[:2000],
            "base_score": base_score,
            "volume": len(c_texts),
            "neg_emotion": sent['neg']
        })

    # Sort and take top 3 for deep LLM analysis
    cluster_stats.sort(key=lambda x: x['base_score'], reverse=True)
    top_clusters = cluster_stats[:3]

    for cluster in top_clusters:
        # Deep analysis with LLM for Automation Ease and Revenue Potential
        prompt = f"""Analyze these user complaints and estimate SaaS potential:
Complaints:
{cluster['texts']}

Rate from 0.0 to 1.0:
1. Automation Ease (How easy is it to build an automated solution?)
2. Revenue Potential (Will people pay for this?)
3. Market Gap (Is there a clear lack of solutions?)

Format:
AUTOMATION_EASE: <float>
REVENUE_POTENTIAL: <float>
MARKET_GAP: <float>
THEME: <title>
SUMMARY: <description>
"""
        res = await llm.generate(prompt, system="You are the Decision Core. Be analytical and brutal.")

        # Parse
        auto_ease = float(re.search(r"AUTOMATION_EASE:\s*([\d\.]+)", res).group(1) if re.search(r"AUTOMATION_EASE:\s*([\d\.]+)", res) else 0.5)
        rev_pot = float(re.search(r"REVENUE_POTENTIAL:\s*([\d\.]+)", res).group(1) if re.search(r"REVENUE_POTENTIAL:\s*([\d\.]+)", res) else 0.5)
        theme = (re.search(r"THEME:\s*(.*)", res).group(1) if re.search(r"THEME:\s*(.*)", res) else "Unknown").strip()
        summary = (re.search(r"SUMMARY:\s*(.*)", res, re.S).group(1) if re.search(r"SUMMARY:\s*(.*)", res, re.S) else "No summary").strip()

        # Final Weighted Formula
        # Using dynamic weights from Evolution Engine
        # Weights are stored in SystemSetting table as floats (e.g. 40.0, 2.0)
        # We normalize auto_ease and rev_pot (0-1) to 0-100 scale for consistency with weights

        # Mapping to blueprint-style 0.4, 0.2, 0.2, 0.2 distribution if settings are at defaults:
        # volume: 2.0 (w_vol) * 0.4 multiplier? No, let's use weights directly as the blueprint suggests.
        # The blueprint says: score = (complaints * 0.4) + (negative_emotion * 0.2) + (automation_ease * 0.2) + (money_potential * 0.2)
        # We use SystemSetting values if they exist, otherwise fallback to blueprint weights.

        final_score = (
            (cluster['volume'] * (w_vol / 100 if w_vol > 1 else 0.4)) +
            (cluster['neg_emotion'] * 100 * (w_neg / 100 if w_neg > 1 else 0.2)) +
            (auto_ease * 100 * (w_auto / 100 if w_auto > 1 else 0.2)) +
            (rev_pot * 100 * (w_rev / 100 if w_rev > 1 else 0.2))
        )

        # Save idea
        idea = models.IdeaCandidate(
            theme=theme,
            score=final_score,
            summary=summary,
            evidence={
                "cluster_id": cluster['id'],
                "auto_ease": auto_ease,
                "rev_pot": rev_pot,
                "base_score": cluster['base_score'],
                "raw_llm": res
            }
        )
        db.add(idea)
        db.add(models.EngineLog(level="info", source="Decision", message=f"Idea generated: {theme} (Final Score: {final_score:.2f})"))

    db.commit()
