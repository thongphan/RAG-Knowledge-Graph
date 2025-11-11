# core/neo4j_executor.py
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
