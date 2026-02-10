from sqlalchemy.orm import Session
from ..models import EngineLog
import random
import os
from datetime import datetime

def run_growth(db: Session, run_id: int):
    log = EngineLog(run_id=run_id, level="info", source="GROWTH", message="Growth Engine: Spreading awareness to human digital habitats...")
    db.add(log)
    db.commit()

    # Simulate real channel interaction by writing to a distribution log
    channels = ["reddit_posts.txt", "medium_drafts.txt", "twitter_queue.txt"]
    channel = random.choice(channels)

    activity = f"Automated promotional content for the latest SaaS organism. Timestamp: {datetime.now().isoformat()}"

    os.makedirs("growth_outbox", exist_ok=True)
    with open(f"growth_outbox/{channel}", "a") as f:
        f.write(f"\n--- RUN {run_id} ---\n{activity}\n")

    log = EngineLog(run_id=run_id, level="success", source="GROWTH", message=f"Growth activity committed to outbox: {channel}")
    db.add(log)
    db.commit()
    return True
