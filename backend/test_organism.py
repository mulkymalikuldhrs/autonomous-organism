import asyncio
import nltk
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models
from .engine import sense, decision, factory, growth, immune, evolution, spawner, monetization

async def test_loop():
    print("Downloading NLTK data...")
    try:
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except Exception as e:
        print(f"NLTK download error (safe to ignore if already present): {e}")

    print("Starting integration test...")
    # Initialize DB (reset for test)
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Step 1: Sense (Simulated Problem Ingestion)
        problem = models.ProblemClean(text_clean="Human needs a way to track autonomous organisms.")
        db.add(problem)
        db.commit()
        print("STAGE 1: [Sense] MOCK problem added")

        # Step 2: Decision
        print("STAGE 2: [Decision] Running Decision Core...")
        await decision.run_decision(db)
        idea = db.query(models.IdeaCandidate).first()
        if idea:
            print(f"SUCCESS: Idea generated: {idea.theme} (Score: {idea.score:.2f})")
        else:
            raise Exception("FAILURE: No idea generated")

        # Step 3: Factory
        print("STAGE 3: [Factory] Running SaaS Factory...")
        await factory.run_factory(db)
        product = db.query(models.Product).first()
        if product:
            print(f"SUCCESS: Product built: {product.name}")
        else:
            raise Exception("FAILURE: No product built")

        # Step 4: Spawner
        print("STAGE 4: [Spawner] Running Agent Spawner...")
        await spawner.run_spawner(db)
        agents_count = db.query(models.Agent).count()
        print(f"SUCCESS: {agents_count} agents spawned")

        # Step 5: Growth
        print("STAGE 5: [Growth] Running Growth Engine...")
        await growth.run_growth(db)
        print("SUCCESS: Growth campaigns generated")

        # Step 6: Monetization
        print("STAGE 6: [Monetization] Running Monetization Engine...")
        await monetization.run_monetization(db)
        revenue_count = db.query(models.RevenueLog).count()
        print(f"SUCCESS: {revenue_count} revenue logs recorded")

        # Step 7: Evolution
        print("STAGE 7: [Evolution] Running Evolution Engine...")
        await evolution.run_evolution(db)
        print("SUCCESS: Evolution cycle complete")

        # Step 8: Immune
        print("STAGE 8: [Immune] Running Immune System Check...")
        await immune.check_health(db)
        print("SUCCESS: Immune system check complete")

        print("\nFULL INTEGRATION TEST PASSED!")
        print(f"IDEAS GENERATED: {db.query(models.IdeaCandidate).count()}")
        print(f"PRODUCTS BUILT: {db.query(models.Product).count()}")
        print(f"AGENTS ACTIVE: {db.query(models.Agent).filter(models.Agent.status == 'active').count()}")
        print(f"REVENUE LOGS: {revenue_count}")

    except Exception as e:
        print(f"INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_loop())
