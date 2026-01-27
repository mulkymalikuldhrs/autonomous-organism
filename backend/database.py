from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProblemRaw(Base):
    __tablename__ = "problem_raw"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    text = Column(Text)
    date = Column(Date, default=datetime.date.today)

class ProblemClean(Base):
    __tablename__ = "problem_clean"
    id = Column(Integer, primary_key=True, index=True)
    text_clean = Column(Text)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_db_and_tables()
