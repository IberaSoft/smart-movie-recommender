import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Sparkles, AlertCircle } from 'lucide-react'
import { recommendationsApi, ratingsApi } from '@/lib/api'
import MovieCard from '@/components/MovieCard'
import { Link } from 'react-router-dom'

const USER_ID = 'user_123'

export default function RecommendationsPage() {
  const { data: recommendationsData, isLoading, error } = useQuery({
    queryKey: ['recommendations', USER_ID],
    queryFn: () => recommendationsApi.getRecommendations(USER_ID, 10),
  })
  
  const { data: userRatings } = useQuery({
    queryKey: ['ratings', USER_ID],
    queryFn: () => ratingsApi.getUserRatings(USER_ID),
  })
  
  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center text-slate-400">Loading recommendations...</div>
      </div>
    )
  }
  
  if (error || !recommendationsData || recommendationsData.recommendations.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-slate-800 rounded-lg p-8 text-center">
          <AlertCircle className="h-12 w-12 text-yellow-400 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-white mb-4">
            No Recommendations Yet
          </h2>
          <p className="text-slate-300 mb-6">
            Rate at least one movie to get personalized recommendations based on your taste.
          </p>
          <Link
            to="/movies"
            className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Browse Movies
          </Link>
        </div>
      </div>
    )
  }
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center mb-6">
        <Sparkles className="h-8 w-8 text-yellow-400 mr-3" />
        <h1 className="text-3xl font-bold text-white">Your Recommendations</h1>
      </div>
      
      <div className="bg-slate-800 rounded-lg p-6 mb-6">
        <p className="text-slate-300">
          Based on your {userRatings?.length || 0} rating{userRatings?.length !== 1 ? 's' : ''}, 
          here are movies we think you'll enjoy:
        </p>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {recommendationsData.recommendations.map((rec) => (
          <div key={rec.movie_id} className="bg-slate-800 rounded-lg p-6">
            <MovieCard
              movie={{
                id: rec.movie_id,
                title: rec.title,
                genres: rec.genres,
                year: rec.year,
              }}
            />
            <div className="mt-4 pt-4 border-t border-slate-700">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-400">Similarity Score</span>
                <span className="text-sm font-semibold text-green-400">
                  {(rec.similarity_score * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-sm text-slate-300 italic">{rec.reason}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

