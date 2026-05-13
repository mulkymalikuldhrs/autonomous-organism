import os
import time
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models
from .models import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ORGANISME-ALPHA GEN-4.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ALIVE", "version": "4.1", "timestamp": time.time()}

@app.get("/api/metrics")
def get_metrics(db: Session = Depends(get_db)):
    problems_count = db.query(models.ProblemRaw).count()
    ideas_count = db.query(models.IdeaCandidate).count()
    # Mocking revenue for now until monetization engine is fully wired
    revenue = db.query(models.RevenueLog).with_entities(models.RevenueLog.amount).all()
    total_revenue = sum([r[0] for r in revenue])

    return {
        "problemsScanned": problems_count,
        "ideasGenerated": ideas_count,
        "revenue": total_revenue,
        "generation": 4.1
    }

@app.get("/api/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(models.EngineLog).order_by(models.EngineLog.created_at.desc()).limit(100).all()
    return logs

@app.post("/api/run/sense")
def trigger_sense():
    # This will be handled by the scheduler or manual trigger
    return {"message": "Sense engine triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
