from core.neo4j_executor import Neo4jExecutor
from core.neo4j_vector_db import Neo4jVectorDB
from config.app_config import AppConfig
from neo4j import GraphDatabase

class DBFactory:
    """Centralized factory for all Neo4j-related database connectors."""

    @staticmethod
    def get_executor() -> Neo4jExecutor:
        driver = GraphDatabase.driver(
            AppConfig.NEO4J_URI,
            auth=(AppConfig.NEO4J_USERNAME, AppConfig.NEO4J_PASSWORD)
        )
        return Neo4jExecutor(driver, AppConfig.NEO4J_DATABASE)

    @staticmethod
    def get_neo4j_vector_db() -> Neo4jVectorDB:
        return Neo4jVectorDB()
