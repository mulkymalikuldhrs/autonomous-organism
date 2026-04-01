import asyncio
import nltk
from .database import SessionLocal, engine
from . import models
from .engine import sense, decision, factory, growth, immune, evolution, spawner, monetization

async def test_loop():
    print("Downloading NLTK data...")
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

    print("Starting full Gen-4 integration test...")
    # Initialize DB
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Mocking problem data
        problem = models.ProblemClean(text_clean="Managing complex SaaS subscriptions is a nightmare.")
        db.add(problem)
        db.commit()
        print("MOCK: Added clean problem")

        # 1. Spawner
        print("Running Spawner...")
        await spawner.run_spawner(db)
        agents = db.query(models.Agent).all()
        print(f"SUCCESS: {len(agents)} agents spawned.")

        # 2. Decision
        print("Running Decision...")
        await decision.run_decision(db)
        idea = db.query(models.IdeaCandidate).first()
        if idea:
            print(f"SUCCESS: Idea generated: {idea.theme}")

        # 3. Factory
        print("Running Factory...")
        await factory.run_factory(db)
        product = db.query(models.Product).first()
        if product:
            print(f"SUCCESS: Product built: {product.name}")

        # 4. Growth
        print("Running Growth...")
        await growth.run_growth(db)
        print("SUCCESS: Growth campaign generated.")

        # 5. Monetization
        print("Running Monetization...")
        # Add some traffic for simulation
        traffic = models.TrafficLog(product_id=product.id, clicks=100, signups=10)
        db.add(traffic)
        db.commit()
        await monetization.run_monetization(db)
        rev = db.query(models.RevenueLog).first()
        if rev:
            print(f"SUCCESS: Revenue generated: ${rev.amount:.2f}")

        # 6. Evolution
        print("Running Evolution...")
        await evolution.run_evolution(db)
        print("SUCCESS: Evolution weights updated.")

        # 7. Immune
        print("Running Immune...")
        await immune.check_health(db)
        print("SUCCESS: Health check passed.")

        print("\n=== GEN-4 INTEGRATION TEST COMPLETED SUCCESSFULLY ===")

    except Exception as e:
        print(f"Integration test FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_loop())
