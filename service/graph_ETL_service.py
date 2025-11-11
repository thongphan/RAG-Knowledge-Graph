from core.interfaces.extractor import BaseExtractor
from core.interfaces.transformer import BaseTransformer

class GraphETLService:
    """Orchestrates extract -> transform -> load."""

    def __init__(self, extractor: BaseExtractor, transformer: BaseTransformer, loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self, query: str):
        raw_docs = self.extractor.extract(query)
        graph_docs = self.transformer.transform(raw_docs)
        self.loader.load_documents(graph_docs)
        return len(graph_docs)