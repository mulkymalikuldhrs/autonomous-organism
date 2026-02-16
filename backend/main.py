from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import nltk
import asyncio
import os

# NLTK Download FIRST
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except Exception as e:
    print(f"NLTK download error: {e}")

from . import models, database
from .database import engine, get_db, SessionLocal
from .engine import sense, decision, factory, growth, scheduler

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ORGANISME SAAS OTONOM API")

async def run_sense_task():
    db = SessionLocal()
    try:
        await sense.run_sense(db)
    finally:
        db.close()

async def run_decision_task():
    db = SessionLocal()
    try:
        await decision.run_decision(db)
    finally:
        db.close()

async def run_factory_task():
    db = SessionLocal()
    try:
        await factory.run_factory(db)
    finally:
        db.close()

async def run_growth_task():
    db = SessionLocal()
    try:
        await growth.run_growth(db)
    finally:
        db.close()

@app.get("/api/metrics")
def get_metrics(db: Session = Depends(get_db)):
    problems_scanned = db.query(models.ProblemRaw).count()
    ideas_generated = db.query(models.IdeaCandidate).count()

    # Count products recursively or just the directories in products/
    products_count = 0
    if os.path.exists("products"):
        # Each product is now a directory
        products_count = len([d for d in os.listdir("products") if os.path.isdir(os.path.join("products", d))])

    # Revenue can be summed from models.RevenueLog if implemented
    revenue = 0.0
    # Try to sum revenue if table exists
    try:
        revenue = db.query(models.RevenueLog.amount).sum() or 0.0
    except:
        pass

    return {
        "problemsScanned": problems_scanned,
        "ideasGenerated": ideas_generated,
        "productsBuilt": products_count,
        "revenue": float(revenue),
        "generation": 1,
        "status": "healthy"
    }

@app.get("/api/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(models.EngineLog).order_by(models.EngineLog.created_at.desc()).limit(100).all()
    return [
        {
            "id": l.id,
            "level": l.level,
            "source": l.source,
            "message": l.message,
            "created_at": l.created_at.isoformat()
        } for l in logs
    ]

@app.post("/api/run-sense")
async def run_sense_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_sense_task)
    return {"message": "Sense engine started in background"}

@app.post("/api/run-decision")
async def run_decision_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_decision_task)
    return {"message": "Decision engine started in background"}

@app.post("/api/run-factory")
async def run_factory_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_factory_task)
    return {"message": "SaaS Factory started in background"}

@app.post("/api/run-growth")
async def run_growth_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_growth_task)
    return {"message": "Growth engine started in background"}

@app.on_event("startup")
async def startup_event():
    # Start the autonomous life loop
    asyncio.create_task(scheduler.organism_loop())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
