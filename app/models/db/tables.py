from sqlalchemy import Column, Integer, String, Enum, Float, DateTime, ForeignKey
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Enum
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY, UUID
import uuid
from datetime import datetime
from models.db.enums import Difficulty, Language, SubmissionState

Base = declarative_base()

class UserMetadata(Base):
    __tablename__ = 'UserMetadata'
    userId = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=True)
    userName = Column(String(255), nullable=True)
    password = Column(String(60), nullable=True)

class ProblemMetadata(Base):
    __tablename__ = 'ProblemMetadata'
    problemId = Column(Integer, primary_key=True, autoincrement=True)
    problemTitle = Column(String(255), nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False)  # Enum for difficulty
    timeLimit = Column(Float, nullable=True)  # Double precision in PostgreSQL
    memoryLimit = Column(Float, nullable=True)  # Double precision in PostgreSQL
    tags = Column(ARRAY(String), nullable=False, default=[], server_default='{}')  # Array of strings with default '{}'

class SubmissionMetadata(Base):
    __tablename__ = 'SubmissionMetadata'    
    submissionId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problemId = Column(Integer, nullable=True)
    userId = Column(Integer, nullable=True)
    language = Column(Enum(Language), nullable=True)
    state = Column(Enum(SubmissionState), nullable=True)
    statusCode = Column(Integer, nullable=True)
    testsPassed = Column(Integer, nullable=True)
    totalTests = Column(Integer, nullable=True)
    executionTime = Column(Float, nullable=True)
    memory = Column(Float, nullable=True)
    createdAt = Column(DateTime, nullable=True, default=datetime.utcnow)