from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, sense_engine

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # This will create the database file and tables if they don't exist
    database.init_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/sense/run")
def run_sense_engine(db: Session = Depends(database.get_db)):
    """
    Runs the Sense Engine to scrape for new problems and store them in the database.
    This process is now idempotent and uses a single transaction.
    """
    try:
        ideas = sense_engine.scrape_reddit_sideprojectideas()

        # Fetch existing problem texts to prevent duplicates
        existing_problems = db.query(database.ProblemRaw.text).all()
        existing_texts = {text for (text,) in existing_problems}

        new_problems_count = 0
        for idea_text in ideas:
            if idea_text in existing_texts:
                continue  # Skip duplicate

            # Create a raw problem record
            raw_problem = database.ProblemRaw(source="reddit_sideprojectideas", text=idea_text)
            db.add(raw_problem)

            # Defer commit until after the loop
            # The raw_problem object is associated with the session, and its ID will be available after the commit.
            # We'll create the clean problem in a separate step for simplicity in this V1.

            new_problems_count += 1

        # Commit all new raw problems in a single transaction
        db.commit()

        # Now, create clean versions for the newly added raw problems
        newly_added_raw = db.query(database.ProblemRaw).filter(database.ProblemRaw.text.in_(ideas)).all()

        for raw_problem in newly_added_raw:
             # A simple check to avoid creating duplicate clean entries if this endpoint is ever run in parallel
            exists = db.query(database.ProblemClean).filter(database.ProblemClean.raw_id == raw_problem.id).first()
            if not exists:
                clean_problem = database.ProblemClean(text_clean=raw_problem.text.strip(), raw_id=raw_problem.id)
                db.add(clean_problem)

        # Commit all new clean problems in a single transaction
        db.commit()

        return {"message": f"Sense Engine run complete. Ingested {new_problems_count} new problems."}
    except Exception as e:
        db.rollback()  # Rollback the transaction on error
        # Log the error for debugging
        print(f"Error during Sense Engine run: {e}")
        # Return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="An error occurred in the Sense Engine.")
