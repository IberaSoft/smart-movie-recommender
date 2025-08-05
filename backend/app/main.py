"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import movies, ratings, recommendations
from app.db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Movie Recommender API",
    description="Content-based movie recommendation system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router, prefix="/api", tags=["movies"])
app.include_router(ratings.router, prefix="/api", tags=["ratings"])
app.include_router(recommendations.router, prefix="/api", tags=["recommendations"])

@app.get("/")
async def root():
    return {
        "message": "Smart Movie Recommender API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

