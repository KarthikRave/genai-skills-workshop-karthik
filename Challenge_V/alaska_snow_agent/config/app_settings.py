"""
Enhanced configuration management for the Alaska Snow Department AI Agent.
"""
import os
from typing import Optional

class AppConfig:
    """Centralized configuration management."""
    
    # Google Cloud Settings
    PROJECT_ID: str = "qwiklabs-gcp-02-79b6e8a77529"
    LOCATION: str = "us-central1"
    
    # BigQuery Settings
    DATASET_NAME: str = "AlaskaDataBase"
    RAW_TABLE_NAME: str = "question_answer"
    EMBEDDED_TABLE_NAME: str = "question_answer_embedded"
    EMBEDDING_MODEL_NAME: str = "Embeddings"
    
    # Derived IDs
    @property
    def embedded_table_id(self) -> str:
        return f"{self.PROJECT_ID}.{self.DATASET_NAME}.{self.EMBEDDED_TABLE_NAME}"
    
    @property
    def embedding_model_id(self) -> str:
        return f"{self.PROJECT_ID}.{self.DATASET_NAME}.{self.EMBEDDING_MODEL_NAME}"
    
    # Model Settings
    GENERATIVE_MODEL: str = "gemini-2.0-flash-001"
    EMBEDDING_MODEL: str = "text-embedding-005"
    
    # RAG Settings
    TOP_K_RESULTS: int = 3
    SIMILARITY_THRESHOLD: float = 0.7
    
    # Safety Settings
    ENABLE_SAFETY_FILTERING: bool = True
    SAFETY_THRESHOLD: str = "BLOCK_LOW_AND_ABOVE"
    
    # Authentication
    CREDENTIALS_PATH: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "alaska_admin_key.json")

# Global config instance
config = AppConfig()