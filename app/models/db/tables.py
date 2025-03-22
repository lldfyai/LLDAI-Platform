from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserMetadata(Base):
    __tablename__ = 'UserMetadata'
    userId = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    userName = Column(String(250), nullable=False)
    password = Column(String(60), nullable=False)