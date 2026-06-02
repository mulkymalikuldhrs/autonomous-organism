import os
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class ProblemRaw(Base):
    __tablename__ = "problem_raw"
    id = Column(Integer, primary_key=True)
    source = Column(String)
    external_id = Column(String, unique=True)
    title = Column(String)
    content = Column(Text)
    url = Column(String)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ProblemClean(Base):
    __tablename__ = "problem_clean"
    id = Column(Integer, primary_key=True)
    raw_id = Column(Integer, ForeignKey("problem_raw.id"))
    text_clean = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class IdeaCandidate(Base):
    __tablename__ = "idea_candidates"
    id = Column(Integer, primary_key=True)
    theme = Column(String)
    score = Column(Float)
    summary = Column(Text)
    technical_spec = Column(Text) # JSON
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    theme = Column(String)
    status = Column(String) # built, deployed, killed
    url = Column(String)
    revenue = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TrafficLog(Base):
    __tablename__ = "traffic_log"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    channel = Column(String)
    clicks = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SystemSetting(Base):
    __tablename__ = "system_settings"
    key = Column(String, primary_key=True)
    value = Column(String)

class LifeLog(Base):
    __tablename__ = "life_log"
    id = Column(Integer, primary_key=True)
    type = Column(String) # info, success, warning, error
    engine = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Database Setup
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./organism.db")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Init settings if empty
    if not db.query(SystemSetting).filter(SystemSetting.key == "system_active").first():
        db.add(SystemSetting(key="system_active", value="true"))
        db.add(SystemSetting(key="system_cycle_seconds", value="3600"))
        db.commit()
    db.close()
