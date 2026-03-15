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

    print("Starting integration test...")
    # Initialize DB
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # We won't actually run Sense because it uses Playwright and might be slow/flaky in tests
        # But we can test the other parts with mock data

        # Add a clean problem
        problem = models.ProblemClean(text_clean="I hate it when my coffee gets cold too fast.")
        db.add(problem)
        db.commit()
        print("MOCK: Added clean problem")

        # Run Decision
        print("Running Decision...")
        await decision.run_decision(db)

        # Check if idea was generated
        idea = db.query(models.IdeaCandidate).first()
        if idea:
            print(f"SUCCESS: Idea generated: {idea.theme}")
        else:
            print("FAILURE: No idea generated")

        # Run Factory
        print("Running Factory...")
        await factory.run_factory(db)

        # Check if product was built
        product = db.query(models.Product).first()
        if product:
            print(f"SUCCESS: Product built: {product.name}")
        else:
            print("FAILURE: No product built")

        # Run Spawner
        print("Running Spawner...")
        await spawner.run_spawner(db)

        # Run Growth
        print("Running Growth...")
        await growth.run_growth(db)

        # Run Monetization
        print("Running Monetization...")
        await monetization.run_monetization(db)

        # Run Evolution
        print("Running Evolution...")
        await evolution.run_evolution(db)

        # Run Immune
        print("Running Immune...")
        await immune.check_health(db)

        print("Integration test completed successfully.")

    except Exception as e:
        print(f"Integration test FAILED: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_loop())
