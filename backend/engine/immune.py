import time
from ..models import SessionLocal, EngineLog, SystemSetting, Base, engine as db_engine

class ImmuneSystem:
    def __init__(self):
        self.error_threshold = 10
        self.product_limit_per_hour = 5

    def check_health(self):
        print("\n" + "🛡️"*25)
        print("🛡️ IMMUNE SYSTEM (ANTI-GILA) CHECKING")
        print("🛡️"*25)

        Base.metadata.create_all(bind=db_engine)
        db = SessionLocal()

        try:
            # Count errors in last hour
            error_count = db.query(EngineLog).filter(
                EngineLog.level == "error"
            ).count()

            if error_count > self.error_threshold:
                print(f"   🚨 HIGH ERROR RATE DETECTED ({error_count}). ACTIVATING THROTTLE.")
                self.set_setting(db, "system_throttle", "true")
            else:
                self.set_setting(db, "system_throttle", "false")
                print(f"   ✅ System health optimal. Errors: {error_count}")

            return error_count <= self.error_threshold

        except Exception as e:
            print(f"🔥 IMMUNE SYSTEM ERROR: {e}")
            return False
        finally:
            db.close()

    def set_setting(self, db, key, value):
        setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
        if setting:
            setting.value = value
        else:
            db.add(SystemSetting(key=key, value=value))
        db.commit()

if __name__ == "__main__":
    immune = ImmuneSystem()
    immune.check_health()
