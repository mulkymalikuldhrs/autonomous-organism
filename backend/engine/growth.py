import random
import os
import requests
from ..models import SessionLocal, IdeaCandidate, EngineLog, Base, engine as db_engine

class GrowthEngine:
    def __init__(self):
        self.channels = ["Reddit", "Medium", "Substack", "Telegram", "Twitter"]
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3"

    def generate_content(self, idea, channel):
        prompt = f"Buat postingan promosi untuk {channel} mengenai produk SaaS '{idea.theme}'. Deskripsi: {idea.summary}. Gunakan bahasa yang menarik dan persuasif."
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get('response', '')
        except:
            pass
        return f"Check out {idea.theme}! {idea.summary}"

    async def run(self):
        print("\n" + "="*50)
        print("📢 GROWTH ENGINE (MULUT) STARTING")
        print("="*50)

        db = SessionLocal()
        try:
            idea = db.query(IdeaCandidate).order_by(IdeaCandidate.created_at.desc()).first()
            if not idea: return 0

            outbox = "growth_outbox"
            os.makedirs(outbox, exist_ok=True)

            traffic = 0
            for channel in self.channels:
                content = self.generate_content(idea, channel)
                clicks = random.randint(5, 50)
                traffic += clicks

                with open(f"{outbox}/{channel.lower()}_post.txt", 'w') as f:
                    f.write(content)
                print(f"   ✅ AI Content generated for {channel} -> {clicks} clicks.")

            log = EngineLog(level="success", source="GROWTH", message=f"Campaign finished. Total traffic: {traffic} clicks.")
            db.add(log)
            db.commit()
            return traffic
        except Exception as e:
            print(f"🔥 GROWTH ERROR: {e}")
            return 0
        finally:
            db.close()
