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

        # Simulation: 5% conversion rate for realistic testing
        # We look for clicks that haven't been "monetized" yet or just simulate based on total
        # In a real system, this would be an actual stripe webhook or affiliate API

        conversion_rate = 0.05
        new_customers = int(total_clicks * conversion_rate)

        if new_customers > 0:
            model_type = "Subscription" if "SaaS" in product.name else "Affiliate"
            # Deterministic based on clicks to avoid "random" jumps without traffic
            # Affiliate: $0.50 per click conversion, Subscription: $9.99 per signup
            amount = new_customers * (9.99 if model_type == "Subscription" else 0.50)

            revenue = models.RevenueLog(
                product_id=product.id,
                model=model_type,
                amount=round(amount, 2)
            )
            db.add(revenue)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} ({model_type})"))

    db.commit()
