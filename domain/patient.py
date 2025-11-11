from typing import Tuple, Dict, Any

from pydantic import BaseModel


class Patient():
    def __init__(self, name, age, gender, condition):
        self.name = name
        self.age = age
        self.gender = gender
        self.condition = condition

    def cypher_query(self)-> Tuple[str, Dict[str, Any]]:
        query = """
            MERGE (p:Patient {name:$name, age:$age, gender:$gender, condition:$condition})
        """
        parameters = {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "condition": self.condition
        }
        return query, parameters
