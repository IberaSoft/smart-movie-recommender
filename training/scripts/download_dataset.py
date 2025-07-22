#!/usr/bin/env python3
"""
Download MovieLens 100K dataset and prepare movies.csv
"""
import os
import sys
import requests
import zipfile
import pandas as pd
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

MOVIELENS_URL = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
ZIP_PATH = DATA_DIR / "ml-100k.zip"
EXTRACT_DIR = DATA_DIR / "ml-100k"

def download_file(url, dest_path):
    """Download a file from URL"""
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end=''")
                sys.stdout.flush()
    
    print(f"\nDownloaded to {dest_path}")

def extract_zip(zip_path, extract_dir):
    """Extract zip file"""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir.parent)
    print(f"Extracted to {extract_dir}")

def prepare_movies_csv():
    """Combine MovieLens data into movies.csv"""
    print("Preparing movies.csv...")
    
    # Read MovieLens files
    movies_file = EXTRACT_DIR / "u.item"
    ratings_file = EXTRACT_DIR / "u.data"
    users_file = EXTRACT_DIR / "u.user"
    
    # Parse movies (format: movie_id|title|release_date|...|genres)
    movies_data = []
    with open(movies_file, 'r', encoding='latin-1') as f:
        for line in f:
            parts = line.strip().split('|')
            movie_id = int(parts[0])
            title = parts[1]
            release_date = parts[2]
            # Genres are last 19 fields (binary indicators)
            genres = parts[5:]
            
            # Convert genre indicators to genre names
            genre_names = [
                "Action", "Adventure", "Animation", "Children's", "Comedy",
                "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir",
                "Horror", "Musical", "Mystery", "Romance", "Sci-Fi",
                "Thriller", "War", "Western"
            ]
            movie_genres = [genre_names[i] for i, val in enumerate(genres) if val == '1']
            
            # Extract year from release date
            year = None
            if release_date and release_date != "NULL":
                try:
                    year = int(release_date.split('-')[-1])
                    if year < 1900:
                        year = None
                except:
                    pass
            
            movies_data.append({
                'id': movie_id,
                'title': title,
                'genres': '|'.join(movie_genres) if movie_genres else 'Unknown',
                'year': year if year else 0,
                'director': 'Unknown',  # MovieLens 100K doesn't have director
                'cast': 'Unknown',  # MovieLens 100K doesn't have cast
                'plot': f"A {', '.join(movie_genres) if movie_genres else 'movie'} from {year if year else 'unknown year'}."
            })
    
    # Create DataFrame
    df = pd.DataFrame(movies_data)
    
    # Limit to 1000 movies as mentioned in README
    df = df.head(1000)
    
    # Save to CSV
    output_path = DATA_DIR / "movies.csv"
    df.to_csv(output_path, index=False)
    print(f"✓ Created {output_path} with {len(df)} movies")
    
    return output_path

def main():
    """Main function"""
    print("=" * 60)
    print("MovieLens 100K Dataset Downloader")
    print("=" * 60)
    
    # Download if not exists
    if not ZIP_PATH.exists():
        download_file(MOVIELENS_URL, ZIP_PATH)
    else:
        print(f"Zip file already exists: {ZIP_PATH}")
    
    # Extract if not exists
    if not EXTRACT_DIR.exists():
        extract_zip(ZIP_PATH, EXTRACT_DIR)
    else:
        print(f"Extracted files already exist: {EXTRACT_DIR}")
    
    # Prepare movies.csv
    if not (DATA_DIR / "movies.csv").exists():
        prepare_movies_csv()
    else:
        print(f"movies.csv already exists: {DATA_DIR / 'movies.csv'}")
    
    print("\n✓ Dataset preparation complete!")
    print(f"Movies CSV: {DATA_DIR / 'movies.csv'}")

if __name__ == "__main__":
    main()

