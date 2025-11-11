from core.neo4j_executor import Neo4jExecutor
from repository.base_repository import BaseRepository
from typing import List, Dict

class PatientRepository(BaseRepository):
    def __init__(self, executor: Neo4jExecutor):
        self.executor = executor

    def save(self, patient):
        query, params = patient.cypher_query()
        self.executor.execute(query, params)

    def save_batch(self, patients: list):
        query = """
        UNWIND $batch AS row
        MERGE (p:Patient {name: row.name})
        SET p.age = row.age, p.gender = row.gender, p.condition = row.condition
        """
        batch_params = [{"name": p.name, "age": p.age, "gender": p.gender, "condition": p.condition} for p in patients]
        self.executor.execute_write(query, {"batch": batch_params})

    def get_all(self) -> list[dict]:
        query = "MATCH (p:Patient) RETURN p.name AS name, p.age AS age, p.gender AS gender, p.condition AS condition"
        try:
            return self.executor.execute_read(query)
        except Exception as e:
            print(e)

    def add_patient(self, patient: dict):
        """
        Add a single patient node.
        """
        self.executor.execute_write(
            "CREATE (p:Patient {name:$name})",
            {"name": patient["name"]}
        )

    def get_all_patients(self):
        """
        Return all patient nodes.
        """
        return self.executor.execute_read(
            "MATCH (p:Patient) RETURN p.name AS name"
        )