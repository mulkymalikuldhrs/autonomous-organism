import asyncio
import nltk
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models
from .engine import sense, decision, factory, growth, immune, evolution, spawner, monetization

async def test_loop():
    print("Downloading NLTK data...")
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

    print("Starting integration test (Gen-4 Complete)...")
    # Initialize DB
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Add a clean problem
        problem = models.ProblemClean(text_clean="I hate it when my coffee gets cold too fast. Need an auto-warming mug app.")
        db.add(problem)
        db.commit()
        print("MOCK: Added clean problem")

        # 1. Decision
        print("Running Decision...")
        await decision.run_decision(db)
        idea = db.query(models.IdeaCandidate).first()
        if idea:
            print(f"SUCCESS: Idea generated: {idea.theme}")
        else:
            print("FAILURE: No idea generated")

        # 2. Factory
        print("Running Factory...")
        await factory.run_factory(db)
        product = db.query(models.Product).first()
        if product:
            print(f"SUCCESS: Product built: {product.name}")
        else:
            print("FAILURE: No product built")

        # 3. Spawner
        print("Running Spawner...")
        await spawner.run_spawner(db)
        agents = db.query(models.Agent).count()
        print(f"SUCCESS: {agents} agents spawned")

        # 4. Growth
        print("Running Growth...")
        await growth.run_growth(db)

        # 5. Monetization (MOCK TRAFFIC FIRST)
        print("Running Monetization...")
        traffic = models.TrafficLog(product_id=product.id, clicks=100, channel="Twitter")
        db.add(traffic)
        db.commit()
        await monetization.run_monetization(db)
        revenue = db.query(models.RevenueLog).first()
        if revenue:
            print(f"SUCCESS: Revenue recorded: ${revenue.amount}")
        else:
            print("FAILURE: No revenue recorded")

        # 6. Evolution
        print("Running Evolution...")
        await evolution.run_evolution(db)

        # 7. Immune
        print("Running Immune...")
        await immune.check_health(db)

        print("Integration test completed successfully.")

    except Exception as e:
        print(f"Integration test FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_loop())
