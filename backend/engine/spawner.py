from sqlalchemy.orm import Session
from .. import models
import random
import datetime

AGENT_TYPES = ["Research", "Builder", "Growth", "Support"]
PERSONALITIES = ["Efficient", "Creative", "Persistent", "Analytical", "Speedy"]

async def run_spawner(db: Session):
    log = models.EngineLog(level="info", source="Spawner", message="Agent Spawner started")
    db.add(log)
    db.commit()

    # 1. Evaluate current agents
    active_agents = db.query(models.Agent).filter(models.Agent.status == "active").all()

    # 2. Spawn new agents if needed (maintain a core set)
    if len(active_agents) < 4:
        # Spawn missing types
        existing_types = [a.type for a in active_agents]
        for t in AGENT_TYPES:
            if t not in existing_types:
                new_agent = models.Agent(
                    type=t,
                    status="active",
                    personality=random.choice(PERSONALITIES)
                )
                db.add(new_agent)
                db.add(models.EngineLog(level="success", source="Spawner", message=f"Spawned new {t} agent (Personality: {new_agent.personality})"))

    # 3. Terminate underperforming or old agents (simulation)
    # In a real scenario, this would be based on task success rates
    for agent in active_agents:
        if random.random() < 0.05: # 5% chance of retirement each cycle
            agent.status = "terminated"
            db.add(models.EngineLog(level="warning", source="Spawner", message=f"Terminated {agent.type} agent due to planned lifecycle retirement."))

    db.commit()
