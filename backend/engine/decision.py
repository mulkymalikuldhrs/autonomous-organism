from ..database import SessionLocal, IdeaCandidate, ProblemRaw, LifeLog
from .llm import call_llm, extract_json
import json

def run_decision():
    print("Running Decision Core...")
    db = SessionLocal()
    try:
        problems = db.query(ProblemRaw).order_by(ProblemRaw.created_at.desc()).limit(10).all()
        if not problems:
            print("No problems found")
            db.add(LifeLog(engine="decision", type="warning", message="No problems found to analyze"))
            db.commit()
            return

        combined_text = "\n---\n".join([f"Title: {p.title}\nContent: {p.content[:500]}" for p in problems])
        prompt = (
            "You are the Brain of an Autonomous Organism. "
            "Analyze these real problems collected from the web and formulate a winning SaaS idea. "
            "Return ONLY a JSON object with keys: 'theme', 'score' (0.0-1.0), 'summary', 'ui_ux_strategy', 'monetization_model'.\n\n"
            f"PROBLEMS:\n{combined_text}"
        )

        response_text = call_llm(prompt)
        print(f"LLM Response: {response_text[:100]}...")
        idea_data = extract_json(response_text)

        if idea_data and "theme" in idea_data:
            db.add(IdeaCandidate(
                theme=idea_data["theme"],
                score=float(idea_data.get("score", 0.5)),
                summary=idea_data.get("summary", ""),
                technical_spec=json.dumps(idea_data)
            ))
            db.add(LifeLog(engine="decision", type="success", message=f"Generated autonomous idea: {idea_data['theme']}"))
            print(f"Success: {idea_data['theme']}")
        else:
            print("Error: Failed to parse JSON")
            db.add(LifeLog(engine="decision", type="error", message="Failed to generate valid idea from LLM output"))

        db.commit()
    except Exception as e:
        print(f"Decision Exception: {str(e)}")
    finally:
        db.close()
