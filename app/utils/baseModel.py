from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    # Auto-generated UUID for primary key
    id = Column(Integer, primary_key=True, default=lambda: uuid.uuid4().int & (1<<63)-1)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())