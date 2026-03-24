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
        return

    for product in products:
        # Simulate traffic and conversion
        # In a real scenario, this would come from an analytics API
        traffic = db.query(models.TrafficLog).filter(models.TrafficLog.product_id == product.id).first()
        if not traffic:
            traffic = models.TrafficLog(product_id=product.id, channel="Organic", clicks=random.randint(50, 500), signups=random.randint(1, 10))
            db.add(traffic)
        else:
            traffic.clicks += random.randint(10, 50)
            traffic.signups += random.randint(0, 2)

        # Simulate revenue based on signups
        if traffic.signups > 0:
            # 10% conversion to paid, average $29/mo
            new_revenue = (traffic.signups * 0.1) * 29.0
            if new_revenue > 0:
                rev_log = models.RevenueLog(product_id=product.id, model="Subscription", amount=new_revenue)
                db.add(rev_log)
                db.add(models.EngineLog(level="success", source="Monetization", message=f"Generated ${new_revenue:.2f} revenue for {product.name}"))

    db.commit()
