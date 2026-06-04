import os
from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import init_db, SessionLocal, Product, IdeaCandidate, ProblemRaw, LifeLog, SystemSetting
from .engine.scheduler import orchestrate_cycle, start_scheduler
import uvicorn
import nltk

def setup_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')

app = FastAPI(title="Autonomous Organism Gen-4.1 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    setup_nltk()
    init_db()
    start_scheduler()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/health")
def health():
    return {"status": "online", "generation": "4.1"}

@app.get("/api/metrics")
def get_metrics(db: Session = Depends(get_db)):
    problems_count = db.query(ProblemRaw).count()
    ideas_count = db.query(IdeaCandidate).count()
    products_count = db.query(Product).filter(Product.status != "killed").count()
    total_revenue = db.query(Product).with_entities(Product.revenue).all()
    revenue_sum = sum([r[0] for r in total_revenue]) if total_revenue else 0

    return {
        "problemsScanned": problems_count,
        "ideasGenerated": ideas_count,
        "productsBuilt": products_count,
        "revenue": revenue_sum,
        "generation": 4.1
    }

@app.get("/api/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(LifeLog).order_by(LifeLog.created_at.desc()).limit(100).all()
    return logs

@app.post("/api/engine/run/{engine_name}")
def run_engine(engine_name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(orchestrate_cycle)
    return {"message": f"Global engine cycle triggered via {engine_name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
