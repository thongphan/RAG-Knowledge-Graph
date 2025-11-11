from repository.structured_retriever import StructuredRetriever
from repository.unstructured_retriever import UnstructuredRetriever
class HybridRetriever:
    """Combines structured and unstructured retrievers"""

    def __init__(self, structured_retriever: StructuredRetriever, unstructured_retriever: UnstructuredRetriever):
        self.structured = structured_retriever
        self.unstructured = unstructured_retriever

    def retrieve(self, question: str):
        structured_data = self.structured.retrieve([question])
        unstructured_data = self.unstructured.retrieve(question)
        return f"Structured:\n{structured_data}\n\nUnstructured:\n{'#Document '.join(unstructured_data)}"
