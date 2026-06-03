from ..database import SessionLocal, Product, TrafficLog, LifeLog
import random

def run_growth():
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.status == "built").all()
        for product in products:
            # Simulate marketing campaign
            clicks = random.randint(10, 100)
            db.add(TrafficLog(product_id=product.id, channel="Twitter", clicks=clicks))
            db.add(LifeLog(engine="growth", type="info", message=f"Marketing {product.name}: {clicks} clicks"))

            # Update status to deployed
            product.status = "deployed"

        db.commit()
    finally:
        db.close()
