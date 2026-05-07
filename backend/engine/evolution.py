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

    # Evolution Logic
    # 2. Analyze individual product performance
    all_products = db.query(models.Product).all()
    for product in all_products:
        rev = db.query(func.sum(models.RevenueLog.amount)).filter(models.RevenueLog.product_id == product.id).scalar() or 0.0
        clicks = db.query(func.sum(models.TrafficLog.clicks)).filter(models.TrafficLog.product_id == product.id).scalar() or 0

        conversion_rate = rev / clicks if clicks > 0 else 0.0

        # If product is successful, reinforce the weights that led to its creation
        if rev > 10:
             neg_weight.value += 0.5
             automation_weight.value += 0.2
             db.add(models.EngineLog(level="success", source="Evolution", message=f"Product {product.name} is profitable! Reinforcing pain-point and automation weights."))

    # 3. System-wide adjustments
    if total_revenue > 100:
        neg_weight.value += 1.0
        db.add(models.EngineLog(level="success", source="Evolution", message="High overall revenue detected! Increasing pain-point sensitivity."))

    if total_clicks > 1000 and total_revenue < 10:
        vol_weight.value += 1.0
        neg_weight.value -= 0.5
        db.add(models.EngineLog(level="warning", source="Evolution", message="High traffic but low revenue. Shifting focus to high-volume/lower-pain problems."))

    db.commit()
    db.add(models.EngineLog(level="info", source="Evolution", message="Evolution cycle complete. Weights tuned."))
    db.commit()
