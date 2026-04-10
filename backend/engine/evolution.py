from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
import datetime

async def run_evolution(db: Session):
    log = models.EngineLog(level="info", source="Evolution", message="Evolution engine started (Gen-4 Self-Optimization)")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Evolution", message="No products yet. Evolution is observing market signals."))
        db.commit()
        return

    # 1. Performance Analysis
    total_revenue = db.query(func.sum(models.RevenueLog.amount)).scalar() or 0.0
    total_clicks = db.query(func.sum(models.TrafficLog.clicks)).scalar() or 0

    def get_or_create_setting(key, default_val, desc):
        setting = db.query(models.SystemSetting).filter(models.SystemSetting.key == key).first()
        if not setting:
            setting = models.SystemSetting(key=key, value=default_val, description=desc)
            db.add(setting)
        return setting

    # Strategy Parameters
    neg_weight = get_or_create_setting("decision_neg_weight", 40.0, "Weight for negative sentiment in scoring")
    vol_weight = get_or_create_setting("decision_volume_weight", 2.0, "Weight for problem volume in scoring")
    auto_weight = get_or_create_setting("decision_automation_weight", 20.0, "Weight for automation ease")
    rev_weight = get_or_create_setting("decision_revenue_weight", 20.0, "Weight for revenue potential")

    # 2. Strategic Adjustments
    # If revenue is high, we double down on 'painful' problems (high negative sentiment)
    if total_revenue > 500:
        neg_weight.value += 2.0
        db.add(models.EngineLog(level="success", source="Evolution", message="High revenue detected. Increasing focus on deep pain points."))

    # If traffic is high but revenue is low, we shift to 'volume' (mass market)
    if total_clicks > 2000 and total_revenue < 100:
        vol_weight.value += 1.0
        neg_weight.value -= 1.0
        db.add(models.EngineLog(level="warning", source="Evolution", message="High traffic/Low conversion. Shifting strategy to mass-market volume."))

    # If automation is becoming a bottleneck (many products but low quality)
    recent_errors = db.query(models.EngineLog).filter(
        models.EngineLog.level == "error",
        models.EngineLog.created_at >= (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1))
    ).count()

    if recent_errors > 20:
        auto_weight.value += 5.0 # Prioritize easier-to-automate tasks to reduce errors
        db.add(models.EngineLog(level="info", source="Evolution", message="Increasing automation threshold to ensure system stability."))

    db.commit()
    db.add(models.EngineLog(level="info", source="Evolution", message="Evolution cycle complete. Species strategy upgraded."))
    db.commit()
