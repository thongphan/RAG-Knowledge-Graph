# service/embedding_service.py
from abc import ABC, abstractmethod
from typing import List, Optional
from core.db_factory import DBFactory
from config.app_config import AppConfig
from ollama import Client as OllamaClient
import openai
from repository.base_repository import BaseRepository

# ---------------------- Provider Abstraction ----------------------
class BaseEmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding vector for a given text.

        Args:
            text (str): Input text to embed.

        Returns:
            List[float]: Embedding vector.
        """
        pass

# ---------------------- Ollama Local Provider ----------------------
class OllamaEmbeddingProvider(BaseEmbeddingProvider):
    """Generates embeddings using a local Ollama LLM instance."""

    def __init__(self, model: str, host: str = "http://localhost:11434"):
        self.client = OllamaClient(host=host)
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        response = self.client.embed(model=self.model, input=text)
        vector = response.get("embeddings")
        if vector and isinstance(vector[0], list):
            # Flatten nested list
            vector = [item for sublist in vector for item in sublist]
        return vector or []

# ---------------------- OpenAI Cloud Provider ----------------------
class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """Generates embeddings using OpenAI cloud API."""

    def __init__(self, api_key: str, model: str, api_base: Optional[str] = None):
        openai.api_key = api_key
        if api_base:
            openai.api_base = api_base
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        response = openai.Embedding.create(model=self.model, input=text)
        return response["data"][0]["embedding"]

# ---------------------- Embedding Service ----------------------
class EmbeddingService:
    """
    Service to generate embeddings using a provider and optionally
    store them in a repository.
    """

    def __init__(self, repo: BaseRepository, provider: BaseEmbeddingProvider):
        """
        Args:
            repo (BaseRepository): Repository for storing embeddings.
            provider (BaseEmbeddingProvider): Embedding provider (Ollama or OpenAI).
        """
        self.repo = repo
        self.provider = provider

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a text using the configured provider.

        Args:
            text (str): Input text to embed.

        Returns:
            List[float]: Generated embedding vector.
        """
        return self.provider.embed_text(text)

    def save_embedding(self, entity_id: str, text: str):
        """
        Generate embedding and save it to the repository.

        Args:
            entity_id (str): Unique ID for the entity/document.
            text (str): Text to embed.
        """
        vector = self.generate_embedding(text)
        self.repo.save_embedding(entity_id, vector)
