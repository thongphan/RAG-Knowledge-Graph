from abc import ABC, abstractmethod
from typing import List

class BaseEmbeddingProvider(ABC):
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass
from ollama import Client as OllamaClient

class OllamaEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, model: str, host: str = "http://localhost:11434"):
        self.client = OllamaClient(host=host)
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        response = self.client.embed(model=self.model, input=text)
        vector = response.get("embeddings")
        if vector and isinstance(vector[0], list):
            vector = [item for sublist in vector for item in sublist]
        return vector