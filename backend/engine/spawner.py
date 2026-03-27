from sqlalchemy.orm import Session
from .. import models
import datetime

async def run_spawner(db: Session):
    log = models.EngineLog(level="info", source="Spawner", message="Agent Spawner (Gen-4) started")
    db.add(log)
    db.commit()

    agent_types = ["Research", "Builder", "Growth", "Support"]
    personalities = ["Efficient", "Creative", "Persistent", "Analytical", "Speedy"]

    existing_agents = db.query(models.Agent).all()
    if len(existing_agents) < len(agent_types):
        # Spawn missing agents
        for agent_type in agent_types:
            exists = db.query(models.Agent).filter(models.Agent.type == agent_type).first()
            if not exists:
                new_agent = models.Agent(
                    type=agent_type,
                    status="active",
                    personality=personalities[len(existing_agents) % len(personalities)],
                    last_run=datetime.datetime.now(datetime.timezone.utc)
                )
                db.add(new_agent)
                db.add(models.EngineLog(level="success", source="Spawner", message=f"Spawned new {agent_type} agent ({new_agent.personality})."))

    # Update last_run for active agents
    active_agents = db.query(models.Agent).filter(models.Agent.status == "active").all()
    for agent in active_agents:
        agent.last_run = datetime.datetime.now(datetime.timezone.utc)

    db.commit()
    db.add(models.EngineLog(level="info", source="Spawner", message="Spawner cycle complete. Agents are active."))
    db.commit()
    return {"active_agents": len(active_agents)}
