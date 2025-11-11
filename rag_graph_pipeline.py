
from repository.structured_retriever import StructuredRetriever
from repository.unstructured_retriever import UnstructuredRetriever
from adapters.wikipedia_extractor import WikipediaExtractor
from service.graph_transformer_service import GraphTransformerService
from repository.neo4j_repository import Neo4jRepository
from service.rag_graph_chain_service import RAGPipelineService
from service.graph_ETL_service import GraphETLService
from database.neo4j_graph import GraphDB
from llm.providers.ollama_chat_provider import OllamaProvider
from service.chat_service import ChatService
from service.embedding_service import EmbeddingService


if __name__ == "__main__":
    # Initialize Ollama-based provider
    ollama_provider = OllamaProvider(model="llama3")

    # Inject provider into the chat service
    chat_service = ChatService(provider=ollama_provider)

    #Initialize Neo4J DB
    graph = GraphDB()

    # # 1. Extract
    # extractor = WikipediaExtractor()
    # raw_docs = extractor.extract("Pham Minh Chinh")
    #
    # # 2. Transform
    # transformer = GraphTransformerService()
    # graph_docs = transformer.transform(raw_docs)
    #
    # # 3. Load
    # loader = Neo4jRepository()
    # loader.load_documents(graph_docs)
    #
    # # 4. Wrap in orchestrator to load data from wikipedia
    # etl_service = GraphETLService(extractor, transformer, loader)
    # etl_service.run("Pham Minh Chinh")


    structured = StructuredRetriever(graph)
    unstructured = UnstructuredRetriever()

    pipeline = RAGPipelineService(structured, unstructured, ollama_provider.client)
    # Follow-up question with history
    response = pipeline.run(
        "cardiologist with over 20?",
        chat_history=[("specializes in neurology", "specializes in neurology")]
    )
    print(response)

    # Simple question without history
    #response2 = pipeline.run("Who is Pham Minh Chinh?")
    #print(response2)
