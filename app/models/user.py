from sqlalchemy import Column, Integer, String, DateTime, func
from app.utils.baseModel import BaseModel
import uuid

class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    refresh_token = Column(String, nullable=True)  # To store the refresh token