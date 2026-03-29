from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from datetime import datetime
from .database import Base

class ProblemRaw(Base):
    __tablename__ = "problem_raw"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProblemClean(Base):
    __tablename__ = "problem_clean"
    id = Column(Integer, primary_key=True, index=True)
    text_clean = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class IdeaCandidate(Base):
    __tablename__ = "idea_candidates"
    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String)
    score = Column(Float)
    summary = Column(Text)
    evidence = Column(JSON)
    is_processed = Column(Boolean, default=False) # Flag for Factory
    created_at = Column(DateTime, default=datetime.utcnow)

class EngineLog(Base):
    __tablename__ = "engine_logs"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String) # info, warning, error, danger
    source = Column(String) # Sense, Decision, etc.
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class LifeLog(Base):
    __tablename__ = "life_log"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    result = Column(String)
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer)
    name = Column(String)
    blueprint_path = Column(String)
    is_promoted = Column(Boolean, default=False) # Flag for Growth
    created_at = Column(DateTime, default=datetime.utcnow)

class RevenueLog(Base):
    __tablename__ = "revenue_log"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    model = Column(String)
    amount = Column(Float)
    currency = Column(String, default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)

class TrafficLog(Base):
    __tablename__ = "traffic_log"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    channel = Column(String)
    clicks = Column(Integer, default=0)
    signups = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(Float)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
