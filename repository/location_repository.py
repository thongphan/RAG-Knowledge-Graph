from core.neo4j_executor import Neo4jExecutor
from repository.base_repository import BaseRepository
from typing import List, Dict

class LocationRepository(BaseRepository):
    def __init__(self, executor: Neo4jExecutor):
        self.executor = executor

    def save(self, location):
        query, params = location.cypher_query()
        self.executor.execute_write(query, params)

    def save_batch(self, locations: list):
        query = """
           UNWIND $batch AS row
            MERGE (l:Location {name:row.name})
           """
        batch_params = [{"name": p.name} for p in locations]
        self.executor.execute_write(query, {"batch": batch_params})

    def get_all(self) -> list[dict]:
        query = "MATCH (l:Location) RETURN l.name AS name"
        try:
            return self.executor.execute_read(query)
        except Exception as e:
            print(e)