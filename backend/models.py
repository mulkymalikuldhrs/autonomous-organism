from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./organism.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ProblemRaw(Base):
    __tablename__ = "problem_raw"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    text = Column(Text)
    external_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ProblemClean(Base):
    __tablename__ = "problem_clean"
    id = Column(Integer, primary_key=True, index=True)
    raw_id = Column(Integer, ForeignKey("problem_raw.id"))
    text_clean = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class IdeaCandidate(Base):
    __tablename__ = "idea_candidates"
    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String)
    score = Column(Float)
    summary = Column(Text)
    evidence = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EngineLog(Base):
    __tablename__ = "engine_logs"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    source = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RevenueLog(Base):
    __tablename__ = "revenue_log"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SystemSetting(Base):
    __tablename__ = "system_settings"
    key = Column(String, primary_key=True)
    value = Column(String)
