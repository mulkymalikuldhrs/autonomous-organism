from sqlalchemy.orm import Session
from .. import models
import datetime
import random

AGENT_TYPES = ["Research", "Builder", "Growth", "Support"]

async def run_spawner(db: Session):
    log = models.EngineLog(level="info", source="Spawner", message="Agent Spawner started")
    db.add(log)
    db.commit()

    # 1. Check if new products need specialized agents
    products_without_agents = db.query(models.Product).filter(~models.Product.id.in_(
        db.query(models.Agent.product_id).filter(models.Agent.product_id != None)
    )).all()

    spawn_count = 0
    for product in products_without_agents:
        # Spawn a Growth agent for every new product
        agent_name = f"Agent-{product.name[:5]}-{random.randint(100, 999)}"
        new_agent = models.Agent(
            name=agent_name,
            type="Growth",
            status="active",
            product_id=product.id
        )
        db.add(new_agent)
        spawn_count += 1
        db.add(models.EngineLog(level="success", source="Spawner", message=f"Spawned specialized Growth agent: {agent_name} for {product.name}"))

    # 2. Kill "boros" (wasteful) or inactive agents
    # Simulation: kill agents older than 30 days if they haven't produced revenue
    # (Actually we just log the policy for now)

    db.commit()
    db.add(models.EngineLog(level="info", source="Spawner", message=f"Spawner cycle complete. Spawned {spawn_count} agents."))
    db.commit()

async def spawn_standalone_agent(db: Session, agent_type: str):
    agent_name = f"Autonomous-{agent_type}-{random.randint(1000, 9999)}"
    new_agent = models.Agent(
        name=agent_name,
        type=agent_type,
        status="active"
    )
    db.add(new_agent)
    db.add(models.EngineLog(level="info", source="Spawner", message=f"Spawned standalone {agent_type} agent: {agent_name}"))
    db.commit()
    return new_agent
