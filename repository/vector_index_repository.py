from core.db_factory import DBFactory
from langchain_community.vectorstores import Neo4jVector
from typing import List
from llm.embedding_providers import BaseEmbeddingProvider

class VectorIndexRepository:
    """Handles creation of vector index in Neo4j for any entity type."""

    def __init__(
        self,
        provider: BaseEmbeddingProvider,
        node_label: str = "Document",
        text_properties: List[str] = ["text"],
        embedding_property: str = "embedding",
        search_type: str = "hybrid"
    ):
        self.provider = provider
        self.node_label = node_label
        self.text_properties = text_properties
        self.embedding_property = embedding_property
        self.search_type = search_type
        self.kg = DBFactory.get_neo4j_vector_db()

    def create_index(self):
        """Create a Neo4jVector index for the entity type."""
        return Neo4jVector.from_existing_graph(
            embeddings=self.provider,
            search_type=self.search_type,
            node_label=self.node_label,
            text_node_properties=self.text_properties,
            embedding_node_property=self.embedding_property,
        )

    def save_embedding(self, doc_id: str, text: str):
        """Generate embedding and save in Neo4j."""
        embedding = self.provider.embed_text(text)
        query = f"""
        MERGE (n:{self.node_label} {{id:$doc_id}})
        SET n.{self.embedding_property} = $embedding
        """
        with self.kg.graph.driver.session() as session:
            session.execute_write(lambda tx: tx.run(query, doc_id=doc_id, embedding=embedding))
