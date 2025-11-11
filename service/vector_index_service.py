from typing import List, Dict
from repository.vector_index_repository import VectorIndexRepository

class VectorIndexService:
    """Orchestrates creation of indexes and batch embeddings for entities."""

    def __init__(self, repository: VectorIndexRepository):
        self.repo = repository

    def create_index(self):
        """Initialize index for the entity."""
        return self.repo.create_index()

    def save_embedding(self, doc_id: str, text: str):
        self.repo.save_embedding(doc_id, text)

    def batch_save_embeddings(self, docs: List[Dict[str, str]]):
        """
        docs: list of dict with keys ['doc_id', 'text']
        """
        for doc in docs:
            self.save_embedding(doc['doc_id'], doc['text'])
