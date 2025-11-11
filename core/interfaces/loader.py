# core/loader.py
from abc import ABC, abstractmethod
from typing import List

class BaseLoader(ABC):
    @abstractmethod
    def load(self, docs: List[dict]):
        """Load transformed data into the target system"""
        pass
