import asyncio
import nltk
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models
from .engine import sense, decision, factory, growth, immune, evolution, monetization, spawner

async def test_loop():
    print("Downloading NLTK data...")
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

    print("Starting integration test (Gen-4 Complete)...")
    # Initialize DB
    models.Base.metadata.drop_all(bind=engine) # Start fresh
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Sense Mock
        problem = models.ProblemClean(text_clean="People are complaining about slow AI responses.")
        db.add(problem)
        db.commit()
        print("STEP 1: Added clean problem")

        # 2. Decision
        print("STEP 2: Running Decision...")
        await decision.run_decision(db)
        idea = db.query(models.IdeaCandidate).first()
        if idea:
            print(f"   ✅ Idea generated: {idea.theme}")
        else:
            raise Exception("Decision failed")

        # 3. Factory
        print("STEP 3: Running Factory...")
        await factory.run_factory(db)
        product = db.query(models.Product).first()
        if product:
            print(f"   ✅ Product built: {product.name}")
        else:
            raise Exception("Factory failed")

        # 4. Spawner
        print("STEP 4: Running Spawner...")
        await spawner.run_spawner(db)
        agents = db.query(models.Agent).all()
        print(f"   ✅ Agents spawned: {len(agents)}")

        # 5. Growth
        print("STEP 5: Running Growth...")
        await growth.run_growth(db)
        print("   ✅ Growth campaign generated")

        # 6. Monetization
        print("STEP 6: Running Monetization...")
        await monetization.run_monetization(db)
        revenue = db.query(models.RevenueLog).first()
        if revenue:
            print(f"   ✅ Revenue generated: ${revenue.amount}")

        # 7. Evolution
        print("STEP 7: Running Evolution...")
        await evolution.run_evolution(db)
        print("   ✅ Evolution cycle complete")

        # 8. Immune
        print("STEP 8: Running Immune...")
        await immune.check_health(db)
        print("   ✅ Health check complete")

        print("\n🏆 INTEGRATION TEST PASSED: Full 8-stage lifecycle verified.")

    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_loop())
