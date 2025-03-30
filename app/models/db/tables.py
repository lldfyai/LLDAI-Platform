from sqlalchemy import Column, Integer, String, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from models.db.enums import Difficulty


Base = declarative_base()

class UserMetadata(Base):
    __tablename__ = 'UserMetadata'
    userId = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    userName = Column(String(255), nullable=False)
    password = Column(String(60), nullable=False)

class ProblemMetadata(Base):
    __tablename__ = 'ProblemMetadata'
    problemId = Column(Integer, primary_key=True, autoincrement=True)
    problemTitle = Column(String(255), nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False)
    tags = Column(ARRAY(String), nullable=False, default=[], server_default='{}')
    timeLimit = Column(Float, nullable=True)
    memoryLimit = Column(Float, nullable=True)