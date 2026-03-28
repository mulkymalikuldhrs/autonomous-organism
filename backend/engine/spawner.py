from sqlalchemy.orm import Session
from .. import models
import datetime
import random

AGENT_TYPES = ["Research", "Builder", "Growth", "Support"]
PERSONALITIES = ["Efficient", "Creative", "Persistent", "Analytical", "Speedy"]

async def run_spawner(db: Session):
    log = models.EngineLog(level="info", source="Spawner", message="Agent Spawner active (Gen-4 Personality Mode)")
    db.add(log)
    db.commit()

    # Check current agents
    active_count = db.query(models.Agent).filter(models.Agent.status == "active").count()

    if active_count < 4:
        # Spawn missing agents
        existing_types = [a.type for a in db.query(models.Agent).filter(models.Agent.status == "active").all()]
        for atype in AGENT_TYPES:
            if atype not in existing_types:
                personality = random.choice(PERSONALITIES)
                new_agent = models.Agent(
                    name=f"{atype}-{random.randint(100, 999)}",
                    type=atype,
                    status="active",
                    personality=personality,
                    last_run=datetime.datetime.now(datetime.timezone.utc)
                )
                db.add(new_agent)
                db.add(models.EngineLog(level="info", source="Spawner", message=f"Spawned new {atype} agent with {personality} personality."))

    db.commit()
    return {"status": "checked", "active": active_count}
