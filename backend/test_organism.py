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

    print("Starting full lifecycle integration test...")
    # Initialize DB
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Sense (Mocked data for stability)
        print("Stage 1: Sense (Mocking clean problem)")
        problem = models.ProblemClean(text_clean="I hate it when my coffee gets cold too fast.")
        db.add(problem)
        db.commit()

        # 2. Decision
        print("Stage 2: Decision...")
        await decision.run_decision(db)
        idea = db.query(models.IdeaCandidate).first()
        if idea: print(f"  - Idea generated: {idea.theme}")

        # 3. Factory
        print("Stage 3: Factory...")
        await factory.run_factory(db)
        product = db.query(models.Product).first()
        if product: print(f"  - Product built: {product.name}")

        # 4. Spawner
        print("Stage 4: Spawner...")
        await spawner.run_spawner(db)
        agent_count = db.query(models.Agent).count()
        print(f"  - Agents spawned: {agent_count}")

        # 5. Growth
        print("Stage 5: Growth...")
        await growth.run_growth(db)
        print("  - Growth campaigns generated")

        # 6. Monetization
        print("Stage 6: Monetization...")
        # Add some mock traffic first
        if product:
            traffic = models.TrafficLog(product_id=product.id, channel="Twitter", clicks=150)
            db.add(traffic)
            db.commit()
        await monetization.run_monetization(db)
        revenue = db.query(models.RevenueLog).first()
        if revenue: print(f"  - Revenue generated: {revenue.amount} {revenue.currency}")

        # 7. Evolution
        print("Stage 7: Evolution...")
        await evolution.run_evolution(db)
        print("  - Evolution cycle complete")

        # 8. Immune
        print("Stage 8: Immune...")
        await immune.check_health(db)
        print("  - Health check complete")

        print("\n✅ FULL LIFECYCLE TEST COMPLETED SUCCESSFULLY.")

    except Exception as e:
        print(f"❌ Integration test FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_loop())
