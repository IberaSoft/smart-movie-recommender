import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Movie {
  id: number
  title: string
  genres: string
  year: number
  director?: string
  cast?: string
  plot?: string
}

export interface Rating {
  id: number
  user_id: string
  movie_id: number
  rating: number
  created_at: string
}

export interface Recommendation {
  movie_id: number
  title: string
  genres: string
  year: number
  similarity_score: number
  reason: string
}

export interface MoviesResponse {
  movies: Movie[]
  total: number
  page: number
  size: number
  pages: number
}

export const moviesApi = {
  getAll: async (page = 1, size = 20, genre?: string, year?: number): Promise<MoviesResponse> => {
    const params: any = { page, size }
    if (genre) params.genre = genre
    if (year) params.year = year
    const { data } = await api.get('/api/movies', { params })
    return data
  },
  
  search: async (query: string, genre?: string): Promise<{ results: Movie[] }> => {
    const params: any = { q: query }
    if (genre) params.genre = genre
    const { data } = await api.get('/api/movies/search', { params })
    return data
  },
  
  getById: async (id: number): Promise<Movie> => {
    const { data } = await api.get(`/api/movies/${id}`)
    return data
  },
  
  getSimilar: async (id: number, limit = 10): Promise<{ similar_movies: Movie[] }> => {
    const { data } = await api.get(`/api/movies/${id}/similar`, { params: { limit } })
    return data
  },
}

export const ratingsApi = {
  create: async (user_id: string, movie_id: number, rating: number): Promise<Rating> => {
    const { data } = await api.post('/api/ratings', { user_id, movie_id, rating })
    return data
  },
  
  getUserRatings: async (user_id: string): Promise<Rating[]> => {
    const { data } = await api.get(`/api/ratings/${user_id}`)
    return data
  },
  
  delete: async (rating_id: number): Promise<void> => {
    await api.delete(`/api/ratings/${rating_id}`)
  },
}

export const recommendationsApi = {
  getRecommendations: async (user_id: string, limit = 10): Promise<{ recommendations: Recommendation[] }> => {
    const { data } = await api.get(`/api/recommendations/${user_id}`, { params: { limit } })
    return data
  },
}

export default api

