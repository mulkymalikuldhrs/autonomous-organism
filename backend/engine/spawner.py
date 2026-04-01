from sqlalchemy.orm import Session
from .. import models
import random
from datetime import datetime

AGENT_TYPES = ["Research", "Builder", "Growth", "Support"]
PERSONALITIES = ["Efficient", "Creative", "Persistent", "Analytical", "Speedy"]

async def run_spawner(db: Session):
    log_source = "Spawner"
    db.add(models.EngineLog(level="info", source=log_source, message="Agent Spawner active"))
    db.commit()

    # Ensure at least one agent of each type exists
    for t in AGENT_TYPES:
        existing = db.query(models.Agent).filter(models.Agent.type == t, models.Agent.status != "terminated").count()
        if existing == 0:
            personality = random.choice(PERSONALITIES)
            new_agent = models.Agent(
                type=t,
                status="active",
                personality=personality
            )
            db.add(new_agent)
            db.add(models.EngineLog(level="success", source=log_source, message=f"Spawned new {t} agent with {personality} personality"))

    # Randomly "refresh" or "terminate" weak agents (simulation of evolution)
    agents = db.query(models.Agent).filter(models.Agent.status == "active").all()
    for agent in agents:
        # 5% chance of an agent retiring/terminating
        if random.random() < 0.05:
            agent.status = "terminated"
            db.add(models.EngineLog(level="warning", source=log_source, message=f"Agent {agent.id} ({agent.type}) terminated."))

    db.commit()
