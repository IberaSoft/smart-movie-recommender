import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Search, Filter } from 'lucide-react'
import { moviesApi, ratingsApi } from '@/lib/api'
import MovieCard from '@/components/MovieCard'

const USER_ID = 'user_123'

export default function MoviesPage() {
  const [page, setPage] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedGenre, setSelectedGenre] = useState<string>('')
  const [selectedYear, setSelectedYear] = useState<number | undefined>()
  
  const { data: moviesData, isLoading } = useQuery({
    queryKey: ['movies', page, selectedGenre, selectedYear],
    queryFn: () => moviesApi.getAll(page, 20, selectedGenre || undefined, selectedYear),
  })
  
  const { data: searchResults } = useQuery({
    queryKey: ['movies', 'search', searchQuery, selectedGenre],
    queryFn: () => moviesApi.search(searchQuery, selectedGenre || undefined),
    enabled: searchQuery.length > 0,
  })
  
  const { data: userRatings } = useQuery({
    queryKey: ['ratings', USER_ID],
    queryFn: () => ratingsApi.getUserRatings(USER_ID),
  })
  
  const ratingsMap = new Map(
    userRatings?.map(r => [r.movie_id, r.rating]) || []
  )
  
  const handleRate = async (movieId: number, rating: number) => {
    try {
      await ratingsApi.create(USER_ID, movieId, rating)
      // Refetch ratings
      window.location.reload()
    } catch (error) {
      console.error('Failed to rate movie:', error)
    }
  }
  
  const movies = searchQuery && searchResults 
    ? searchResults.results 
    : moviesData?.movies || []
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-white mb-6">Browse Movies</h1>
      
      <div className="mb-6 space-y-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search movies by title..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div className="flex flex-wrap gap-4 items-center">
          <div className="flex items-center">
            <Filter className="h-5 w-5 text-slate-400 mr-2" />
            <span className="text-slate-300 mr-2">Filter:</span>
          </div>
          
          <select
            value={selectedGenre}
            onChange={(e) => {
              setSelectedGenre(e.target.value)
              setPage(1)
            }}
            className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Genres</option>
            <option value="Action">Action</option>
            <option value="Adventure">Adventure</option>
            <option value="Animation">Animation</option>
            <option value="Comedy">Comedy</option>
            <option value="Crime">Crime</option>
            <option value="Drama">Drama</option>
            <option value="Fantasy">Fantasy</option>
            <option value="Horror">Horror</option>
            <option value="Romance">Romance</option>
            <option value="Sci-Fi">Sci-Fi</option>
            <option value="Thriller">Thriller</option>
          </select>
          
          <input
            type="number"
            placeholder="Year"
            value={selectedYear || ''}
            onChange={(e) => {
              const year = e.target.value ? parseInt(e.target.value) : undefined
              setSelectedYear(year)
              setPage(1)
            }}
            className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 w-32"
          />
        </div>
      </div>
      
      {isLoading ? (
        <div className="text-center py-12">
          <div className="text-slate-400">Loading movies...</div>
        </div>
      ) : movies.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-slate-400">No movies found.</div>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            {movies.map((movie) => (
              <MovieCard
                key={movie.id}
                movie={movie}
                userRating={ratingsMap.get(movie.id)}
                onRate={handleRate}
              />
            ))}
          </div>
          
          {!searchQuery && moviesData && (
            <div className="flex justify-center items-center space-x-4">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 bg-slate-700 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-600"
              >
                Previous
              </button>
              <span className="text-slate-300">
                Page {page} of {moviesData.pages}
              </span>
              <button
                onClick={() => setPage(p => Math.min(moviesData.pages, p + 1))}
                disabled={page >= moviesData.pages}
                className="px-4 py-2 bg-slate-700 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-600"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

