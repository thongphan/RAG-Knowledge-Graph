import pytest
from neo4j import GraphDatabase
from core.neo4j_executor import Neo4jExecutor
from config.app_config import AppConfig

# -------------------------------
# Fixture: Neo4j Driver
# -------------------------------
@pytest.fixture(scope="module")
def neo4j_driver():
    """Provide a Neo4j driver for testing."""
    driver = GraphDatabase.driver(
        AppConfig.NEO4J_URI,
        auth=(AppConfig.NEO4J_USERNAME, AppConfig.NEO4J_PASSWORD),
        database=AppConfig.NEO4J_DATABASE
    )
    yield driver
    driver.close()


# -------------------------------
# Fixture: Neo4jExecutor
# -------------------------------
@pytest.fixture(scope="module")
def executor(neo4j_driver):
    """Provide a Neo4jExecutor using the driver."""
    return Neo4jExecutor(neo4j_driver, AppConfig.NEO4J_DATABASE)


# -------------------------------
# Optional: Repository factory fixture
# -------------------------------
@pytest.fixture
def provider_repository(executor):
    from repository.provider_repository import ProviderRepository
    return ProviderRepository(executor)

# -------------------------------
# Optional: Patient repository fixture
# -------------------------------
@pytest.fixture
def patient_repository(executor):
    """
    Provides an instance of PatientRepository for testing.
    Ensures dependency inversion: tests do not need to know executor internals.
    """
    from repository.patient_repository import PatientRepository
    return PatientRepository(executor)

