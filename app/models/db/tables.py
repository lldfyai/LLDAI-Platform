from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Enum
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from models.db.enums import Difficulty

Base = declarative_base()

class UserMetadata(Base):
    __tablename__ = 'UserMetadata'
    userId = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    userName = Column(String(255), nullable=True)  # Nullable as per schema
    problemsSolved = Column(Integer, nullable=True, default=0, server_default='0')
    rank = Column(Integer, nullable=True, default=0, server_default='0')
    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())  # Default to CURRENT_TIMESTAMP

class ProblemMetadata(Base):
    __tablename__ = 'ProblemMetadata'
    problemId = Column(Integer, primary_key=True, autoincrement=True)
    problemTitle = Column(String(255), nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False)  # Enum for difficulty
    timeLimit = Column(Float, nullable=True)  # Double precision in PostgreSQL
    memoryLimit = Column(Float, nullable=True)  # Double precision in PostgreSQL
    tags = Column(ARRAY(String), nullable=False, default=[], server_default='{}')  # Array of strings with default '{}'