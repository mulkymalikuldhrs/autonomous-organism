from sqlalchemy.orm import Session
from .. import models
import datetime

async def check_health(db: Session):
    # Check for recent errors
    one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    errors = db.query(models.EngineLog).filter(
        models.EngineLog.level == "error",
        models.EngineLog.created_at >= one_hour_ago
    ).count()

    if errors > 5:
        log = models.EngineLog(level="danger", source="Immune", message=f"High error rate detected ({errors} errors in last hour). Entering isolation mode.")
        db.add(log)
    else:
        log = models.EngineLog(level="info", source="Immune", message="System health check: Optimal.")
        db.add(log)
    db.commit()
