from sqlalchemy.orm import Session
from .. import models
import random
import datetime

AGENT_TYPES = ["Research", "Builder", "Growth", "Support"]
PERSONALITIES = ["Efficient", "Creative", "Persistent", "Analytical", "Speedy"]

async def run_spawner(db: Session):
    log = models.EngineLog(level="info", source="Spawner", message="Agent Spawner started (Gen-4)")
    db.add(log)
    db.commit()

    # 1. Self-Check existing agents
    active_agents = db.query(models.Agent).filter(models.Agent.status == "active").count()
    if active_agents < 4:
        # Spawn new agents
        for i in range(4 - active_agents):
            agent_type = random.choice(AGENT_TYPES)
            personality = random.choice(PERSONALITIES)
            name = f"{agent_type}-{personality}-{random.randint(100, 999)}"

            new_agent = models.Agent(
                type=agent_type,
                name=name,
                personality=personality,
                status="active"
            )
            db.add(new_agent)
            db.add(models.EngineLog(level="info", source="Spawner", message=f"Spawned new agent: {name} (Type: {agent_type}, Personality: {personality})"))

    # 2. Terminate weak/failed agents (simulated based on errors)
    # Check if we have agents that should be "terminated"
    # For now, let's keep it simple: 10% chance an agent retires/dies
    if random.random() < 0.1:
        weak_agent = db.query(models.Agent).filter(models.Agent.status == "active").first()
        if weak_agent:
            weak_agent.status = "terminated"
            db.add(models.EngineLog(level="danger", source="Spawner", message=f"Agent terminated: {weak_agent.name} (Retired due to burnout)"))

    db.commit()
