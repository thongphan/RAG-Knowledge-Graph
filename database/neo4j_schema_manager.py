# database/neo4j_schema_manager.py
from database.base_schema_manager import BaseSchemaManager
from database.schema_registry import SCHEMA_REGISTRY

class Neo4jSchemaManager(BaseSchemaManager):
    def create_all_indexes(self):
        """Create all indexes and constraints from schema registry."""
        for label, queries in SCHEMA_REGISTRY.items():
            print(f"🔧 Applying schema for label: {label}")
            self.run_queries(queries)

    def drop_all_indexes(self):
        """Drop all constraints and indexes (use carefully)."""
        drop_query = "CALL apoc.schema.assert({}, {}, true)"
        self.executor.execute(drop_query)
        print("🧹 Dropped all schema constraints and indexes.")
