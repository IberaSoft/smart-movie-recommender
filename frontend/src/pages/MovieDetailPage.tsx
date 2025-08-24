import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowLeft, Calendar, Film } from 'lucide-react'
import { moviesApi, ratingsApi } from '@/lib/api'
import RatingStars from '@/components/RatingStars'

const USER_ID = 'user_123'

export default function MovieDetailPage() {
  const { id } = useParams<{ id: string }>()
  const movieId = parseInt(id || '0')
  
  const { data: movie, isLoading } = useQuery({
    queryKey: ['movie', movieId],
    queryFn: () => moviesApi.getById(movieId),
    enabled: !!movieId,
  })
  
  const { data: similarMovies } = useQuery({
    queryKey: ['similar', movieId],
    queryFn: () => moviesApi.getSimilar(movieId, 6),
    enabled: !!movieId,
  })
  
  const { data: userRatings } = useQuery({
    queryKey: ['ratings', USER_ID],
    queryFn: () => ratingsApi.getUserRatings(USER_ID),
  })
  
  const userRating = userRatings?.find(r => r.movie_id === movieId)?.rating
  
  const handleRate = async (rating: number) => {
    try {
      await ratingsApi.create(USER_ID, movieId, rating)
      window.location.reload()
    } catch (error) {
      console.error('Failed to rate movie:', error)
    }
  }
  
  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center text-slate-400">Loading...</div>
      </div>
    )
  }
  
  if (!movie) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center text-slate-400">Movie not found</div>
      </div>
    )
  }
  
  const genres = movie.genres?.split('|').filter(Boolean) || []
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Link
        to="/movies"
        className="inline-flex items-center text-slate-400 hover:text-white mb-6"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Movies
      </Link>
      
      <div className="bg-slate-800 rounded-lg p-8 mb-8">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-4xl font-bold text-white mb-4">{movie.title}</h1>
            <div className="flex items-center space-x-4 text-slate-300">
              {movie.year > 0 && (
                <div className="flex items-center">
                  <Calendar className="h-5 w-5 mr-2" />
                  <span>{movie.year}</span>
                </div>
              )}
            </div>
          </div>
        </div>
        
        <div className="flex flex-wrap gap-2 mb-6">
          {genres.map((genre, idx) => (
            <span
              key={idx}
              className="px-3 py-1 bg-slate-700 text-slate-300 rounded-full text-sm"
            >
              {genre}
            </span>
          ))}
        </div>
        
        {movie.plot && (
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-white mb-2">Plot</h2>
            <p className="text-slate-300">{movie.plot}</p>
          </div>
        )}
        
        <div className="border-t border-slate-700 pt-6">
          <h3 className="text-lg font-semibold text-white mb-4">Rate this movie</h3>
          <div className="flex items-center space-x-4">
            <RatingStars
              rating={userRating || 0}
              interactive
              onRate={handleRate}
              size="lg"
            />
            {userRating && (
              <span className="text-slate-400">Your rating: {userRating}/5</span>
            )}
          </div>
        </div>
      </div>
      
      {similarMovies && similarMovies.similar_movies.length > 0 && (
        <div>
          <h2 className="text-2xl font-semibold text-white mb-4">Similar Movies</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {similarMovies.similar_movies.map((similar) => (
              <Link
                key={similar.id}
                to={`/movies/${similar.id}`}
                className="bg-slate-800 rounded-lg p-4 hover:bg-slate-700 transition-colors"
              >
                <h3 className="text-lg font-semibold text-white mb-2">{similar.title}</h3>
                <div className="flex items-center text-sm text-slate-400 mb-2">
                  {similar.year > 0 && <span>{similar.year}</span>}
                </div>
                <div className="text-xs text-slate-500">
                  Similarity: {((similar as any).similarity_score * 100).toFixed(0)}%
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

