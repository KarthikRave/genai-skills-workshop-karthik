"""
Custom exceptions for the Alaska Snow Department AI Agent.
"""

class AlaskaAgentException(Exception):
    """Base exception for Alaska Agent."""
    pass

class SafetyValidationError(AlaskaAgentException):
    """Raised when prompt fails safety validation."""
    pass

class RAGRetrievalError(AlaskaAgentException):
    """Raised when RAG context retrieval fails."""
    pass

class ResponseGenerationError(AlaskaAgentException):
    """Raised when response generation fails."""
    pass

class BigQueryConnectionError(AlaskaAgentException):
    """Raised when BigQuery connection fails."""
    pass