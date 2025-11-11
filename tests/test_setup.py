import os
import pytest
from dotenv import load_dotenv
from neo4j import GraphDatabase
from ollama import Client

# Load .env automatically for tests
load_dotenv()

# ---------- Neo4j Connection Test ----------
@pytest.fixture
def neo4j_driver():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    assert uri, "NEO4J_URI not set in .env"
    assert user, "NEO4J_USERNAME not set in .env"
    assert password, "NEO4J_PASSWORD not set in .env"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    yield driver
    driver.close()

def test_neo4j_connection(neo4j_driver):
    # Simple test to check Neo4j connection
    with neo4j_driver.session() as session:
        result = session.run("RETURN 1 AS value")
        record = result.single()
        assert record["value"] == 1
    print("✅ Neo4j connection successful")


# ---------- Ollama LLM Test ----------
@pytest.fixture
def ollama_client():
    api_base = os.getenv("EMBEDDING_API_BASE")
    assert api_base, "EMBEDDING_API_BASE not set in .env"

    client = Client(host=api_base)
    return client

def test_ollama_client(ollama_client):
    # Check if client responds to basic query
    try:
        # List models as a simple test
        models = ollama_client.list()
        assert models, "No models available"
    except Exception as e:
        pytest.fail(f"Ollama client failed: {e}")
    print("✅ Ollama client setup successful")
