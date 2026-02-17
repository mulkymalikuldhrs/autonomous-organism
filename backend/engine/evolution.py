from sqlalchemy.orm import Session
from .. import models
import datetime

async def run_evolution(db: Session):
    log = models.EngineLog(level="info", source="Evolution", message="Evolution engine started")
    db.add(log)
    db.commit()

    # 1. Analyze performance
    # Get total revenue and traffic per product theme
    # For now, we simulate "learning" from logs

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Evolution", message="No products yet. Evolution is observing."))
        db.commit()
        return

    # Logic: if total revenue > 0, we are doing something right
    total_revenue = db.query(models.RevenueLog.amount).sum() or 0
    total_clicks = db.query(models.TrafficLog.clicks).sum() or 0

    # Adjust weights in SystemSetting
    # Keys: decision_neg_weight, decision_volume_weight

    def update_setting(key, default_val, desc):
        setting = db.query(models.SystemSetting).filter(models.SystemSetting.key == key).first()
        if not setting:
            setting = models.SystemSetting(key=key, value=default_val, description=desc)
            db.add(setting)
        return setting

    neg_weight = update_setting("decision_neg_weight", 40.0, "Weight for negative sentiment in scoring")
    vol_weight = update_setting("decision_volume_weight", 2.0, "Weight for problem volume in scoring")

    # If we have revenue, maybe we should focus more on "pain" (neg sentiment)
    if total_revenue > 100:
        neg_weight.value += 1.0
        db.add(models.EngineLog(level="success", source="Evolution", message="Revenue detected! Increasing pain-point sensitivity."))

    # If we have lots of clicks but no revenue, maybe we need to focus on different themes
    if total_clicks > 1000 and total_revenue == 0:
        vol_weight.value += 0.5
        db.add(models.EngineLog(level="warning", source="Evolution", message="High traffic but no revenue. Shifting focus to volume."))

    db.commit()
    db.add(models.EngineLog(level="info", source="Evolution", message="Evolution cycle complete. Weights tuned."))
    db.commit()
