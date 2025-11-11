# service/graph_transformer.py
from core.interfaces.transformer import BaseTransformer
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_ollama import ChatOllama
from typing import List
from langchain_text_splitters import TokenTextSplitter

class GraphTransformerService(BaseTransformer):
    """Converts raw documents to graph documents using an LLM."""

    def __init__(self, llm_model="llama3"):
        self.chat = ChatOllama(model=llm_model, temperature=0.7)
        self.transformer = LLMGraphTransformer(llm=self.chat)
        self.splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)

    def transform(self, raw_docs: List) -> List:
        """Split and transform raw docs into graph docs."""
        if not raw_docs:
            return []
        documents = self.splitter.split_documents(raw_docs)
        graph_docs = self.transformer.convert_to_graph_documents(documents)
        return graph_docs
