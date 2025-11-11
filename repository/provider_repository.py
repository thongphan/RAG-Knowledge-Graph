from typing import List, Dict
from functools import lru_cache
from core.neo4j_executor import Neo4jExecutor
from domain.healthcare_provider import HealthcareProvider
from repository.base_repository import BaseRepository


class ProviderRepository(BaseRepository):
    def __init__(self, executor: Neo4jExecutor):
        self.executor = executor

    def save(self, provider: HealthcareProvider) -> None:
        try:
            query, params = provider.cypher_query()
            self.executor.execute_write(query, params)
        except Exception as e:
            print(f"Error executing query: {e}")

    def save_batch(self, providers: List[HealthcareProvider]) -> None:
        """Save multiple providers in a batch using UNWIND"""
        if not providers:
            return
        try:
            query = """
            UNWIND $batch AS row
            MERGE (p:HealthcareProvider {name: row.name})
            SET p.bio = row.bio
            """
            batch_params = [{"name": p.name, "bio": p.bio} for p in providers]
            self.executor.execute_write(query, {"batch": batch_params})
        except Exception as e:
            print(e)
    def get_all(self) -> list[dict]:
        query = "MATCH (p:HealthcareProvider) RETURN p.name AS name, p.bio AS bio, p.comprehensiveEmbedding AS comprehensiveEmbedding"
        try:
            return self.executor.execute_read(query)
        except Exception as e:
            print(e)

    def update_provider_embedding(self, name: str, vector: List[float]):
        self.executor.execute_write(
            """
            MATCH (hp:HealthcareProvider {name: $name})
            SET hp.comprehensiveEmbedding = $vector
            """,
            {"name": name, "vector": vector},
        )

    def create_vector_index(self):
        self.executor.execute_write(
            """
            CREATE VECTOR INDEX health_providers_embeddings IF NOT EXISTS
            FOR (hp:HealthcareProvider) ON (hp.comprehensiveEmbedding)
            OPTIONS {
              indexConfig: {
                `vector.dimensions`: 4096,
                `vector.similarity_function`: 'cosine'
              }
            }
            """
        )

    def similarity_search(self, query_vector: List[float], top_k: int = 5):
        """
        Perform a cosine similarity search in Neo4j over 'comprehensiveEmbedding'.
        """
        # labels = [r["labels"] for r in self.executor.query("""
        #     MATCH (n)
        #     RETURN DISTINCT labels(n) AS labels
        # """)]
        # print(labels)

        cypher = f"""
           MATCH (p:HealthcareProvider)
           WHERE p.comprehensiveEmbedding IS NOT NULL
           WITH p, gds.similarity.cosine(p.comprehensiveEmbedding, $query_vector) AS score
           RETURN p.name AS name, p.bio AS bio, score
           ORDER BY score DESC
           LIMIT $top_k
           """
        params = {"query_vector": query_vector, "top_k": top_k}
        return self.executor.query(cypher, params)

    def add_providers(self, batch):
        self.executor.execute_batch(
            """
            UNWIND $batch AS row
            MERGE (p:HealthcareProvider {name: row.name})
            SET p.bio = row.bio
            """,
            batch
        )

    def get_all_providers(self):
        return self.executor.execute_read(
            "MATCH (p:HealthcareProvider) RETURN p.name AS name, p.bio AS bio"
        )

    def sample_providers(self, limit: int = 5) -> List[dict]:
        return self.executor.execute_read(
            """
            MATCH (hp:HealthcareProvider)
            WHERE hp.bio IS NOT NULL
            RETURN hp.name AS name, hp.bio AS bio, hp.comprehensiveEmbedding AS embedding
            LIMIT $limit
            """,
            {"limit": limit},
        )