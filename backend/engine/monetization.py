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
        total_clicks = sum(t.clicks for t in traffic_logs) if traffic_logs else 0

        # Gen-4.1 Deterministic Simulation: 5% conversion rate
        conversion_rate = 0.05
        active_conversions = int(total_clicks * conversion_rate)

        if active_conversions > 0 or random.random() < 0.05:
            # Determine rate based on product category hint or random
            # Affiliate: $0.50 per click conversion
            # Subscription: $9.99 per signup
            # Tool Sale: $29.00 once

            model_type = random.choice(models_available)

            if model_type == "Affiliate":
                amount = active_conversions * 0.50 if active_conversions > 0 else 0.50
            elif model_type == "Subscription":
                amount = active_conversions * 9.99 if active_conversions > 0 else 9.99
            else:
                amount = 29.00

            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=round(amount, 2)
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} ({model_type})"))

    db.commit()
