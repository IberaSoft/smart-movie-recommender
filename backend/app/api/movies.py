"""
Movies API endpoints
"""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.core.model_loader import model_loader
import json

router = APIRouter()

@router.get("/movies")
async def get_movies(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    genre: Optional[str] = None,
    year: Optional[int] = None
):
    """Get paginated list of movies"""
    movies_metadata = model_loader.movies_metadata
    
    # Convert to list
    movies = list(movies_metadata.values())
    
    # Filter by genre
    if genre:
        movies = [m for m in movies if genre.lower() in str(m.get('genres', '')).lower()]
    
    # Filter by year
    if year:
        movies = [m for m in movies if m.get('year') == year]
    
    # Paginate
    total = len(movies)
    start = (page - 1) * size
    end = start + size
    paginated_movies = movies[start:end]
    
    return {
        "movies": paginated_movies,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }

@router.get("/movies/search")
async def search_movies(
    q: str = Query(..., min_length=1),
    genre: Optional[str] = None
):
    """Search movies by title"""
    movies_metadata = model_loader.movies_metadata
    
    query_lower = q.lower()
    results = []
    
    for movie_id, movie in movies_metadata.items():
        title = str(movie.get('title', '')).lower()
        
        if query_lower in title:
            # Filter by genre if provided
            if genre:
                movie_genres = str(movie.get('genres', '')).lower()
                if genre.lower() not in movie_genres:
                    continue
            
            results.append({
                'id': movie_id,
                **movie
            })
    
    return {"results": results[:50]}  # Limit to 50 results

@router.get("/movies/{movie_id}")
async def get_movie(movie_id: int):
    """Get movie details by ID"""
    movies_metadata = model_loader.movies_metadata
    
    if movie_id not in movies_metadata:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie = movies_metadata[movie_id].copy()
    movie['id'] = movie_id
    
    return movie

