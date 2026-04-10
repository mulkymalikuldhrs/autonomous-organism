from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import models
import datetime
import os
import shutil

async def check_health(db: Session):
    log_source = "Immune"
    now = datetime.datetime.now(datetime.timezone.utc)

    # 1. Error Rate Monitoring
    one_hour_ago = now - datetime.timedelta(hours=1)
    errors = db.query(models.EngineLog).filter(
        models.EngineLog.level == "error",
        models.EngineLog.created_at >= one_hour_ago
    ).count()

    if errors > 10:
        db.add(models.EngineLog(level="danger", source=log_source, message=f"CRITICAL: High error rate ({errors} errors/hr). Throttling cycles."))
        # Safety: Disable non-essential engines via settings
        throttle = db.query(models.SystemSetting).filter(models.SystemSetting.key == "system_throttle").first()
        if not throttle:
            throttle = models.SystemSetting(key="system_throttle", value=1.0, description="System activity multiplier")
            db.add(throttle)
        throttle.value = 0.5

    # 2. Storage & Resource Health
    try:
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)
        if free_gb < 1:
            db.add(models.EngineLog(level="warning", source=log_source, message=f"Low disk space: {free_gb} GB. Initiating data purge."))
            # Purge raw problems older than 3 days
            db.query(models.ProblemRaw).filter(models.ProblemRaw.created_at < (now - datetime.timedelta(days=3))).delete()
    except Exception as e:
        db.add(models.EngineLog(level="error", source=log_source, message=f"Failed to check disk health: {e}"))

    # 3. Intelligence Reliability Check
    # Check if LLM is consistently failing (falling back)
    fallback_logs = db.query(models.EngineLog).filter(
        models.EngineLog.message.contains("Ollama error"),
        models.EngineLog.created_at >= one_hour_ago
    ).count()

    if fallback_logs > 20:
        db.add(models.EngineLog(level="warning", source=log_source, message="LLM reliability low. Check Ollama connectivity."))

    # 4. Pipeline Monitoring (Indonesian Sources)
    id_findings = db.query(models.ProblemRaw).filter(
        models.ProblemRaw.source.contains(".id") | models.ProblemRaw.source.contains("kaskus"),
        models.ProblemRaw.created_at >= (now - datetime.timedelta(days=1))
    ).count()

    if id_findings == 0:
        db.add(models.EngineLog(level="warning", source=log_source, message="No Indonesian findings in last 24h. Sense ID pipeline might be blocked."))

    # 5. Anomaly Detection
    recent_products = db.query(models.Product).filter(models.Product.created_at >= one_hour_ago).count()
    if recent_products > 5:
        db.add(models.EngineLog(level="danger", source=log_source, message=f"Anomaly: Rapid product spawning detected ({recent_products}/hr). Emergency pause."))

    db.add(models.EngineLog(level="info", source=log_source, message="System health check: All vitals normal."))
    db.commit()
