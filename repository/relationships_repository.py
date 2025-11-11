from core.neo4j_executor import Neo4jExecutor
from repository.base_repository import BaseRepository
from typing import List, Dict

class RelationshipsRepository(BaseRepository):
    def __init__(self, executor: Neo4jExecutor):
        self.executor = executor

    def save(self, relationship):
        query, params = relationship.cypher_query()
        self.executor.execute_write(query, params)

    def save_batch(self, relationships: list):
        query = """
           UNWIND $batch AS row
           MATCH (hp:HealthcareProvider {name: row.provider})
           MATCH (p:Patient {name: row.patient})
           MERGE (hp)-[:TREATS]->(p)
           WITH hp, row
           MATCH (s:Specialization {name: row.specialization})
           MERGE (hp)-[:SPECIALIZES_IN]->(s)
           WITH hp, row
           MATCH (l:Location {name: row.location})
           MERGE (hp)-[:LOCATED_AT]->(l)
           """
        batch_params = [
            {"provider": r.provider, "patient": r.patient, "specialization": r.specialization, "location": r.location}
            for r in relationships]
        self.executor.execute_write(query, {"batch": batch_params})

    def get_all(self) -> list[dict]:
        query = "MATCH (r:Relationships) RETURN r.name AS name"
        try:
            return self.executor.execute_read(query)
        except Exception as e:
            print(e)