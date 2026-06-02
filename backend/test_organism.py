import os
import sys
from backend.database import init_db, SessionLocal, ProblemRaw, IdeaCandidate, Product, LifeLog
from backend.engine.scheduler import orchestrate_cycle

def test_full_cycle():
    print("Testing Autonomous Cycle Gen-4.1...")
    if os.path.exists("organism.db"):
        os.remove("organism.db")
    init_db()

    db = SessionLocal()
    # Add a seed problem
    db.add(ProblemRaw(
        source="Test",
        external_id="test_001",
        title="Manual Test Problem",
        content="Testing the autonomous pipeline with a dummy problem.",
        url="http://test.com"
    ))
    db.commit()
    db.close()

    print("Running cycle...")
    orchestrate_cycle()

    db = SessionLocal()
    problems = db.query(ProblemRaw).count()
    ideas = db.query(IdeaCandidate).count()
    products = db.query(Product).count()
    logs = db.query(LifeLog).count()

    print(f"Results: Problems={problems}, Ideas={ideas}, Products={products}, Logs={logs}")

    if ideas > 0 and products > 0:
        print("✅ Cycle verification successful!")
    else:
        print("❌ Cycle verification failed.")
        sys.exit(1)
    db.close()

if __name__ == "__main__":
    test_full_cycle()
