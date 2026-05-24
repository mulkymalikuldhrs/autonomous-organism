from sqlalchemy.orm import Session
from .. import models
import random
import datetime

AGENT_TYPES = ["Research", "Builder", "Growth", "Support"]
PERSONALITIES = ["Efficient", "Creative", "Persistent", "Analytical", "Speedy"]

async def run_spawner(db: Session):
    log = models.EngineLog(level="info", source="Spawner", message="Agent Spawner engine started")
    db.add(log)
    db.commit()

    # Ensure at least one agent of each type exists
    for agent_type in AGENT_TYPES:
        active_count = db.query(models.Agent).filter(
            models.Agent.agent_type == agent_type,
            models.Agent.status == "active"
        ).count()

        if active_count == 0:
            personality = random.choice(PERSONALITIES)
            new_agent = models.Agent(
                agent_type=agent_type,
                status="active",
                personality=personality
            )
            db.add(new_agent)
            db.add(models.EngineLog(level="success", source="Spawner", message=f"Spawned new {agent_type} agent with {personality} personality"))

    # Cleanup logic for 'boros' (inefficient) or looping agents could go here
    # For now, just mark last_run
    active_agents = db.query(models.Agent).filter(models.Agent.status == "active").all()
    for agent in active_agents:
        agent.last_run = datetime.datetime.now(datetime.timezone.utc)

    db.commit()
