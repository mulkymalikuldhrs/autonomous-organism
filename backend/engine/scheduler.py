import asyncio
from sqlalchemy.orm import Session
from . import sense, decision, factory, growth, immune, evolution, monetization, spawner
from ..database import SessionLocal
import time

async def organism_loop():
    while True:
        db = SessionLocal()
        try:
            # 1. Sense - Find human problems
            await sense.run_sense(db)

            # 2. Decision - Choose and score best idea
            await decision.run_decision(db)

            # 3. Factory - Build MVP solution (Dockerized SaaS)
            await factory.run_factory(db)

            # 4. Spawner - Manage specialized sub-agents
            await spawner.run_spawner(db)

            # 5. Growth - Generate marketing campaigns
            await growth.run_growth(db)

            # 6. Monetization - Generate and track revenue
            await monetization.run_monetization(db)

            # 7. Evolution - Dynamic strategy adjustment
            await evolution.run_evolution(db)

            # 8. Immune - Health check and system protection
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
