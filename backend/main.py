from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from .database import get_db, SessionLocal, engine, Base
from .models import EngineRun, EngineLog, ProblemRaw, IdeaCandidate
from .engine.sense import run_sense
from .engine.decision import run_decision
from .engine.factory import run_factory
from .engine.growth import run_growth
from .engine.monetization import run_monetization
from .engine.immune import run_immune_check
from datetime import datetime
import asyncio
from fastapi.middleware.cors import CORSMiddleware

# Initialize DB
Base.metadata.create_all(bind=engine)

# Ensure NLTK data is available
import nltk
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

app = FastAPI(title="ORGANISME SAAS OTONOM")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
async def get_status(db: Session = Depends(get_db)):
    last_run = db.query(EngineRun).order_by(EngineRun.started_at.desc()).first()
    return {
        "status": "alive",
        "last_run": last_run,
        "version": "1.0.0-otonom"
    }

@app.get("/api/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    raw_count = db.query(ProblemRaw).count()
    idea_count = db.query(IdeaCandidate).count()
    return {
        "problemsScanned": raw_count,
        "ideasGenerated": idea_count,
        "revenue": 0,
        "generation": 1
    }

@app.get("/api/logs")
async def get_logs(db: Session = Depends(get_db)):
    logs = db.query(EngineLog).order_by(EngineLog.created_at.desc()).limit(50).all()
    return [
        {
            "id": l.id,
            "level": l.level,
            "source": l.source,
            "message": l.message,
            "created_at": l.created_at
        } for l in logs
    ]

@app.get("/api/ideas")
async def get_ideas(db: Session = Depends(get_db)):
    ideas = db.query(IdeaCandidate).order_by(IdeaCandidate.score.desc()).limit(10).all()
    return ideas

@app.post("/api/run/sense")
async def trigger_sense(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    run = EngineRun(engine="sense", status="running")
    db.add(run)
    db.commit()
    db.refresh(run)

    async def task():
        db_task = SessionLocal()
        try:
            await run_sense(db_task, run.id)
            r = db_task.query(EngineRun).get(run.id)
            r.status = "success"
            r.finished_at = datetime.now()
            db_task.commit()
        except Exception as e:
            r = db_task.query(EngineRun).get(run.id)
            r.status = "failed"
            r.meta = {"error": str(e)}
            db_task.commit()
        finally:
            db_task.close()

    background_tasks.add_task(task)
    return {"run_id": run.id, "status": "started"}

async def run_lifecycle_loop():
    """The Heartbeat of the Organism"""
    await asyncio.sleep(10) # wait for startup
    while True:
        print("Organism Heartbeat: Starting Lifecycle Cycle...")
        db = SessionLocal()
        try:
            # 1. Sense
            run_s = EngineRun(engine="sense", status="running")
            db.add(run_s)
            db.commit()
            db.refresh(run_s)
            await run_sense(db, run_s.id)
            run_s.status = "success"
            run_s.finished_at = datetime.now()
            db.commit()

            # 2. Decision
            run_d = EngineRun(engine="decision", status="running")
            db.add(run_d)
            db.commit()
            db.refresh(run_d)
            run_decision(db, run_d.id)
            run_d.status = "success"
            run_d.finished_at = datetime.now()
            db.commit()

            # 3. Factory
            run_f = EngineRun(engine="factory", status="running")
            db.add(run_f)
            db.commit()
            await run_factory(db, run_f.id)
            run_f.status = "success"
            run_f.finished_at = datetime.now()
            db.commit()

            # 4. Growth
            run_g = EngineRun(engine="growth", status="running")
            db.add(run_g)
            db.commit()
            run_growth(db, run_g.id)
            run_g.status = "success"
            run_g.finished_at = datetime.now()
            db.commit()

            # 5. Monetization
            run_m = EngineRun(engine="monetization", status="running")
            db.add(run_m)
            db.commit()
            run_monetization(db, run_m.id)
            run_m.status = "success"
            run_m.finished_at = datetime.now()
            db.commit()

            # 6. Immune System
            run_i = EngineRun(engine="system", status="running")
            db.add(run_i)
            db.commit()
            run_immune_check(db, run_i.id)
            run_i.status = "success"
            run_i.finished_at = datetime.now()
            db.commit()

            print("Lifecycle Cycle Complete.")
        except Exception as e:
            print(f"Lifecycle Error: {e}")
        finally:
            db.close()

        await asyncio.sleep(600) # every 10 minutes

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_lifecycle_loop())
