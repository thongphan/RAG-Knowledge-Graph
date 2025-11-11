from pydantic import BaseSettings


class Settings(BaseSettings):
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    NEO4J_DATABASE: str = "neo4j"
    CSV_FILE: str = "data/healthcare.csv"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()