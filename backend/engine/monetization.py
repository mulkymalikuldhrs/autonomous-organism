from sqlalchemy.orm import Session
from ..models import EngineLog
import random

def run_monetization(db: Session, run_id: int):
    log = EngineLog(run_id=run_id, level="info", source="MONETIZATION", message="Monetization Engine: Analyzing conversion and revenue...")
    db.add(log)
    db.commit()

    # In a real scenario, this would check Stripe or Affiliate dashboards
    revenue = random.uniform(0, 100) if random.random() > 0.7 else 0

    if revenue > 0:
        log = EngineLog(run_id=run_id, level="success", source="MONETIZATION", message=f"Generated ${revenue:.2f} in passive income this cycle.")
    else:
        log = EngineLog(run_id=run_id, level="info", source="MONETIZATION", message="No sales detected. Re-evaluating CTA placement.")

    db.add(log)
    db.commit()
    return revenue
