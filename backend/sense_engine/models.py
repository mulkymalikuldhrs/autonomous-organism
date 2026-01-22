from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class ProblemRaw(Base):
    __tablename__ = 'problem_raw'
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    text = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)

class ProblemClean(Base):
    __tablename__ = 'problem_clean'
    id = Column(Integer, primary_key=True, index=True)
    text_clean = Column(String)
    raw_id = Column(Integer, ForeignKey('problem_raw.id'))
