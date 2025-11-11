# adapters/wikipedia_loader.py
from typing import List
from core.interfaces.extractor import BaseExtractor
from langchain_community.document_loaders import WikipediaLoader

class WikipediaExtractor(BaseExtractor):
    def extract(self, query: str):
        return WikipediaLoader(query=query).load()

    def extract_with_limit(self, query: str, limit: int = 3) -> List:
        raw_docs = WikipediaLoader(query=query).load()
        if not raw_docs:
            return []
        return raw_docs[:limit]  # limit number of documents
