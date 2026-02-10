from sqlalchemy.orm import Session
from ..models import EngineLog, EngineRun

def run_immune_check(db: Session, run_id: int):
    log = EngineLog(run_id=run_id, level="system", source="IMMUNE", message="Immune System: Performing self-diagnostic...")
    db.add(log)
    db.commit()

    # Check for failure clusters
    recent_runs = db.query(EngineRun).order_by(EngineRun.started_at.desc()).limit(10).all()
    failed_count = sum(1 for r in recent_runs if r.status == 'failed')

    if failed_count > 5:
        log = EngineLog(run_id=run_id, level="error", source="IMMUNE", message="System Instability Detected. Emergency isolation protocol active.")
        db.add(log)
        db.commit()
        return False

    log = EngineLog(run_id=run_id, level="success", source="IMMUNE", message="Organism health verified. No pathogens found.")
    db.add(log)
    db.commit()
    return True
