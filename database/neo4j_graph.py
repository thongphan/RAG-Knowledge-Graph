from core.db_factory import DBFactory

class GraphDB:
    """Responsible only for graph operations"""
    def __init__(self):
        self.neo4jdb = DBFactory.get_neo4j_vector_db().graph

    def ensure_fulltext_index(self):
        self.neo4jdb.query("""
            CREATE FULLTEXT INDEX entity IF NOT EXISTS
            FOR (e:__Entity__)
            ON EACH [e.id, e.description];
        """)

    def query(self, cypher: str, params: dict = None):
        return self.neo4jdb.query(cypher, params or {})
