# core/extractor.py
from abc import ABC, abstractmethod
from typing import List

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, query: str) -> List[dict]:
        """Extract raw data from a source"""
        pass
