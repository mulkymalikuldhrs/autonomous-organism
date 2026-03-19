from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
import datetime

async def run_evolution(db: Session):
    log = models.EngineLog(level="info", source="Evolution", message="Evolution engine started")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Evolution", message="No products yet. Evolution is observing."))
        db.commit()
        return

    # 1. Analyze performance
    total_revenue = db.query(func.sum(models.RevenueLog.amount)).scalar() or 0.0
    total_clicks = db.query(func.sum(models.TrafficLog.clicks)).scalar() or 0

    def update_setting(key, default_val, desc):
        setting = db.query(models.SystemSetting).filter(models.SystemSetting.key == key).first()
        if not setting:
            setting = models.SystemSetting(key=key, value=default_val, description=desc)
            db.add(setting)
            db.commit() # Persistent on creation
        return setting

    # Dynamic weights for Decision Core
    neg_weight = update_setting("decision_neg_weight", 40.0, "Weight for negative sentiment in scoring")
    vol_weight = update_setting("decision_volume_weight", 2.0, "Weight for problem volume in scoring")
    automation_weight = update_setting("decision_automation_weight", 20.0, "Weight for automation ease")
    revenue_weight = update_setting("decision_revenue_weight", 20.0, "Weight for revenue potential")

    # Evolution Logic
    if total_revenue > 100:
        neg_weight.value += 1.0
        db.add(models.EngineLog(level="success", source="Evolution", message="Revenue detected! Increasing pain-point sensitivity."))

    if total_clicks > 1000 and total_revenue == 0:
        vol_weight.value += 0.5
        db.add(models.EngineLog(level="warning", source="Evolution", message="High traffic but no revenue. Shifting focus to volume."))

    db.commit()
    db.add(models.EngineLog(level="info", source="Evolution", message="Evolution cycle complete. Weights tuned."))
    db.commit()
