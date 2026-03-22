import asyncio
from sqlalchemy.orm import Session
from . import sense, decision, factory, growth, immune, evolution, monetization, spawner
from ..database import SessionLocal
import time

async def organism_loop():
    while True:
        db = SessionLocal()
        try:
            # 1. Sense
            await sense.run_sense(db)

            # 2. Decision
            await decision.run_decision(db)

            # 3. Factory
            await factory.run_factory(db)

            # 4. Spawner (New)
            await spawner.run_spawner(db)

            # 5. Growth
            await growth.run_growth(db)

            # 6. Monetization (New)
            await monetization.run_monetization(db)

            # 7. Evolution
            await evolution.run_evolution(db)

            # 8. Immune
            await immune.check_health(db)

        except Exception as e:
            print(f"Loop error: {e}")
        finally:
            db.close()

        # Sleep for 1 hour (or less for testing)
        # For Gen-4, we can set it to 3600, but for immediate activity, maybe 1800
        await asyncio.sleep(3600)

def start_scheduler():
    # This should be called from main.py startup
    asyncio.create_task(organism_loop())
