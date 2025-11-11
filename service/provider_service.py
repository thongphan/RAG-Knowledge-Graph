from typing import List, Dict
from repository.provider_repository import ProviderRepository
from dto.provider_DTO import ProviderDTO
from ollama import Client
from config.app_config import AppConfig

class ProviderService():
    def __init__(self, provider_repo: ProviderRepository,base_uri:str=AppConfig.EMBEDDING_API_BASE):
        self.provider_repo = provider_repo
        self.client = Client(host=AppConfig.EMBEDDING_API_BASE)

    def get_all_providers(self) -> List[ProviderDTO]:
        records = self.provider_repo.get_all()
        return [ProviderDTO(name=r["name"], bio=r["bio"],comprehensiveEmbedding=r.get("comprehensiveEmbedding")) for r in records]

    def update_embeddings_for_all_providers_with_bio(self):
        """Fetch all providers, generate embeddings, and update in Neo4j."""
        providers = self.provider_repo.get_all()

        print(f"Found {len(providers)} providers to update embeddings...")

        for provider in providers:
            name = provider["name"]
            bio = provider["bio"]

            try:
                response = self.client.embed(model=AppConfig.EMBEDDING_MODEL, input=bio)
                vector = response.get("embeddings")
                # flatten if nested
                if vector and isinstance(vector[0], list):
                    vector = [item for sublist in vector for item in sublist]
                if vector:
                    self.provider_repo.update_provider_embedding(name, vector)
                    print(f"Updated embedding for: {name}")
                else:
                    print(f"⚠️ No embedding returned for {name}")

            except Exception as e:
                print(f"⚠️ Error generating embedding for {name}: {e}")

    def search_providers_by_query(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for providers most similar to the query embedding.
        Returns top_k provider DTOs with similarity score.
        """
        client = Client(host=AppConfig.EMBEDDING_API_BASE)

        query_text = "Experienced cardiologist with research background"
        response = client.embed(model=AppConfig.EMBEDDING_MODEL, input=query_text)

        query_vector = response.get("embeddings")
        # flatten if nested
        if query_vector and isinstance(query_vector[0], list):
            query_vector = [item for sublist in query_vector for item in sublist]

        print("Query vector length:", len(query_vector))
        results = self.provider_repo.similarity_search(query_vector, top_k=top_k)
        return results

    def create_vector_index(self):
        """Create vector index for provider embeddings."""
        self.provider_repo.create_vector_index()

    def sample_providers(self, limit: int = 5):
        """Return a sample of providers with embeddings."""
        return self.provider_repo.sample_providers(limit=limit)


# Dependency injector function moved inside service
def get_provider_service() -> ProviderService:
    from core.neo4j_executor import Neo4jExecutor
    from config.app_config import AppConfig

    driver = AppConfig.driver()
    executor = Neo4jExecutor(driver, AppConfig.NEO4J_DATABASE)
    repo = ProviderRepository(executor)
    return ProviderService(repo)