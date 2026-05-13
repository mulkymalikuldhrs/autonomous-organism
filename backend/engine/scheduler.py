import asyncio
import time
from .sense import SenseEngine
from .decision import DecisionCore
from .factory import SaasFactory
from .growth import GrowthEngine
from .monetization import MonetizationEngine
from ..models import SessionLocal, EngineLog, SystemSetting, Base, engine as db_engine

class Scheduler:
    def __init__(self):
        self.sense = SenseEngine()
        self.decision = DecisionCore()
        self.factory = SaasFactory()
        self.growth = GrowthEngine()
        self.monetization = MonetizationEngine()

    async def run_full_cycle(self):
        print("\n" + "🌀"*25)
        print("🧬 ORGANISME ALPHA GEN-4.1 - FULL CYCLE STARTING")
        print("🌀"*25)

        db = SessionLocal()
        try:
            # Check throttle from Immune System
            throttle = db.query(SystemSetting).filter(SystemSetting.key == "system_throttle").first()
            if throttle and throttle.value == "true":
                print("   🛡️ SYSTEM THROTTLED BY IMMUNE SYSTEM. SLEEPING.")
                await asyncio.sleep(600)
                return

            # 1. Sense
            await self.sense.run()

            # 2. Decision
            await self.decision.run()

            # 3. Factory
            await self.factory.run()

            # 4. Growth
            traffic = await self.growth.run()

            # 5. Monetization
            await self.monetization.run(traffic=traffic)

            print("\n" + "✅"*25)
            print("🧬 FULL CYCLE COMPLETE")
            print("✅"*25)

        except Exception as e:
            print(f"🔥 SCHEDULER FATAL ERROR: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    sched = Scheduler()
    asyncio.run(sched.run_full_cycle())
