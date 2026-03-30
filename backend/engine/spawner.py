from sqlalchemy.orm import Session
from .. import models
import random
import datetime

AGENT_TYPES = ["Research", "Builder", "Growth", "Support"]
PERSONALITIES = ["Efficient", "Creative", "Persistent", "Analytical", "Speedy"]

async def run_spawner(db: Session):
    log = models.EngineLog(level="info", source="Spawner", message="Agent Spawner engine started (Gen-4)")
    db.add(log)
    db.commit()

    # 1. Check existing agents
    agents = db.query(models.Agent).all()

    # 2. Ensure we have at least one of each core type
    spawned_count = 0
    for t in AGENT_TYPES:
        exists = any(a.type == t and a.status != "terminated" for a in agents)
        if not exists:
            new_agent = models.Agent(
                type=t,
                status="active",
                personality=random.choice(PERSONALITIES)
            )
            db.add(new_agent)
            spawned_count += 1
            db.add(models.EngineLog(level="success", source="Spawner", message=f"Spawned new {t} Agent ({new_agent.personality} trait)"))

    # 3. Simulate agent activity update
    for agent in agents:
        if agent.status == "active":
            agent.last_run = datetime.datetime.now(datetime.timezone.utc)

    db.add(models.EngineLog(level="info", source="Spawner", message=f"Spawner cycle complete. New agents: {spawned_count}"))
    db.commit()
    return spawned_count
