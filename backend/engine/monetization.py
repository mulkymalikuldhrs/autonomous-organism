from sqlalchemy.orm import Session
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started (Gen-4 Realism)")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products yet to monetize."))
        db.commit()
        return

    # Deterministic models based on product name/category hints
    for product in products:
        # Check traffic
        traffic = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first()
        clicks = traffic.clicks if traffic else 0

        # Calculate conversion rate based on clicks
        # Real-world SaaS conversion is usually 1-3%
        conversion_rate = 0.02
        conversions = int(clicks * conversion_rate)

        # Fixed pricing for stability in simulation
        price_per_unit = 19.00

        if conversions > 0:
            amount = round(conversions * price_per_unit, 2)
            model_type = "Subscription"

            # Check if we already logged this revenue for today to avoid duplication in rapid loops
            today = datetime.datetime.now(datetime.timezone.utc).date()
            exists = db.query(models.RevenueLog).filter(
                models.RevenueLog.product_id == product.id,
                models.RevenueLog.created_at >= datetime.datetime.combine(today, datetime.time.min)
            ).first()

            if not exists:
                revenue = models.RevenueLog(
                    product_id=product.id,
                    model=model_type,
                    amount=amount
                )
                db.add(revenue)
                db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount} from {conversions} conversions."))
            else:
                # Update existing for the day if more conversions happened
                if amount > exists.amount:
                    exists.amount = amount
                    db.add(models.EngineLog(level="info", source="Monetization", message=f"Updated revenue for {product.name}: ${amount} total for today."))

    db.commit()
