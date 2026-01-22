from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..sense_engine.scraper import scrape_reddit
from ..sense_engine.cleaner import clean_text
from ..sense_engine.models import ProblemRaw, ProblemClean
from ..decision_core.analyzer import analyze_problems
from ..decision_core.scorer import score_clusters
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Problem(BaseModel):
    text: str

class Idea(BaseModel):
    theme: str
    score: float
    summary: str

@app.post("/sense/scrape", response_model=List[Problem])
def run_scraper(subreddit: str, db: Session = Depends(get_db)):
    posts = scrape_reddit(subreddit)
    problems = []
    for post in posts:
        raw_problem = ProblemRaw(source=subreddit, text=post['title'] + " " + post['text'])
        db.add(raw_problem)
        db.commit()
        db.refresh(raw_problem)

        cleaned_text = clean_text(raw_problem.text)
        clean_problem = ProblemClean(text_clean=cleaned_text, raw_id=raw_problem.id)
        db.add(clean_problem)
        db.commit()
        problems.append({"text": clean_problem.text_clean})
    return problems

@app.get("/decision/ideas", response_model=List[Idea])
def get_ideas(db: Session = Depends(get_db)):
    clean_problems = db.query(ProblemClean).all()
    problem_texts = [p.text_clean for p in clean_problems]

    if not problem_texts:
        return []

    analysis_df = analyze_problems(problem_texts)
    scored_df = score_clusters(analysis_df)

    ideas = []
    for _, row in scored_df.iterrows():
        ideas.append({
            "theme": f"Cluster {row['cluster']}",
            "score": row['score'],
            "summary": row['summary']
        })
    return ideas

from ..saas_factory.generator import create_nextjs_project

class Project(BaseModel):
    name: str

@app.post("/factory/create", response_model=Project)
def create_project(project: Project):
    create_nextjs_project(project.name)
    return {"name": project.name}

@app.get("/")
def read_root():
    return {"message": "ORGANISME SAAS OTONOM API is running."}
