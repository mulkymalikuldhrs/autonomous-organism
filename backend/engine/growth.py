from ..database import SessionLocal, Product, TrafficLog, LifeLog
import random

def run_growth():
    db = SessionLocal()
    try:
        # Target only built products to deploy them
        products = db.query(Product).filter(Product.status == "built").all()
        for product in products:
            # Simulate marketing campaign across multiple channels
            channels = ["Twitter", "Reddit", "IndieHackers", "ProductHunt"]
            for channel in channels:
                # Deterministic but slightly random traffic: 10-50 clicks per channel
                clicks = random.randint(10, 50)
                db.add(TrafficLog(product_id=product.id, channel=channel, clicks=clicks))
                db.add(LifeLog(engine="growth", type="info", message=f"Campaign on {channel} for {product.name}: {clicks} clicks"))

            # Update status to deployed after first growth cycle
            product.status = "deployed"
            db.add(LifeLog(engine="growth", type="success", message=f"Product {product.name} is now LIVE"))

        db.commit()
    finally:
        db.close()
