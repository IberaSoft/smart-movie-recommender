import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Sparkles, Film, TrendingUp } from 'lucide-react'
import { moviesApi, recommendationsApi } from '@/lib/api'
import MovieCard from '@/components/MovieCard'

const USER_ID = 'user_123' // In production, this would come from auth

export default function HomePage() {
  const [userId] = useState(USER_ID)
  
  const { data: moviesData } = useQuery({
    queryKey: ['movies', 'home', 1],
    queryFn: () => moviesApi.getAll(1, 6),
  })
  
  const { data: recommendationsData } = useQuery({
    queryKey: ['recommendations', userId],
    queryFn: () => recommendationsApi.getRecommendations(userId, 6),
    enabled: false, // Only fetch when user has ratings
  })
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-white mb-4">
          🎬 Smart Movie Recommender
        </h1>
        <p className="text-xl text-slate-300">
          Discover your next favorite movie with AI-powered recommendations
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div className="bg-slate-800 rounded-lg p-6">
          <div className="flex items-center mb-4">
            <Film className="h-6 w-6 text-blue-400 mr-2" />
            <h2 className="text-xl font-semibold text-white">Browse Movies</h2>
          </div>
          <p className="text-slate-300 mb-4">
            Explore our collection of 1,000+ movies across all genres. Rate movies you've watched to get personalized recommendations.
          </p>
          <a
            href="/movies"
            className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            Browse All Movies
          </a>
        </div>
        
        <div className="bg-slate-800 rounded-lg p-6">
          <div className="flex items-center mb-4">
            <Sparkles className="h-6 w-6 text-purple-400 mr-2" />
            <h2 className="text-xl font-semibold text-white">Get Recommendations</h2>
          </div>
          <p className="text-slate-300 mb-4">
            Rate at least one movie to receive personalized recommendations based on your taste using content-based filtering.
          </p>
          <a
            href="/recommendations"
            className="inline-block px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors"
          >
            View Recommendations
          </a>
        </div>
      </div>
      
      {moviesData && (
        <div className="mb-12">
          <div className="flex items-center mb-4">
            <TrendingUp className="h-5 w-5 text-green-400 mr-2" />
            <h2 className="text-2xl font-semibold text-white">Popular Movies</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {moviesData.movies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        </div>
      )}
      
      {recommendationsData && recommendationsData.recommendations.length > 0 && (
        <div>
          <div className="flex items-center mb-4">
            <Sparkles className="h-5 w-5 text-yellow-400 mr-2" />
            <h2 className="text-2xl font-semibold text-white">Recommended for You</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {recommendationsData.recommendations.map((rec) => (
              <MovieCard
                key={rec.movie_id}
                movie={{
                  id: rec.movie_id,
                  title: rec.title,
                  genres: rec.genres,
                  year: rec.year,
                }}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

