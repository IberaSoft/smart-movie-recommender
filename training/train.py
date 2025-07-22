#!/usr/bin/env python3
"""
Train content-based recommendation model using TF-IDF and cosine similarity
"""
import argparse
import json
import pickle
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

def load_data(data_path):
    """Load movie data from CSV"""
    print(f"Loading movies from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} movies")
    return df

def create_features(df):
    """Create combined text features from movie metadata"""
    print("Creating features from genres, cast, directors...")
    
    # Combine all text features
    features = []
    for _, row in df.iterrows():
        feature_parts = []
        
        # Add genres (repeat for weight)
        if pd.notna(row.get('genres')):
            genres = str(row['genres']).replace('|', ' ')
            feature_parts.extend([genres] * 3)  # Weight genres more
        
        # Add director
        if pd.notna(row.get('director')) and str(row['director']) != 'Unknown':
            feature_parts.append(str(row['director']))
        
        # Add cast
        if pd.notna(row.get('cast')) and str(row['cast']) != 'Unknown':
            cast = str(row['cast']).replace('|', ' ')
            feature_parts.append(cast)
        
        # Add plot
        if pd.notna(row.get('plot')):
            feature_parts.append(str(row['plot']))
        
        # Add year as text (for temporal similarity)
        if pd.notna(row.get('year')) and row['year'] > 0:
            feature_parts.append(f"year_{int(row['year'])}")
        
        combined = ' '.join(feature_parts)
        features.append(combined)
    
    return features

def train_model(df, features):
    """Train TF-IDF vectorizer and compute similarity matrix"""
    print("Computing TF-IDF vectors...")
    
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),  # Unigrams and bigrams
        min_df=2,  # Minimum document frequency
        max_df=0.95,  # Maximum document frequency
        stop_words='english'
    )
    
    # Fit and transform
    tfidf_matrix = vectorizer.fit_transform(features)
    print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
    
    print("Calculating similarity matrix...")
    start_time = time.time()
    
    # Compute cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    elapsed = time.time() - start_time
    print(f"Similarity matrix computed in {elapsed:.2f}s")
    print(f"Similarity matrix shape: {similarity_matrix.shape}")
    
    return vectorizer, similarity_matrix

def evaluate_model(df, similarity_matrix):
    """Evaluate model performance"""
    print("\nEvaluating model...")
    
    # Calculate coverage (how many movies are recommended at least once)
    # Simulate recommendations for all movies
    recommended_movies = set()
    for i in range(len(df)):
        # Get top 10 similar movies (excluding self)
        similar_indices = np.argsort(similarity_matrix[i])[::-1][1:11]
        recommended_movies.update(similar_indices)
    
    coverage = len(recommended_movies) / len(df) * 100
    
    # Calculate average similarity score
    # Get average similarity for top recommendations
    avg_similarities = []
    for i in range(len(df)):
        similar_indices = np.argsort(similarity_matrix[i])[::-1][1:11]
        avg_sim = np.mean([similarity_matrix[i][idx] for idx in similar_indices])
        avg_similarities.append(avg_sim)
    
    avg_similarity = np.mean(avg_similarities)
    
    metrics = {
        'coverage': round(coverage, 2),
        'avg_similarity': round(avg_similarity, 2),
        'num_movies': len(df),
        'similarity_matrix_shape': list(similarity_matrix.shape)
    }
    
    print(f"Coverage: {metrics['coverage']}% of movies recommended at least once")
    print(f"Avg similarity score: {metrics['avg_similarity']}")
    
    return metrics

def save_model(vectorizer, similarity_matrix, df, output_dir, metrics):
    """Save trained model and metadata"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("\nSaving models...")
    
    # Save similarity matrix
    similarity_path = output_path / "similarity_matrix.pkl"
    with open(similarity_path, 'wb') as f:
        pickle.dump(similarity_matrix, f)
    print(f"✓ Saved similarity matrix to {similarity_path}")
    
    # Save vectorizer
    vectorizer_path = output_path / "tfidf_vectorizer.pkl"
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"✓ Saved TF-IDF vectorizer to {vectorizer_path}")
    
    # Save movie metadata (for quick lookup)
    movies_metadata = df[['id', 'title', 'genres', 'year']].to_dict('records')
    movies_path = output_path / "movies_metadata.json"
    with open(movies_path, 'w') as f:
        json.dump(movies_metadata, f, indent=2)
    print(f"✓ Saved movies metadata to {movies_path}")
    
    # Save model metrics
    metadata = {
        'metrics': metrics,
        'model_version': '1.0.0',
        'algorithm': 'TF-IDF + Cosine Similarity',
        'training_date': pd.Timestamp.now().isoformat()
    }
    metadata_path = output_path / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Saved model metadata to {metadata_path}")
    
    print(f"\n✓ Model saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Train content-based recommendation model')
    parser.add_argument('--data', type=str, default='data/movies.csv',
                       help='Path to movies CSV file')
    parser.add_argument('--output', type=str, default='models/',
                       help='Output directory for models')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Content-Based Movie Recommendation Model Training")
    print("=" * 60)
    
    # Load data
    data_path = Path(__file__).parent / args.data
    df = load_data(data_path)
    
    # Create features
    features = create_features(df)
    
    # Train model
    vectorizer, similarity_matrix = train_model(df, features)
    
    # Evaluate
    metrics = evaluate_model(df, similarity_matrix)
    
    # Save model
    output_dir = Path(__file__).parent / args.output
    save_model(vectorizer, similarity_matrix, df, output_dir, metrics)
    
    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)
    print("\nEvaluation Metrics:")
    print(f"- Coverage: {metrics['coverage']}%")
    print(f"- Avg similarity score: {metrics['avg_similarity']}")

if __name__ == "__main__":
    main()

