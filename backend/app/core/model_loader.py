"""
Load trained ML models
"""
import pickle
import json
from pathlib import Path
from typing import Optional, Dict, Any
import numpy as np
from app.core.config import settings

class ModelLoader:
    """Singleton model loader"""
    _instance = None
    _similarity_matrix: Optional[np.ndarray] = None
    _vectorizer: Optional[Any] = None
    _movies_metadata: Optional[Dict[int, Dict]] = None
    _model_metadata: Optional[Dict] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def load_models(self) -> bool:
        """Load all model files"""
        model_path = Path(settings.MODEL_PATH)
        
        try:
            # Load similarity matrix
            similarity_path = model_path / "similarity_matrix.pkl"
            if not similarity_path.exists():
                raise FileNotFoundError(f"Similarity matrix not found: {similarity_path}")
            
            with open(similarity_path, 'rb') as f:
                self._similarity_matrix = pickle.load(f)
            
            # Load vectorizer
            vectorizer_path = model_path / "tfidf_vectorizer.pkl"
            if vectorizer_path.exists():
                with open(vectorizer_path, 'rb') as f:
                    self._vectorizer = pickle.load(f)
            
            # Load movies metadata
            movies_path = model_path / "movies_metadata.json"
            if movies_path.exists():
                with open(movies_path, 'r') as f:
                    movies_list = json.load(f)
                    self._movies_metadata = {movie['id']: movie for movie in movies_list}
            
            # Load model metadata
            metadata_path = model_path / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    self._model_metadata = json.load(f)
            
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    @property
    def similarity_matrix(self) -> np.ndarray:
        if self._similarity_matrix is None:
            self.load_models()
        return self._similarity_matrix
    
    @property
    def vectorizer(self):
        if self._vectorizer is None:
            self.load_models()
        return self._vectorizer
    
    @property
    def movies_metadata(self) -> Dict[int, Dict]:
        if self._movies_metadata is None:
            self.load_models()
        return self._movies_metadata or {}
    
    @property
    def model_metadata(self) -> Dict:
        if self._model_metadata is None:
            self.load_models()
        return self._model_metadata or {}

# Global instance
model_loader = ModelLoader()

