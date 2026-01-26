from sqlalchemy import Column, Integer, String, DateTime, Enum
from ..database import Base
import datetime
import enum

class LogType(enum.Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"

class LifeLog(Base):
    __tablename__ = 'life_log'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    log_type = Column(Enum(LogType))
    name = Column(String)
    result = Column(String)
    reason = Column(String)
