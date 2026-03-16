from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products to monetize yet."))
        db.commit()
        return

    for product in products:
        # Simulate traffic-based revenue
        # Get total clicks for this product
        clicks = db.query(func.sum(models.TrafficLog.clicks)).filter(models.TrafficLog.product_id == product.id).scalar() or 0

        # Simple simulation logic: 1% conversion rate, $29 per conversion
        conversion_rate = 0.01
        expected_sales = int(clicks * conversion_rate)

        if expected_sales > 0:
            revenue_amount = expected_sales * 29.0
            log_entry = models.RevenueLog(
                product_id=product.id,
                model="Subscription",
                amount=revenue_amount,
                currency="USD"
            )
            db.add(log_entry)
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Generated ${revenue_amount} revenue for {product.name}"))
        else:
            # Random tiny revenue for simulation if no traffic yet
            if random.random() < 0.1:
                revenue_amount = 5.0
                db.add(models.RevenueLog(
                    product_id=product.id,
                    model="Donation",
                    amount=revenue_amount,
                    currency="USD"
                ) )
                db.add(models.EngineLog(level="info", source="Monetization", message=f"Received ${revenue_amount} donation for {product.name}"))

    db.commit()
