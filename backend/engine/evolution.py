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
        return setting

    # Dynamic weights for Decision Core
    neg_weight = update_setting("decision_neg_weight", 40.0, "Weight for negative sentiment in scoring")
    vol_weight = update_setting("decision_volume_weight", 2.0, "Weight for problem volume in scoring")
    automation_weight = update_setting("decision_automation_weight", 20.0, "Weight for automation ease")
    revenue_weight = update_setting("decision_revenue_weight", 20.0, "Weight for revenue potential")

    # Evolution Logic: Adjust weights based on revenue performance
    # Proportional reward for high-revenue ideas
    if total_revenue > 0:
        # Increase revenue_weight proportionally to its success
        # Example: for every $100 revenue, increase weight by 1.0 (5% of base 20.0)
        boost = min(10.0, total_revenue / 100.0)
        revenue_weight.value += boost

        # Increase sensitivity to pain points if revenue is high (people pay to solve pain)
        neg_weight.value += (boost * 0.5)

        db.add(models.EngineLog(
            level="success",
            source="Evolution",
            message=f"Revenue detected (${total_revenue:.2f}). Increasing revenue_weight by {boost:.2f}."
        ))

    # If high traffic but NO revenue, maybe volume is less important than revenue potential
    if total_clicks > 1000 and total_revenue == 0:
        vol_weight.value -= 0.1 # Slight decrease if volume doesn't convert
        revenue_weight.value += 1.0 # Focus more on potential monetization next time
        db.add(models.EngineLog(
            level="warning",
            source="Evolution",
            message="High traffic without revenue. Shifting focus to monetization potential."
        ))

    db.commit()
    db.add(models.EngineLog(level="info", source="Evolution", message="Evolution cycle complete. Weights tuned."))
    db.commit()
