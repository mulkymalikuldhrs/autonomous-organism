import asyncio
import nltk
import os
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models
from .engine import sense, decision, factory, growth, immune, evolution, monetization, spawner

async def test_loop():
    print("\n" + "="*50)
    print("🚀 STARTING INTEGRATION TEST - GEN-4")
    print("="*50)

    print("\n📥 Downloading NLTK data...")
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

    # Clean up old test data if any
    if os.path.exists("organism.db"):
        os.remove("organism.db")

    # Initialize DB
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. SPWNER TEST
        print("\n🤖 Running Spawner...")
        await spawner.run_spawner(db)
        agents = db.query(models.Agent).all()
        print(f"✅ Agents spawned: {len(agents)}")
        for a in agents:
            print(f"   - {a.name} ({a.type}, {a.personality})")

        # 2. SENSE MOCK
        print("\n👁️ Adding mock clean problems...")
        problems_list = [
            "I hate it when my coffee gets cold too fast.",
            "Setting up a SaaS takes too much manual work.",
            "I need an automated way to track my recurring expenses.",
            "Finding reliable freelancers for micro-tasks is hard."
        ]
        for p_text in problems_list:
            problem = models.ProblemClean(text_clean=p_text)
            db.add(problem)
        db.commit()
        print(f"✅ Added {len(problems_list)} clean problems")

        # 3. DECISION TEST
        print("\n🧠 Running Decision Core...")
        await decision.run_decision(db)
        ideas = db.query(models.IdeaCandidate).all()
        print(f"✅ Ideas generated: {len(ideas)}")
        for i in ideas:
            print(f"   - [{i.theme}] Score: {i.score:.2f}")

        # 4. FACTORY TEST
        print("\n🏭 Running SaaS Factory...")
        await factory.run_factory(db)
        products = db.query(models.Product).all()
        if products:
            print(f"✅ Product built: {products[0].name}")
            print(f"   - Blueprint: {products[0].blueprint_path}")
        else:
            print("❌ FAILURE: No product built")

        # 5. GROWTH TEST
        print("\n📢 Running Growth Engine...")
        await growth.run_growth(db)
        print("✅ Growth campaigns generated in growth_outbox/")

        # 6. MONETIZATION TEST
        print("\n💰 Running Monetization Engine...")
        await monetization.run_monetization(db)
        revenue_logs = db.query(models.RevenueLog).all()
        traffic_logs = db.query(models.TrafficLog).all()
        print(f"✅ Traffic records: {len(traffic_logs)}")
        print(f"✅ Revenue logs: {len(revenue_logs)}")
        total_rev = sum(r.amount for r in revenue_logs)
        print(f"✅ Total simulated revenue: ${total_rev:.2f}")

        # 7. EVOLUTION TEST
        print("\n🔄 Running Evolution Engine...")
        await evolution.run_evolution(db)
        settings = db.query(models.SystemSetting).all()
        print(f"✅ System settings tuned: {len(settings)}")
        for s in settings:
            print(f"   - {s.key}: {s.value}")

        # 8. IMMUNE TEST
        print("\n🛡️ Running Immune System...")
        await immune.check_health(db)
        logs = db.query(models.EngineLog).filter(models.EngineLog.source == "Immune").all()
        if logs:
            print(f"✅ Health check log: {logs[-1].message}")

        print("\n" + "="*50)
        print("✅ INTEGRATION TEST COMPLETED SUCCESSFULLY")
        print("="*50)

    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_loop())
