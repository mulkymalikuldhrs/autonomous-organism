import random
from ..models import SessionLocal, IdeaCandidate, RevenueLog, EngineLog, Base, engine as db_engine

class MonetizationEngine:
    async def run(self, traffic=0):
        print("\n" + "="*50)
        print("💰 MONETIZATION ENGINE (PERUT) STARTING")
        print("="*50)

        db = SessionLocal()
        try:
            idea = db.query(IdeaCandidate).order_by(IdeaCandidate.created_at.desc()).first()
            if not idea: return 0

            # Deterministic simulation based on category hints in summary
            conv_rate = 0.05
            if "b2b" in idea.summary.lower(): conv_rate = 0.02
            elif "tools" in idea.summary.lower(): conv_rate = 0.08

            sales = int(traffic * conv_rate)
            price = 19.99 if "business" in idea.theme.lower() else 9.99
            revenue = sales * price

            if revenue > 0:
                db.add(RevenueLog(product=idea.theme, amount=revenue))
                print(f"   💸 Sales: {sales} | Revenue: ${revenue:.2f}")

            log = EngineLog(level="success", source="MONETIZATION", message=f"Earned: ${revenue:.2f} from {sales} sales.")
            db.add(log)
            db.commit()
            return revenue
        except Exception as e:
            print(f"🔥 MONETIZATION ERROR: {e}")
            return 0
        finally:
            db.close()
