from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization engine started (Gen-4)")
    db.add(log)
    db.commit()

    # Get products and traffic data
    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products yet to monetize."))
        db.commit()
        return

    total_new_revenue = 0.0

    for product in products:
        # 1. Gather Traffic Info
        total_clicks = db.query(func.sum(models.TrafficLog.clicks)).filter(models.TrafficLog.product_id == product.id).scalar() or 0

        if total_clicks > 0:
            # 2. Revenue Simulation (Simulating Conversion)
            # 1-3% conversion rate, $9.99 average revenue per conversion
            conversion_rate = random.uniform(0.01, 0.03)
            conversions = int(total_clicks * conversion_rate)

            if conversions > 0:
                amount = conversions * 9.99
                revenue_log = models.RevenueLog(
                    product_id=product.id,
                    model="SaaS Subscription",
                    amount=amount,
                    currency="USD"
                )
                db.add(revenue_log)
                total_new_revenue += amount
                db.add(models.EngineLog(level="success", source="Monetization", message=f"Revenue generated for {product.name}: ${amount:.2f}"))

    db.add(models.EngineLog(level="info", source="Monetization", message=f"Monetization cycle complete. Total new revenue: ${total_new_revenue:.2f}"))
    db.commit()
    return total_new_revenue
