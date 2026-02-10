from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, ForeignKey, Boolean
from sqlalchemy.sql import func
from .database import Base

class ProblemRaw(Base):
    __tablename__ = "problem_raw"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    external_id = Column(String, unique=True)
    title = Column(Text)
    url = Column(Text)
    content = Column(Text)
    date = Column(DateTime(timezone=True), server_default=func.now())

class ProblemClean(Base):
    __tablename__ = "problem_clean"
    id = Column(Integer, primary_key=True, index=True)
    raw_id = Column(Integer, ForeignKey("problem_raw.id"))
    text_clean = Column(Text)

class IdeaCandidate(Base):
    __tablename__ = "idea_candidates"
    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String)
    score = Column(Float)
    summary = Column(Text)
    evidence = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EngineRun(Base):
    __tablename__ = "engine_runs"
    id = Column(Integer, primary_key=True, index=True)
    engine = Column(String) # sense, decision, factory, growth
    status = Column(String) # running, success, failed
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True))
    meta = Column(JSON)

class EngineLog(Base):
    __tablename__ = "engine_logs"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("engine_runs.id"))
    level = Column(String) # info, success, warning, error
    source = Column(String)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
