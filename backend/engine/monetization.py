from sqlalchemy.orm import Session
from .. import models
import random
import datetime

async def run_monetization(db: Session):
    log = models.EngineLog(level="info", source="Monetization", message="Monetization Engine (Gen-4) started")
    db.add(log)
    db.commit()

    products = db.query(models.Product).all()
    if not products:
        db.add(models.EngineLog(level="info", source="Monetization", message="No products yet to monetize."))
        db.commit()
        return

    total_income = 0
    for product in products:
        # Simulate traffic/clicks if not present
        traffic = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first()
        if not traffic:
            traffic = models.TrafficLog(product_id=product.id, channel="direct", clicks=random.randint(5, 50))
            db.add(traffic)

        # Simulate revenue based on clicks and conversion
        conversion_rate = 0.05
        sales = int(traffic.clicks * conversion_rate)
        if sales > 0:
            amount = sales * 9.99 # Mock price
            revenue = models.RevenueLog(product_id=product.id, model="Subscription", amount=amount)
            db.add(revenue)
            total_income += amount
            db.add(models.EngineLog(level="success", source="Monetization", message=f"Generated ${amount:.2f} revenue for {product.name}"))

    db.commit()
    db.add(models.EngineLog(level="info", source="Monetization", message=f"Monetization cycle complete. Total new revenue: ${total_income:.2f}"))
    db.commit()
    return {"income": total_income}
