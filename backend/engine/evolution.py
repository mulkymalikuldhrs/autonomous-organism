from ..database import SessionLocal, LifeLog, SystemSetting

def run_evolution():
    db = SessionLocal()
    try:
        # Autonomous tuning
        # In a real Gen-4.1, this would analyze metrics and adjust system_cycle_seconds
        db.add(LifeLog(engine="evolution", type="info", message="Evolving system parameters"))
        db.commit()
    finally:
        db.close()

def run_immune():
    db = SessionLocal()
    try:
        # Check for errors and runaway processes
        errors = db.query(LifeLog).filter(LifeLog.type == "error").count()
        if errors > 10:
             # Throttling logic
             setting = db.query(SystemSetting).filter(SystemSetting.key == "system_throttle").first()
             if not setting:
                 db.add(SystemSetting(key="system_throttle", value="true"))
             db.add(LifeLog(engine="immune", type="warning", message="High error rate detected. Throttling system."))
        db.commit()
    finally:
        db.close()
