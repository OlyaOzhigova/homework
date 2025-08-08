from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Advertisement(Base):
    __tablename__ = "advertisements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Integer, nullable=False)
    author = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())