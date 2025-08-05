"""
Database models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Rating(Base):
    """User movie ratings"""
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    movie_id = Column(Integer, index=True, nullable=False)
    rating = Column(Float, nullable=False)  # 1-5 stars
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Rating(user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating})>"

