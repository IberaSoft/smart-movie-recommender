import { Star } from 'lucide-react'

interface RatingStarsProps {
  rating: number
  maxRating?: number
  size?: 'sm' | 'md' | 'lg'
  interactive?: boolean
  onRate?: (rating: number) => void
}

export default function RatingStars({ 
  rating, 
  maxRating = 5, 
  size = 'md',
  interactive = false,
  onRate 
}: RatingStarsProps) {
  const sizeClasses = {
    sm: 'h-3 w-3',
    md: 'h-4 w-4',
    lg: 'h-6 w-6'
  }
  
  return (
    <div className="flex items-center">
      {Array.from({ length: maxRating }, (_, i) => i + 1).map((star) => (
        <button
          key={star}
          onClick={() => interactive && onRate && onRate(star)}
          disabled={!interactive}
          className={`${sizeClasses[size]} ${
            star <= rating
              ? 'text-yellow-400'
              : 'text-slate-500'
          } ${
            interactive 
              ? 'hover:text-yellow-400 cursor-pointer transition-colors' 
              : ''
          }`}
        >
          <Star className="fill-current" />
        </button>
      ))}
    </div>
  )
}

