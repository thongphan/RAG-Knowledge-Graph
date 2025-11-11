# database/base_schema_manager.py
from core.neo4j_executor import Neo4jExecutor
from typing import List

class BaseSchemaManager:
    def __init__(self, executor: Neo4jExecutor):
        self.executor = executor

    def run_queries(self, queries: List[str]):
        """Execute multiple schema setup queries safely."""
        for query in queries:
            try:
                self.executor.execute(query)
                print(f"✅ Executed schema query successfully:\n{query.strip()}\n")
            except Exception as e:
                print(f"❌ Failed to execute schema query:\n{query.strip()}\nError: {e}\n")
