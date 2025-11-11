# database/schema_registry.py
from typing import Dict, List

# A registry that can be extended as the system grows
SCHEMA_REGISTRY: Dict[str, List[str]] = {
    "HealthcareProvider": [
        """
        CREATE CONSTRAINT IF NOT EXISTS
        FOR (hp:HealthcareProvider)
        REQUIRE hp.name IS UNIQUE
        """,
        """
        CREATE VECTOR INDEX health_provider_embedding IF NOT EXISTS
        FOR (hp:HealthcareProvider)
        ON (hp.comprehensiveEmbedding)
        OPTIONS {
            indexConfig: {
                'vectorDimension': 1536,
                'vector.similarity_function': 'cosine'
            }
        }
        """
    ],
    "Patient": [
        """
        CREATE CONSTRAINT IF NOT EXISTS
        FOR (p:Patient)
        REQUIRE p.patientId IS UNIQUE
        """,
    ],
    "Location": [
        """
        CREATE CONSTRAINT IF NOT EXISTS
        FOR (l:Location)
        REQUIRE l.name IS UNIQUE
        """,
    ],
}
