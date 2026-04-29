from sqlalchemy.orm import Session
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products yet to monetize."))
        db.commit()
        return

    # For each product, simulate revenue if it has traffic or randomly
    # Models: Affiliate, Subscription, Jual Tools, Lead Generation, Donation
    models_available = ["Affiliate", "Subscription", "Tool Sale", "Lead Gen", "Donation"]

    for product in products:
        # Check traffic
        traffic_logs = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).all()
        total_clicks = sum([t.clicks for t in traffic_logs])

        # Deterministic simulation: 1% conversion rate for every 100 clicks
        # or a base chance if traffic is low but exists
        new_sales = total_clicks // 100

        # Check if we already logged revenue for these clicks to avoid double counting
        # (Simplified: just check if any revenue exists, if not and clicks > 50, give a first sale)
        existing_revenue = db.query(models.RevenueLog).filter(models.RevenueLog.product_id == product.id).count()

        if (total_clicks > 50 and existing_revenue == 0) or new_sales > existing_revenue:
            model_type = random.choice(models_available)
            amount = round(random.uniform(10.0, 99.0), 2) # Aggressive pricing

            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=amount
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} ({model_type}) based on {total_clicks} clicks"))

    db.commit()
