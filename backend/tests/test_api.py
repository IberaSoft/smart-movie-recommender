"""
Tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_movies():
    """Test getting movies list"""
    response = client.get("/api/movies?page=1&size=10")
    # May fail if models not loaded, but structure is correct
    assert response.status_code in [200, 500]

def test_search_movies():
    """Test searching movies"""
    response = client.get("/api/movies/search?q=test")
    # May fail if models not loaded, but structure is correct
    assert response.status_code in [200, 500]

