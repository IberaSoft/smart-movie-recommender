#!/usr/bin/env python3
"""
Seed database with initial data (optional)
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import engine, Base
from app.db.models import Rating

def seed_database():
    """Create database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

if __name__ == "__main__":
    seed_database()

