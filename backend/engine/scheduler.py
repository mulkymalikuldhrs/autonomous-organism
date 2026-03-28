import asyncio
from sqlalchemy.orm import Session
from . import sense, decision, factory, growth, immune, evolution, spawner
from ..database import SessionLocal
import time

async def organism_loop():
    while True:
        db = SessionLocal()
        try:
            # 1. Sense - Collect problems
            await sense.run_sense(db)

            # 2. Decision - Filter and pick best ideas
            await decision.run_decision(db)

            # 3. Factory - Generate full product structure
            await factory.run_factory(db)

            # 4. Spawner - Manage specialized sub-agents
            await spawner.run_spawner(db)

            # 5. Growth - Execute marketing and traffic generation
            await growth.run_growth(db)

            # 6. Evolution - Tune system settings and weights
            await evolution.run_evolution(db)

            # 7. Immune - Run health checks and resource management
            await immune.check_health(db)

        except Exception as e:
            print(f"Loop error: {e}")
        finally:
            db.close()

        # Sleep for 1 hour (or less for testing)
        await asyncio.sleep(3600)

def start_scheduler():
    # This should be called from main.py startup
    asyncio.create_task(organism_loop())
