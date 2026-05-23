import asyncio
from sqlalchemy.orm import Session
from . import sense, decision, factory, growth, immune, evolution, spawner, monetization
from ..database import SessionLocal
import time

async def organism_loop():
    while True:
        db = SessionLocal()
        try:
            from .. import models
            # Check if system is still active
            active_setting = db.query(models.SystemSetting).filter(models.SystemSetting.key == "system_active").first()
            if active_setting and active_setting.value == 0.0:
                print("Organism termination triggered via system_active setting.")
                db.add(models.EngineLog(level="danger", source="System", message="Organism is terminating as requested."))
                db.commit()
                break

            # 1. Sense - Scan Problems
            await sense.run_sense(db)

            # 2. Decision - Choose Best Problem
            await decision.run_decision(db)

            # 3. Factory - Build Solution
            await factory.run_factory(db)

            # 4. Spawner - Manage Agents
            await spawner.run_spawner(db)

            # 5. Growth - Find Users
            await growth.run_growth(db)

            # 6. Monetization - Generate Revenue
            await monetization.run_monetization(db)

            # 7. Evolution - Self Upgrade
            await evolution.run_evolution(db)

            # 8. Immune - Health Check
            await immune.check_health(db)

        except Exception as e:
            print(f"Loop error: {e}")
        finally:
            db.close()

        # Cycle once per hour
        await asyncio.sleep(3600)

def start_scheduler():
    # This is called from main.py startup lifespan
    asyncio.create_task(organism_loop())
