"""
Ratings API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List
from app.db.database import get_db
from app.db.models import Rating
from datetime import datetime

router = APIRouter()

class RatingCreate(BaseModel):
    user_id: str = Field(..., description="User identifier")
    movie_id: int = Field(..., description="Movie ID", gt=0)
    rating: float = Field(..., description="Rating (1-5 stars)", ge=1, le=5)

class RatingResponse(BaseModel):
    id: int
    user_id: str
    movie_id: int
    rating: float
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/ratings", response_model=RatingResponse)
async def create_rating(rating_data: RatingCreate, db: Session = Depends(get_db)):
    """Create or update a movie rating"""
    # Check if rating already exists
    existing = db.query(Rating).filter(
        Rating.user_id == rating_data.user_id,
        Rating.movie_id == rating_data.movie_id
    ).first()
    
    if existing:
        # Update existing rating
        existing.rating = rating_data.rating
        existing.created_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new rating
        rating = Rating(
            user_id=rating_data.user_id,
            movie_id=rating_data.movie_id,
            rating=rating_data.rating
        )
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return rating

@router.get("/ratings/{user_id}", response_model=List[RatingResponse])
async def get_user_ratings(user_id: str, db: Session = Depends(get_db)):
    """Get all ratings for a user"""
    ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    return ratings

@router.delete("/ratings/{rating_id}")
async def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    """Delete a rating"""
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(rating)
    db.commit()
    return {"message": "Rating deleted"}

