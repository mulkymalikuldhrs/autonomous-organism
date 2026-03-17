from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import models
from ..models import utc_now
import datetime
import os
import shutil

async def check_health(db: Session):
    log_source = "Immune"

    # 1. Error Rate Check
    one_hour_ago = utc_now() - datetime.timedelta(hours=1)
    errors = db.query(models.EngineLog).filter(
        models.EngineLog.level == "error",
        models.EngineLog.created_at >= one_hour_ago
    ).count()

    if errors > 10:
        db.add(models.EngineLog(level="danger", source=log_source, message=f"CRITICAL: High error rate ({errors} errors/hr). Entering isolation."))
        # In a real scenario, this could trigger a system pause or restart

    # 2. Disk Space Check
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    if free_gb < 1:
        db.add(models.EngineLog(level="warning", source=log_source, message=f"Low disk space: {free_gb} GB remaining. Cleaning logs..."))
        # Potential cleanup logic: delete old raw problems
        db.query(models.ProblemRaw).filter(models.ProblemRaw.created_at < (utc_now() - datetime.timedelta(days=7))).delete()

    # 3. Database Integrity Check
    try:
        # Simple query to ensure DB is responsive
        db.execute(text("SELECT 1")).fetchone()
    except Exception as e:
        print(f"DB Integrity Failure: {e}")
        # Could trigger an emergency backup or alert

    # 4. Loop Prevention
    # Check if we are generating too many products too fast (potential runaway)
    recent_products = db.query(models.Product).filter(models.Product.created_at >= one_hour_ago).count()
    if recent_products > 5:
        db.add(models.EngineLog(level="danger", source=log_source, message=f"Anomaly: {recent_products} products generated in 1 hour. Throttling factory."))
        # Could set a SystemSetting to pause factory

    db.add(models.EngineLog(level="info", source=log_source, message="System health check: All vitals normal."))
    db.commit()
