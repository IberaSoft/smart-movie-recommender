import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import MoviesPage from './pages/MoviesPage'
import RecommendationsPage from './pages/RecommendationsPage'
import MovieDetailPage from './pages/MovieDetailPage'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/movies" element={<MoviesPage />} />
        <Route path="/movies/:id" element={<MovieDetailPage />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
      </Routes>
    </Layout>
  )
}

export default App

