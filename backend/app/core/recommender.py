"""
Recommendation engine using content-based filtering
"""
import numpy as np
from typing import List, Dict, Any, Optional
from app.core.model_loader import model_loader
from app.db.models import Rating

class RecommendationEngine:
    """Content-based recommendation engine"""
    
    TOP_N = 10  # Default number of recommendations
    MIN_SIMILARITY = 0.3  # Minimum similarity threshold
    RECENCY_WEIGHT = 0.1  # Weight for recency boost
    
    def __init__(self):
        self.model_loader = model_loader
    
    def get_recommendations(
        self,
        user_ratings: List[Rating],
        limit: int = TOP_N,
        exclude_rated: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get recommendations based on user ratings
        
        Args:
            user_ratings: List of user's ratings
            limit: Number of recommendations to return
            exclude_rated: Whether to exclude already rated movies
        
        Returns:
            List of recommended movies with similarity scores
        """
        if not user_ratings:
            return []
        
        # Load models
        similarity_matrix = self.model_loader.similarity_matrix
        movies_metadata = self.model_loader.movies_metadata
        
        # Get movie IDs from ratings
        rated_movie_ids = {rating.movie_id for rating in user_ratings}
        
        # Map movie IDs to indices in similarity matrix
        # Note: This assumes movie IDs match matrix indices (1-indexed to 0-indexed)
        movie_id_to_index = {}
        for movie_id, metadata in movies_metadata.items():
            # Try to map movie_id to index (assuming sequential or 1-indexed)
            idx = movie_id - 1 if movie_id > 0 else None
            if idx is not None and 0 <= idx < len(similarity_matrix):
                movie_id_to_index[movie_id] = idx
        
        # Aggregate similarity scores from all rated movies
        aggregated_scores = np.zeros(len(similarity_matrix))
        
        for rating in user_ratings:
            movie_id = rating.movie_id
            if movie_id not in movie_id_to_index:
                continue
            
            idx = movie_id_to_index[movie_id]
            rating_weight = rating.rating / 5.0  # Normalize to 0-1
            
            # Add weighted similarity scores
            aggregated_scores += similarity_matrix[idx] * rating_weight
        
        # Get top recommendations
        top_indices = np.argsort(aggregated_scores)[::-1]
        
        recommendations = []
        seen_movie_ids = set()
        
        for idx in top_indices:
            if len(recommendations) >= limit:
                break
            
            similarity_score = aggregated_scores[idx]
            if similarity_score < self.MIN_SIMILARITY:
                continue
            
            # Find movie_id for this index
            movie_id = None
            for mid, midx in movie_id_to_index.items():
                if midx == idx:
                    movie_id = mid
                    break
            
            if movie_id is None:
                continue
            
            # Skip if already rated and exclude_rated is True
            if exclude_rated and movie_id in rated_movie_ids:
                continue
            
            # Skip duplicates
            if movie_id in seen_movie_ids:
                continue
            
            # Get movie metadata
            movie_info = movies_metadata.get(movie_id, {})
            
            # Generate reason
            reason = self._generate_reason(movie_info, user_ratings, similarity_score)
            
            recommendations.append({
                'movie_id': movie_id,
                'title': movie_info.get('title', f'Movie {movie_id}'),
                'genres': movie_info.get('genres', ''),
                'year': movie_info.get('year', 0),
                'similarity_score': round(float(similarity_score), 4),
                'reason': reason
            })
            
            seen_movie_ids.add(movie_id)
        
        return recommendations
    
    def _generate_reason(
        self,
        movie_info: Dict,
        user_ratings: List[Rating],
        similarity_score: float
    ) -> str:
        """Generate explanation for recommendation"""
        reasons = []
        
        # Genre match
        movie_genres = set(movie_info.get('genres', '').split('|'))
        rated_genres = set()
        for rating in user_ratings:
            # Would need to get genres from rated movies
            pass
        
        if similarity_score > 0.8:
            reasons.append("Highly similar to your favorite movies")
        elif similarity_score > 0.6:
            reasons.append("Similar to movies you've rated highly")
        else:
            reasons.append("Based on your preferences")
        
        # Add genre info if available
        if movie_genres:
            reasons.append(f"Genres: {', '.join(list(movie_genres)[:3])}")
        
        return ". ".join(reasons) if reasons else "Recommended based on your ratings"
    
    def get_similar_movies(
        self,
        movie_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get movies similar to a given movie"""
        similarity_matrix = self.model_loader.similarity_matrix
        movies_metadata = self.model_loader.movies_metadata
        
        # Map movie_id to index
        movie_id_to_index = {}
        for mid, metadata in movies_metadata.items():
            idx = mid - 1 if mid > 0 else None
            if idx is not None and 0 <= idx < len(similarity_matrix):
                movie_id_to_index[mid] = idx
        
        if movie_id not in movie_id_to_index:
            return []
        
        idx = movie_id_to_index[movie_id]
        similarities = similarity_matrix[idx]
        
        # Get top similar movies (excluding self)
        top_indices = np.argsort(similarities)[::-1][1:limit+1]
        
        similar_movies = []
        for sim_idx in top_indices:
            similarity_score = similarities[sim_idx]
            if similarity_score < self.MIN_SIMILARITY:
                continue
            
            # Find movie_id
            movie_id_sim = None
            for mid, midx in movie_id_to_index.items():
                if midx == sim_idx:
                    movie_id_sim = mid
                    break
            
            if movie_id_sim is None:
                continue
            
            movie_info = movies_metadata.get(movie_id_sim, {})
            similar_movies.append({
                'movie_id': movie_id_sim,
                'title': movie_info.get('title', f'Movie {movie_id_sim}'),
                'genres': movie_info.get('genres', ''),
                'year': movie_info.get('year', 0),
                'similarity_score': round(float(similarity_score), 4)
            })
        
        return similar_movies

