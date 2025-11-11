from typing import List

from config.app_config import AppConfig
from database.neo4j_graph import GraphDB
from dto.provider_DTO import ProviderDTO
from llm.providers.ollama_chat_provider import OllamaProvider
from repository.patient_repository import PatientRepository
from repository.provider_repository import ProviderRepository
from repository.location_repository import LocationRepository
from repository.specialization_repository import SpecializationRepository
from repository.relationships_repository import RelationshipsRepository
from service.chat_service import ChatService
from service.embedding_service import EmbeddingService
from service.ingestion_service import IngestionService
from config.csv_config import CSVConfig
from core.db_factory import DBFactory
from service.provider_service import ProviderService, get_provider_service


def main():
    #Call a dbfactory to get Neo4J database executor
    executor = DBFactory.get_executor()

    # Initialize Ollama-based provider
    ollama_provider = OllamaProvider(model="llama3")

    # Initialize Neo4J DB
    graph = GraphDB()

    patient_repo = PatientRepository(executor)
    provider_repo = ProviderRepository(executor)
    location_repo = LocationRepository(executor)
    specialization_repo = SpecializationRepository(executor)
    relationships_repo = RelationshipsRepository(executor)


    ingestion = IngestionService(
        csv_path=CSVConfig.FILE_PATH,
        headers=CSVConfig.HEADERS,
        provider_repo=provider_repo,
        patient_repo=patient_repo,
        specialization_repo=specialization_repo,
        location_repo=location_repo,
        relationships_repo=relationships_repo

    )
    ingestion.ingest()

    # ✅ Fetch all provider data from service
    service = get_provider_service()
    service.update_embeddings_for_all_providers_with_bio()
    #use get provider service from provider_service.py
    query = "Experienced cardiologist with research background"
    results = service.search_providers_by_query(query, top_k=5)

    for r in results:
        print(f"{r['name']} (score: {r['score']:.4f}) - {r['bio']}")

if __name__ == "__main__":
    main()
    print("Graph populated successfully!")