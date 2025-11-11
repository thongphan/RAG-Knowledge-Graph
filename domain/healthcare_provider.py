from typing import Tuple, Dict, Any

from pydantic import BaseModel


class HealthcareProvider():
    def __init__(self, name: str,  bio: str | None = None):
        self.name = name
        self.bio = bio

    def cypher_query(self)-> Tuple[str, Dict[str, Any]]:
        query = """
          MERGE (hp:HealthcareProvider {name: $name, bio: $bio})
          """
        parameters = {
            "name": self.name,
            "bio": self.bio
        }
        return query, parameters
