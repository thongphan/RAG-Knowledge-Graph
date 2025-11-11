# database/init_schema.py
from core.neo4j_executor import Neo4jExecutor
from database.neo4j_schema_manager import Neo4jSchemaManager
from core.db_factory import DBFactory

def initialize_database():
    print("🔗 Connecting to Neo4j for schema setup...")
    executor = DBFactory.get_neo4j_vector_db()

    try:
        schema_manager = Neo4jSchemaManager(executor)
        schema_manager.create_all_indexes()
        print("✅ All indexes and constraints are up to date.")
    except Exception as e:
        print("❌ Failed to initialize schema:", e)
    finally:
        executor.close()
        print("🔒 Connection closed.")

if __name__ == "__main__":
    initialize_database()
