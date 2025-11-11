from typing import Tuple, Dict, Any

from pydantic import BaseModel


class Location():
    def __init__(self, name):
        self.name = name

    def cypher_query(self)-> Tuple[str, Dict[str, Any]]:
        query = """
            MERGE (l:Location {name:$name})
        """
        parameters = {
            "name": self.name
        }
        return query, parameters
