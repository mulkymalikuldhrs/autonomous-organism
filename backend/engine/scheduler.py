import time
import threading
from ..database import SessionLocal, SystemSetting, LifeLog
from .sense import run_sense
from .decision import run_decision
from .factory import run_factory
from .growth import run_growth
from .monetization import run_monetization
from .evolution import run_evolution, run_immune

def orchestrate_cycle():
    db = SessionLocal()
    try:
        active = db.query(SystemSetting).filter(SystemSetting.key == "system_active").first()
        if not active or active.value != "true":
            return

        db.add(LifeLog(engine="scheduler", type="info", message="Starting autonomous cycle"))
        db.commit()

        # Execute Pipeline
        run_sense()
        run_decision()
        run_factory()
        run_growth()
        run_monetization()
        run_evolution()
        run_immune()

        db.add(LifeLog(engine="scheduler", type="success", message="Cycle completed successfully"))
        db.commit()
    except Exception as e:
        print(f"Cycle failed: {str(e)}")
        db.add(LifeLog(engine="scheduler", type="error", message=f"Cycle failed: {str(e)}"))
        db.commit()
    finally:
        db.close()

def start_scheduler():
    def run_forever():
        while True:
            orchestrate_cycle()
            db = SessionLocal()
            cycle_time = int(db.query(SystemSetting).filter(SystemSetting.key == "system_cycle_seconds").first().value)
            db.close()
            time.sleep(cycle_time)

    thread = threading.Thread(target=run_forever, daemon=True)
    thread.start()
