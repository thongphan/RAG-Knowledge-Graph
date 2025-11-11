from repository.patient_repository import PatientRepository
from dto.patient_DTO import PatientDTO
from typing import List

class PatientService:
    def __init__(self, patient_repo: PatientRepository):
        self.patient_repo = patient_repo

    def get_all_patients(self) -> List[PatientDTO]:
        records = self.patient_repo.get_all()
        return [PatientDTO(name=r["name"]) for r in records]

# Dependency injector function moved inside service
def get_patient_service() -> PatientService:
    from core.neo4j_executor import Neo4jExecutor
    from config.app_config import AppConfig

    driver = AppConfig.driver()
    executor = Neo4jExecutor(driver, AppConfig.NEO4J_DATABASE)
    repo = PatientRepository(executor)
    return PatientService(repo)