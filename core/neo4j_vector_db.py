from langchain_neo4j import Neo4jGraph
from config.app_config import AppConfig

class Neo4jVectorDB:
    """LangChain-compatible graph connector for AI/RAG operations."""

    def __init__(self):
        self.graph = Neo4jGraph(
            url=AppConfig.NEO4J_URI,
            username=AppConfig.NEO4J_USERNAME,
            password=AppConfig.NEO4J_PASSWORD,
            database=AppConfig.NEO4J_DATABASE
        )

    def create_vector_index(self, label: str, property_name: str, dimension: int = 1536):
        """Creates vector index if not exists for the given label/property."""
        query = f"""
        CREATE VECTOR INDEX {label.lower()}_{property_name}_embedding IF NOT EXISTS
        FOR (n:{label}) ON (n.{property_name})
        OPTIONS {{
            indexConfig: {{
                `vector.dimensions`: {dimension},
                `vector.similarity_function`: 'cosine'
            }}
        }}
        """
        self.graph.query(query)
        print(f"✅ Vector index created for {label}.{property_name}")

    def query(self, cypher: str, params: dict = None):
        """General query execution for AI-driven searches."""
        return self.graph.query(cypher, params or {})
