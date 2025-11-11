# Wait 60 seconds before connecting using these details, or login to https://console.neo4j.io to validate the Aura Instance is available
NEO4J_URI=neo4j+s://8768c71b.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=I9TNFCXFbmimRLuKgd-hQxsfNLzdWqnjopFrD2czxS0
NEO4J_DATABASE=neo4j
AURA_INSTANCEID=8768c71b
AURA_INSTANCENAME=Instance01

# Healthcare Knowledge Graph (Neo4j) + FastAPI

## Setup
1. Copy `.env.example` to `.env` and fill with your Neo4j credentials and CSV path.
2. `pip install -r requirements.txt`
3. Run the API:
 uvicorn main:app --reload

POST to `http://127.0.0.1:8000/ingest/` to start ingestion (runs in background).

## Notes
- CSV must follow headers:
Provider,Provider_Bio,Patient,Patient_Age,Patient_Gender,Patient_Condition,Specialization,Location
- Batch size default is 100; adjust in `IngestionService`.

##Set up ollama on a local
- ollama pull llama3
- it is running on a port = 11434

1. Flow Overview
[Extractor] → [Transformer] → [Loader] → [Neo4j]

Extractor: Pulls raw data from multiple sources (Wikipedia, YouTube, APIs, Kafka, database, etc.).

Transformer: Converts raw documents into graph-friendly documents (chunks, embeddings, entities) using LLMs.

Loader: Persists transformed documents into Neo4j or another graph/vector DB.

Orchestrator/Service: Coordinates the full flow and handles pipelines for RAG or other use cases.