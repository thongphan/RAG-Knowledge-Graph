from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

load_dotenv()

class AppConfig:
    AURA_INSTANCENAME = os.getenv("AURA_INSTANCENAME")
    NEO4J_URI =os.environ["NEO4J_URI"]
    NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
    NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
    NEO4J_DATABASE = os.environ["NEO4J_DATABASE"]

    EMBEDDING_MODEL:str = os.environ["EMBEDDING_MODEL"]
    EMBEDDING_API_BASE: str = os.environ["EMBEDDING_API_BASE"]
    EMBEDDING_API_KEY: str = os.environ["EMBEDDING_API_KEY"]
    EMBEDDING_PROVIDER:str = os.environ["EMBEDDING_PROVIDER"]
    AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

    @classmethod
    def driver(cls):
        return GraphDatabase.driver(
            uri=cls.NEO4J_URI,
            auth=cls.AUTH
        )
