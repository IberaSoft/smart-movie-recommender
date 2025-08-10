"""
Recommendations API endpoints
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Rating
from app.core.recommender import RecommendationEngine

router = APIRouter()
recommender = RecommendationEngine()

@router.get("/recommendations/{user_id}")
async def get_recommendations(
    user_id: str,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get personalized movie recommendations for a user"""
    # Get user's ratings
    user_ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    
    if not user_ratings:
        raise HTTPException(
            status_code=400,
            detail="No ratings found. Please rate some movies first."
        )
    
    # Get recommendations
    recommendations = recommender.get_recommendations(
        user_ratings=user_ratings,
        limit=limit,
        exclude_rated=True
    )
    
    return {
        "user_id": user_id,
        "recommendations": recommendations,
        "count": len(recommendations)
    }

@router.get("/movies/{movie_id}/similar")
async def get_similar_movies(
    movie_id: int,
    limit: int = Query(10, ge=1, le=50)
):
    """Get movies similar to a given movie"""
    similar_movies = recommender.get_similar_movies(movie_id, limit=limit)
    
    if not similar_movies:
        raise HTTPException(status_code=404, detail="Movie not found or no similar movies")
    
    return {
        "movie_id": movie_id,
        "similar_movies": similar_movies,
        "count": len(similar_movies)
    }

