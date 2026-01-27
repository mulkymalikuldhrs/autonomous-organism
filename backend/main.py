from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sense_engine.scraper import scrape_text
from decision_core.analyzer import analyze_problems
from database import SessionLocal, create_db_and_tables, ProblemClean, ProblemRaw
import datetime

app = FastAPI()

# Create database and tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

class ScrapeRequest(BaseModel):
    url: str
    source: str

@app.post("/scrape")
def scrape(request: ScrapeRequest):
    text = scrape_text(request.url)
    if "An error occurred" in text or "Error response" in text:
        raise HTTPException(status_code=400, detail=text)

    db = SessionLocal()
    # Store raw data
    db_problem_raw = ProblemRaw(source=request.source, text=text, date=datetime.date.today())
    db.add(db_problem_raw)
    db.commit()

    # Simple text cleaning: remove extra whitespace
    cleaned_text = " ".join(text.split())

    # Store cleaned data
    db_problem_clean = ProblemClean(text_clean=cleaned_text)
    db.add(db_problem_clean)
    db.commit()
    db.close()

    return {"message": "Scraping successful"}

@app.get("/ideas")
def get_ideas():
    db = SessionLocal()
    # Retrieve all cleaned problems
    problems = db.query(ProblemClean).all()
    db.close()

    if not problems:
        return {"ideas": []}

    # Extract text for analysis
    texts = [problem.text_clean for problem in problems]

    # Analyze problems to get ideas
    analysis_results = analyze_problems(texts)

    # Here you would typically have more logic to rank ideas, etc.
    # For now, we'll just return the analysis.
    return {"ideas": analysis_results}

@app.get("/")
def read_root():
    return {"Hello": "World"}
