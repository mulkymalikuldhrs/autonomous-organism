from sqlalchemy.orm import Session
from .. import models
import random
import datetime

AGENT_TYPES = ["Research", "Builder", "Growth", "Support"]
TRAITS = ["Efficient", "Creative", "Persistent", "Analytical"]

async def run_spawner(db: Session):
    log = models.EngineLog(level="info", source="Spawner", message="Agent Spawner started")
    db.add(log)
    db.commit()

    # Ensure we have at least one of each agent type
    for agent_type in AGENT_TYPES:
        exists = db.query(models.Agent).filter(models.Agent.type == agent_type, models.Agent.status == "active").first()
        if not exists:
            new_agent = models.Agent(
                name=f"{agent_type}Agent-{random.randint(100, 999)}",
                type=agent_type,
                status="active",
                personality=random.choice(TRAITS)
            )
            db.add(new_agent)
            db.add(models.EngineLog(level="info", source="Spawner", message=f"Spawned new {agent_type} agent: {new_agent.name}"))

    # Immune system for agents: Terminate if "boros" (simulated by random check for now)
    active_agents = db.query(models.Agent).filter(models.Agent.status == "active").all()
    for agent in active_agents:
        if random.random() < 0.05: # 5% chance of retirement/failure
            agent.status = "terminated"
            db.add(models.EngineLog(level="warning", source="Spawner", message=f"Agent {agent.name} has been terminated (Lifecycle complete)"))

    db.commit()
