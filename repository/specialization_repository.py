from core.neo4j_executor import Neo4jExecutor
from domain.specialization import Specialization
from repository.base_repository import BaseRepository
from typing import List, Dict

class SpecializationRepository(BaseRepository):
    def __init__(self, executor: Neo4jExecutor):
        self.executor = executor

    def save(self, specialization: Specialization):
        query, params = specialization.cypher_query()
        self.executor.execute_write(query, params)

    def save_batch(self, specializations: list):
        query = """
           UNWIND $batch AS row
             MERGE (s:Specialization {name:row.name})
           """
        batch_params = [{"name": p.name} for p in specializations]
        self.executor.execute_write(query, {"batch": batch_params})

    def get_all(self) -> list[dict]:
        query = "MATCH (s:Specialization) RETURN s.name AS name"
        try:
            return self.executor.execute_read(query)
        except Exception as e:
            print(e)