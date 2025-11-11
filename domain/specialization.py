from typing import Tuple, Dict, Any

from pydantic import BaseModel


class Specialization():
    def __init__(self, name):
        self.name = name

    def cypher_query(self)-> Tuple[str, Dict[str, Any]]:
        query = """
           MERGE (s:Specialization {name:$name})
            """
        parameters = {
            "name": self.name
        }
        return query, parameters
