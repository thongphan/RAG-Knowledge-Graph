# core/neo4j_executor.py
from typing import List, Any, Dict

from neo4j import GraphDatabase

class Neo4jExecutor:
    """Handles direct Neo4j Cypher queries for repositories."""
    def __init__(self, driver: GraphDatabase.driver, database: str):
        self.driver = driver
        self.database = database

    def execute_write(self, query: str, parameters: dict = None):
        try:
            with self.driver.session(database=self.database) as session:
                session.run(query, parameters)
        except Exception as e:
            print(f"[Neo4jExecutor] Error executing write query: {e}")

    def execute_batch(self, query: str, batch_params: list):
        """Execute batch of Cypher queries with parameters list."""
        try:
            with self.driver.session(database=self.database) as session:
                def _batch(tx):
                    for params in batch_params:
                        tx.run(query, params)
                session.execute_write(_batch)
        except Exception as e:
            print(f"[Neo4jExecutor] Error executing batch query: {e}")

    def execute_read(self, query: str, parameters: dict = None) -> list[dict]:
        try:
            with self.driver.session(database=self.database) as session:
                def _read(tx):
                    result = tx.run(query, parameters)
                    return [dict(record) for record in result]
                return session.execute_read(_read)
        except Exception as e:
            print(f"[Neo4jExecutor] Error executing read query: {e}")
            return []

    def create_vector_index(
        self,
        label: str,
        property_name: str,
        dimension: int = 4096,
    ):
        """
        Create a vector index for the given label/property if it doesn't exist.
        """
        index_name = f"{label.lower()}_{property_name.lower()}_index"

        if self.index_exists(index_name):
            print(f"✅ Vector index '{index_name}' already exists — skipping creation.")
            return

        cypher = f"""
        CREATE VECTOR INDEX {index_name}
        FOR (n:{label})
        ON (n.{property_name})
        OPTIONS {{
            indexConfig: {{
                `vector.dimensions`: {dimension},
                `vector.similarity_function`: 'cosine'
            }}
        }}
        """
        self.graph.query(cypher)
        print(f"⚙️ Vector index '{index_name}' created for {label}.{property_name}")

    def index_exists(self, index_name: str) -> bool:
        """
        Check if a vector index exists in Neo4j
        """
        query = "SHOW INDEXES YIELD name RETURN name"
        results = self.graph.query(query)
        # Neo4jGraph.query() returns list of dicts
        indexes = [r["name"] for r in results]
        return index_name in indexes

    # Generic query executor
    def query(self, cypher: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return results as a list of dicts
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(cypher, parameters or {})
            return [record.data() for record in result]