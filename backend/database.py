import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Use SQLite as the database.
# The --app-dir backend flag in the uvicorn command ensures this file is created inside the backend directory.
DATABASE_URL = "sqlite:///organism.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the database models
class ProblemRaw(Base):
    __tablename__ = "problem_raw"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProblemClean(Base):
    __tablename__ = "problem_clean"
    id = Column(Integer, primary_key=True, index=True)
    text_clean = Column(Text)
    raw_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LifeLog(Base):
    __tablename__ = "life_log"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    name = Column(String)
    result = Column(String)
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class IdeaCandidate(Base):
    __tablename__ = "idea_candidates"
    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String)
    score = Column(Float)
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized.")