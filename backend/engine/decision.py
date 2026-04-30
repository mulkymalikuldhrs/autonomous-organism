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
    log = models.EngineLog(level="info", source="Decision", message="Decision core started (Gen-4.1 Blueprint Scoring)")
    db.add(log)
    db.commit()

    sia = get_sia()

    # Load dynamic weights from SystemSetting
    def get_weight(key, default):
        s = db.query(models.SystemSetting).filter(models.SystemSetting.key == key).first()
        return s.value if s else default

    # These are used as dynamic multipliers if evolution engine changes them,
    # but we follow the blueprint's fixed formula for the final score structure.
    w_neg_mult = get_weight("decision_neg_weight", 1.0)
    w_vol_mult = get_weight("decision_volume_weight", 1.0)
    w_auto_mult = get_weight("decision_automation_weight", 1.0)
    w_rev_mult = get_weight("decision_revenue_weight", 1.0)

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
    max_volume = 0
    for i in range(n_clusters):
        c_texts = df[df['cluster'] == i]['text'].tolist()
        vol = len(c_texts)
        if vol > max_volume: max_volume = vol

        combined = "\n".join(c_texts)
        sent = sia.polarity_scores(combined)

        cluster_stats.append({
            "id": i,
            "texts": combined[:2000],
            "volume": vol,
            "neg_emotion": sent['neg']
        })

    # Sort and take top 3 for deep LLM analysis
    # Use volume and negativity for initial ranking
    cluster_stats.sort(key=lambda x: (x['volume'] * 0.5 + x['neg_emotion'] * 0.5), reverse=True)
    top_clusters = cluster_stats[:3]

    for cluster in top_clusters:
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

        # Normalized Volume (0-1)
        norm_vol = cluster['volume'] / max_volume if max_volume > 0 else 0

        # Blueprint Formula:
        # score = (jumlah_keluhan * 0.4) + (emosi_negatif * 0.2) + (mudah_otomatis * 0.2) + (potensi_uang * 0.2)
        # We apply the dynamic multipliers from SystemSetting on top of these weights.

        final_score = (
            (norm_vol * 0.4 * w_vol_mult) +
            (cluster['neg_emotion'] * 0.2 * w_neg_mult) +
            (auto_ease * 0.2 * w_auto_mult) +
            (rev_pot * 0.2 * w_rev_mult)
        ) * 100 # Scale to 0-100

        # Save idea
        idea = models.IdeaCandidate(
            theme=theme,
            score=final_score,
            summary=summary,
            evidence={
                "cluster_id": cluster['id'],
                "auto_ease": auto_ease,
                "rev_pot": rev_pot,
                "volume": cluster['volume'],
                "neg_emotion": cluster['neg_emotion'],
                "raw_llm": res
            }
        )
        db.add(idea)
        db.add(models.EngineLog(level="info", source="Decision", message=f"Idea generated: {theme} (Score: {final_score:.2f})"))

    db.commit()
