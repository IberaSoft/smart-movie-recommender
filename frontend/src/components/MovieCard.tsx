import { Link } from 'react-router-dom'
import { Star, Calendar } from 'lucide-react'
import { Movie } from '@/lib/api'

interface MovieCardProps {
  movie: Movie
  userRating?: number
  onRate?: (movieId: number, rating: number) => void
}

export default function MovieCard({ movie, userRating, onRate }: MovieCardProps) {
  const genres = movie.genres?.split('|').filter(Boolean) || []
  
  return (
    <div className="bg-slate-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
      <div className="p-4">
        <Link to={`/movies/${movie.id}`}>
          <h3 className="text-lg font-semibold text-white mb-2 hover:text-blue-400 transition-colors">
            {movie.title}
          </h3>
        </Link>
        
        <div className="flex items-center text-sm text-slate-400 mb-2">
          {movie.year > 0 && (
            <>
              <Calendar className="h-4 w-4 mr-1" />
              <span>{movie.year}</span>
            </>
          )}
        </div>
        
        <div className="flex flex-wrap gap-1 mb-3">
          {genres.slice(0, 3).map((genre, idx) => (
            <span
              key={idx}
              className="px-2 py-1 bg-slate-700 text-slate-300 text-xs rounded"
            >
              {genre}
            </span>
          ))}
        </div>
        
        {onRate && (
          <div className="mt-3 pt-3 border-t border-slate-700">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400">Your rating:</span>
              <div className="flex">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    onClick={() => onRate(movie.id, star)}
                    className={`p-1 ${
                      userRating && star <= userRating
                        ? 'text-yellow-400'
                        : 'text-slate-500 hover:text-yellow-400'
                    } transition-colors`}
                  >
                    <Star className="h-4 w-4 fill-current" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

