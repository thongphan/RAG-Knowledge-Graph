# core/transformer.py
from abc import ABC, abstractmethod
from typing import List

class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, raw_docs: List[dict]) -> List[dict]:
        """Transform raw data into graph or vector-ready format"""
        pass
