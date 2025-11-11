from repository.patient_repository import PatientRepository
from repository.provider_repository import ProviderRepository
from repository.location_repository import LocationRepository
from repository.specialization_repository import SpecializationRepository
from repository.relationships_repository import RelationshipsRepository
from service.ingestion_service import IngestionService
from config.csv_config import CSVConfig
from core.db_factory import DBFactory

def main():
    #Call a dbfactory to get Neo4J database executor
    executor = DBFactory.get_executor()

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

if __name__ == "__main__":
    main()
    print("Graph populated successfully!")