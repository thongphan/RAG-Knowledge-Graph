from typing import Tuple, Dict, Any

from pydantic import BaseModel


class Relationships():
    def __init__(self, provider: str, patient: str, specialization: str, location: str):
        self.provider = provider
        self.patient = patient
        self.specialization = specialization
        self.location = location

    """Return parameterized Cypher query to create relationships between nodes."""
    def cypher_query(self) -> Tuple[str, Dict[str, Any]]:

        query ="""
            MATCH (hp:HealthcareProvider {name: $provider}),
                  (p:Patient {name: $patient})
            MERGE (hp)-[:TREATS]->(p)
            WITH hp
            MATCH (s:Specialization {name: $specialization})
            MERGE (hp)-[:SPECIALIZES_IN]->(s)
            WITH hp
            MATCH (l:Location {name: $location})
            MERGE (hp)-[:LOCATED_AT]->(l)
        """
        parameters = {
            "provider": self.provider,
            "patient": self.patient,
            "specialization": self.specialization,
            "location": self.location
        }
        return query,parameters
