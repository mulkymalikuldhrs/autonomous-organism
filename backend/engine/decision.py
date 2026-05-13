import requests
import json
import re
from ..models import SessionLocal, ProblemClean, IdeaCandidate, EngineLog, Base, engine as db_engine

class DecisionCore:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3"

    def get_candidates_from_llm(self, problems):
        prompt = f"""
        Kamu adalah Decision Core untuk organisme SaaS otonom.
        Tugasmu adalah menganalisis masalah-masalah manusia berikut dan memberikan 1 ide solusi SaaS terbaik.

        Masalah:
        {json.dumps(problems, indent=2)}

        Berikan output dalam format JSON:
        {{
            "theme": "Nama Produk",
            "score": 0.95,
            "summary": "Penjelasan singkat solusi",
            "potential_revenue": "Affiliate/Subscription",
            "automation_ease": 0.9
        }}
        """

        try:
            response = requests.post(
                self.ollama_url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=30
            )
            if response.status_code == 200:
                result = response.json().get('response', '')
                # Extract JSON from response
                match = re.search(r'\{.*\}', result, re.DOTALL)
                if match:
                    return json.loads(match.group())
        except Exception as e:
            print(f"   ⚠️ LLM Error: {e}. Using deterministic fallback.")

        # Fallback logic if LLM fails
        if not problems:
            return None

        best_problem = problems[0]
        return {
            "theme": f"Auto {best_problem[:10].capitalize()}",
            "score": 0.8,
            "summary": f"Autonomous solution for: {best_problem}",
            "potential_revenue": "Subscription",
            "automation_ease": 0.7
        }

    async def run(self):
        print("\n" + "="*50)
        print("🧠 DECISION CORE (BRAIN) STARTING")
        print("="*50)

        Base.metadata.create_all(bind=db_engine)
        db = SessionLocal()

        try:
            # Get latest clean problems
            problems = db.query(ProblemClean).order_by(ProblemClean.created_at.desc()).limit(20).all()
            problem_texts = [p.text_clean for p in problems]

            if not problem_texts:
                # Add mock if empty for testing
                problem_texts = ["susah cari freelancer terpercaya", "ribet atur jadwal posting instagram"]

            print(f"   📊 Analyzing {len(problem_texts)} problems...")

            idea = self.get_candidates_from_llm(problem_texts)

            if idea:
                new_idea = IdeaCandidate(
                    theme=idea['theme'],
                    score=idea['score'],
                    summary=idea['summary'],
                    evidence=idea
                )
                db.add(new_idea)
                db.commit()

                log = EngineLog(
                    level="success",
                    source="DECISION",
                    message=f"Generated new idea: {idea['theme']} (Score: {idea['score']})"
                )
                db.add(log)
                db.commit()

                print(f"✅ DECISION CORE COMPLETE: {idea['theme']} selected.")
                return idea

            return None

        except Exception as e:
            print(f"🔥 DECISION CORE CRITICAL ERROR: {e}")
            log = EngineLog(
                level="error",
                source="DECISION",
                message=f"Critical failure: {str(e)}"
            )
            db.add(log)
            db.commit()
            return None
        finally:
            db.close()

if __name__ == "__main__":
    import asyncio
    core = DecisionCore()
    asyncio.run(core.run())
