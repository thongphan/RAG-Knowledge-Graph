# service/neo4j_property_service.py
from core.neo4j_executor import Neo4jExecutor
from typing import Optional

class Neo4jPropertyService:
    """
    General service to manage properties on nodes in Neo4j.
    Supports removing or updating properties for scalable and batch operations.
    """

    def __init__(self, executor: Neo4jExecutor):
        self.executor = executor

    def remove_property(
        self,
        label: str,
        property_key: str,
        batch_size: int = 100
    ) -> int:
        """
        Remove a property from all nodes with a given label in batches.
        Returns the total number of nodes updated.
        """
        total_removed = 0
        offset = 0

        while True:
            # Fetch a batch of nodes with the property
            fetch_query = f"""
                MATCH (n:{label})
                WHERE n.{property_key} IS NOT NULL
                RETURN n.name AS name
                SKIP $offset LIMIT $batch_size
            """
            batch_nodes = self.executor.execute_read(fetch_query, {"offset": offset, "batch_size": batch_size})

            if not batch_nodes:
                break

            # Remove property in batch
            names = [node["name"] for node in batch_nodes]
            remove_query = f"""
                UNWIND $names AS nname
                MATCH (n:{label} {{name: nname}})
                REMOVE n.{property_key}
            """
            self.executor.execute_write(remove_query, {"names": names})

            total_removed += len(batch_nodes)
            offset += batch_size

        return total_removed
