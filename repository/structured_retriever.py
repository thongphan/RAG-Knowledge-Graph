from typing import List
from database.neo4j_graph import GraphDB
from langchain_neo4j.vectorstores.neo4j_vector import remove_lucene_chars

class StructuredRetriever:
    """Retrieves structured entity data from Neo4j"""

    def __init__(self, graph_db: GraphDB):
        self.graph_db = graph_db

    def _generate_full_text_query(self, text: str) -> str:
        words = [el for el in remove_lucene_chars(text).split() if el]
        return " AND ".join([f"{w}~2" for w in words])

    def retrieve(self, entities: List[str]) -> str:
        result = []
        for entity in entities:
            cypher = """
            CALL db.index.fulltext.queryNodes('entity', $query, {limit:2})
            YIELD node, score
            WITH node, score
            OPTIONAL MATCH (node)-[r]-(neighbor)
            RETURN node.id + ' - ' + type(r) + ' -> ' + neighbor.id AS output
            LIMIT 50
            """
            rows = self.graph_db.query(cypher, {"query": self._generate_full_text_query(entity)})
            result.extend([r["output"] for r in rows])
        return "\n".join(result)
