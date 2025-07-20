from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):

  __tablename__ = "users"

  uuid = Column(Integer, primary_key=True, unique=True, index=True)
  username = Column(Integer, unique=True, index=True)