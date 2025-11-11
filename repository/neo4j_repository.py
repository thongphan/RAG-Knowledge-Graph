from typing import List, Optional, Dict
from core.db_factory import DBFactory
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Neo4jRepository:
    """
    Handles all Neo4j CRUD operations, relationships, and document ingestion.
    """

    def __init__(self):
        self.driver = DBFactory.get_executor().driver
        self.kg = DBFactory.get_neo4j_vector_db()
        logger.info("Neo4jRepository initialized.")

    # ---------------------------
    # Node Operations
    # ---------------------------
    def create_entities(self, entities: List[Dict]):
        """
        Create nodes from a list of entities.
        Each entity dict should include 'label', 'name', and optional 'properties'.
        """
        if not entities:
            logger.warning("No entities provided to create.")
            return

        def tx_func(tx):
            for e in entities:
                label = e['label']
                name = e['name']
                query = f"MERGE (n:{label} {{name: $name}})"
                tx.run(query, name=name)

                # Set additional properties if any
                if 'properties' in e and e['properties']:
                    props = ', '.join([f"n.{k} = ${k}" for k in e['properties']])
                    parameters = {"name": name, **e['properties']}
                    tx.run(f"MATCH (n:{label} {{name: $name}}) SET {props}", parameters)

        with self.driver.session() as session:
            session.execute_write(tx_func)
        logger.info(f"✅ Created/merged {len(entities)} entities.")

    # ---------------------------
    # Relationship Operations
    # ---------------------------
    def create_relationships(self, relationships: List[Dict]):
        """
        Create relationships from a list of dictionaries.
        Each dict should have 'from_label', 'from', 'to_label', 'to', 'type'.
        """
        if not relationships:
            logger.warning("No relationships provided to create.")
            return

        def tx_func(tx):
            for r in relationships:
                query = (
                    f"MATCH (a:{r['from_label']} {{name:$from_name}}), "
                    f"(b:{r['to_label']} {{name:$to_name}}) "
                    f"MERGE (a)-[:{r['type']}]->(b)"
                )
                tx.run(query, from_name=r['from'], to_name=r['to'])

        with self.driver.session() as session:
            session.execute_write(tx_func)
        logger.info(f"✅ Created {len(relationships)} relationships.")

    # ---------------------------
    # Generic Query
    # ---------------------------
    def query(self, cypher: str, parameters: Optional[Dict] = None):
        """
        Execute a Cypher query and return records.
        """
        with self.driver.session() as session:
            result = session.run(cypher, parameters or {})
            records = [record for record in result]
        return records

    # ---------------------------
    # Document Loading for RAG / Vector DB
    # ---------------------------
    def load_documents(self, docs: List[dict]):
        """
        Load a list of documents into Neo4j graph vector database.
        """
        if not docs:
            logger.warning("No documents provided for loading.")
            return

        self.kg.graph.add_graph_documents(
            docs,
            include_source=True,
            baseEntityLabel=True
        )
        logger.info(f"✅ Loaded {len(docs)} documents into Neo4j vector DB.")