from ..database import SessionLocal, IdeaCandidate, ProblemRaw, LifeLog, SystemSetting
from .llm import call_llm, extract_json
import json

def run_decision():
    print("Running Decision Core Gen-4.1...")
    db = SessionLocal()
    try:
        # Get weight settings from DB or use defaults from blueprint
        w_vol = 0.4
        w_neg = 0.2
        w_auto = 0.2
        w_rev = 0.2

        problems = db.query(ProblemRaw).order_by(ProblemRaw.created_at.desc()).limit(20).all()
        if not problems:
            print("No problems found")
            db.add(LifeLog(engine="decision", type="warning", message="No problems found to analyze"))
            db.commit()
            return

        combined_text = "\n---\n".join([f"ID: {p.id}\nTitle: {p.title}\nContent: {p.content[:300]}" for p in problems])

        prompt = (
            "You are the Brain of an Autonomous Organism. Your goal is to find a high-potential SaaS idea from human problems.\n"
            "Analyze these real problems and formulate ONE winning SaaS idea.\n\n"
            "Required qualitative metrics (0-10 scale):\n"
            "1. jumlah_keluhan: How many people seem to have this problem?\n"
            "2. emosi_negatif: How painful/frustrating is this problem?\n"
            "3. mudah_otomatis: How easy is it to solve this with code/AI autonomously?\n"
            "4. potensi_uang: How likely are people to pay for a solution?\n\n"
            "Return ONLY a JSON object with these keys:\n"
            "- 'theme': A catchy name for the SaaS\n"
            "- 'summary': Brief explanation of the solution\n"
            "- 'jumlah_keluhan': 0-10\n"
            "- 'emosi_negatif': 0-10\n"
            "- 'mudah_otomatis': 0-10\n"
            "- 'potensi_uang': 0-10\n"
            "- 'ui_ux_strategy': Design approach\n"
            "- 'monetization_model': How it makes money\n\n"
            f"PROBLEMS TO ANALYZE:\n{combined_text}"
        )

        response_text = call_llm(prompt)
        idea_data = extract_json(response_text)

        if idea_data and "theme" in idea_data:
            # Normalize scores to 0-1 range for the formula
            s_vol = float(idea_data.get("jumlah_keluhan", 5)) / 10.0
            s_neg = float(idea_data.get("emosi_negatif", 5)) / 10.0
            s_auto = float(idea_data.get("mudah_otomatis", 5)) / 10.0
            s_rev = float(idea_data.get("potensi_uang", 5)) / 10.0

            # Formula: score = (vol * 0.4) + (neg * 0.2) + (auto * 0.2) + (rev * 0.2)
            final_score = (s_vol * w_vol) + (s_neg * w_neg) + (s_auto * w_auto) + (s_rev * w_rev)

            db.add(IdeaCandidate(
                theme=idea_data["theme"],
                score=final_score,
                summary=idea_data.get("summary", ""),
                technical_spec=json.dumps(idea_data)
            ))
            db.add(LifeLog(engine="decision", type="success", message=f"Generated autonomous idea: {idea_data['theme']} with score {final_score:.2f}"))
            print(f"Success: {idea_data['theme']} (Score: {final_score:.2f})")
        else:
            print("Error: Failed to parse JSON from LLM")
            db.add(LifeLog(engine="decision", type="error", message="Failed to generate valid idea from LLM output"))

        db.commit()
    except Exception as e:
        print(f"Decision Exception: {str(e)}")
        db.add(LifeLog(engine="decision", type="error", message=f"Decision Core failed: {str(e)}"))
    finally:
        db.close()
