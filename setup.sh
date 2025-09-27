#!/bin/bash
# Setup script for Smart Movie Recommender

set -e

echo "🎬 Smart Movie Recommender - Setup Script"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env 2>/dev/null || echo "Note: .env.example not found, you may need to create .env manually"
fi

# Start Docker containers
echo ""
echo "Starting Docker containers..."
docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 5

# Download dataset and train model
echo ""
echo "Downloading MovieLens dataset..."
docker-compose exec -T backend python -c "
import sys
sys.path.insert(0, '/app/../training')
from scripts.download_dataset import main
main()
" || docker-compose exec backend bash -c "cd /app/../training && python scripts/download_dataset.py"

echo ""
echo "Training recommendation model..."
docker-compose exec backend bash -c "cd /app/../training && python train.py"

echo ""
echo "✓ Setup complete!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "📡 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "To stop the services, run: docker-compose down"

