import asyncio
from sqlalchemy.orm import Session
from . import sense, decision, factory, growth, immune, evolution, monetization, spawner
from ..database import SessionLocal
import time

async def organism_loop():
    while True:
        db = SessionLocal()
        try:
            # 1. Sense - Find problems
            await sense.run_sense(db)

            # 2. Decision - Choose best problem
            await decision.run_decision(db)

            # 3. Factory - Build solutions
            await factory.run_factory(db)

            # 4. Spawner - Manage agents
            await spawner.run_spawner(db)

            # 5. Growth - Find users
            await growth.run_growth(db)

            # 6. Monetization - Generate revenue
            await monetization.run_monetization(db)

            # 7. Evolution - Learn and upgrade
            await evolution.run_evolution(db)

            # 8. Immune - Maintain health
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
