from typing import List

from langchain_community.vectorstores import Neo4jVector

from core.interfaces.base_embedding_provider import BaseEmbeddingProvider
from core.neo4j_executor import Neo4jExecutor


class EmbeddingService:
    """
    Handles embedding generation, vector index management, and hybrid retrieval.
    """

    def __init__(
        self,
        neo4j_executor: Neo4jExecutor,
        embedding_provider: BaseEmbeddingProvider,
        label: str = "Document",
        property_name: str = "embedding",
        dimension: int = 4096,
    ):
        self.neo4j_executor = neo4j_executor
        self.embedding_provider = embedding_provider
        self.label = label
        self.property_name = property_name
        self.dimension = dimension

        # Auto-generate index name
        self.index_name = f"{self.label.lower()}_{self.property_name.lower()}_index"

    def _ensure_index(self):
        """
        Check if the vector index exists and create it if missing.
        """
        if not self.neo4j_executor.index_exists(self.index_name):
            print(f"⚙️ Creating vector index '{self.index_name}' for label '{self.label}'...")
            self.neo4j_executor.create_vector_index(
                label=self.label,
                property_name=self.property_name,
                dimension=self.dimension,
            )
        else:
            print(f"✅ Vector index '{self.index_name}' already exists — skipping creation.")


    def search(self, query: str, top_k: int = 3) -> List[str]:
        """Perform hybrid similarity search on the Neo4j vector index."""
        print(f"🔍 Searching top {top_k} results for query: '{query}' on label '{self.label}'")
        results = self.vector_index.similarity_search(query, k=top_k)
        return [res.page_content for res in results]