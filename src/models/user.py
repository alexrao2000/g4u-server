from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):

  __tablename__ = "users"

  uuid = Column(String, primary_key=True, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password = Column(String)