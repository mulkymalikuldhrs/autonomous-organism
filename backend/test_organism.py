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
        # 1. Mock Sense
        problem = models.ProblemClean(text_clean="I hate it when my coffee gets cold too fast.")
        db.add(problem)
        db.commit()
        print("MOCK: Added clean problem")

        # 2. Decision
        print("Running Decision...")
        await decision.run_decision(db)
        idea = db.query(models.IdeaCandidate).first()
        if idea:
            print(f"SUCCESS: Idea generated: {idea.theme}")
        else:
            print("FAILURE: No idea generated")

        # 3. Factory
        print("Running Factory...")
        await factory.run_factory(db)
        product = db.query(models.Product).first()
        if product:
            print(f"SUCCESS: Product built: {product.name}")
        else:
            print("FAILURE: No product built")

        # 4. Spawner
        print("Running Spawner...")
        await spawner.run_spawner(db)
        agent = db.query(models.Agent).first()
        if agent:
            print(f"SUCCESS: Agent spawned: {agent.name}")
        else:
            print("FAILURE: No agent spawned")

        # 5. Growth
        print("Running Growth...")
        await growth.run_growth(db)

        # 6. Monetization
        print("Running Monetization...")
        await monetization.run_monetization(db)
        rev = db.query(models.RevenueLog).first()
        if rev:
            print(f"SUCCESS: Revenue generated: ${rev.amount}")
        else:
            print("FAILURE: No revenue generated")

        # 7. Evolution
        print("Running Evolution...")
        await evolution.run_evolution(db)

        # 8. Immune
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
