from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Neo4jVector
from config.app_config import AppConfig

class UnstructuredRetriever:
    """Retrieves unstructured data using Neo4j Vector Index"""

    def __init__(self):
        embeddings = OllamaEmbeddings(model=AppConfig.EMBEDDING_MODEL)
        self.vector_index = Neo4jVector.from_existing_graph(
            embeddings,
            search_type="hybrid",
            node_label="Document",
            text_node_properties=["text"],
            embedding_node_property="embedding"
        )

    def retrieve(self, query: str):
        return [doc.page_content for doc in self.vector_index.similarity_search(query)]
