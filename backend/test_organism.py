import asyncio
import os
import sys
from backend.engine.scheduler import Scheduler
from backend.engine.immune import ImmuneSystem
from backend.models import SessionLocal, EngineLog, ProblemRaw, IdeaCandidate, RevenueLog, Base, engine as db_engine

async def test_full_organism():
    print("🚀 STARTING FULL SYSTEM VERIFICATION")

    # 1. Initialize DB
    Base.metadata.create_all(bind=db_engine)

    # 2. Run Immune Check
    immune = ImmuneSystem()
    health = immune.check_health()
    print(f"   [IMMUNE] System healthy: {health}")

    # 3. Run Full Cycle
    sched = Scheduler()
    await sched.run_full_cycle()

    # 4. Verify Database Records
    db = SessionLocal()
    try:
        raw_count = db.query(ProblemRaw).count()
        idea_count = db.query(IdeaCandidate).count()
        rev_count = db.query(RevenueLog).count()
        log_count = db.query(EngineLog).count()

        print("\n" + "="*30)
        print("📊 VERIFICATION RESULTS")
        print("="*30)
        print(f"PROBLEMS SCANNED: {raw_count}")
        print(f"IDEAS GENERATED:  {idea_count}")
        print(f"PRODUCTS BUILT:   {len(os.listdir('products')) if os.path.exists('products') else 0}")
        print(f"REVENUE LOGS:     {rev_count}")
        print(f"SYSTEM LOGS:      {log_count}")

        if log_count > 0:
            print("✅ SYSTEM IS ALIVE AND RECORDING")
        else:
            print("❌ SYSTEM FAILED TO RECORD ACTIVITY")
            sys.exit(1)

    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_full_organism())
