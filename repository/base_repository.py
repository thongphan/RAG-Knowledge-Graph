from abc import ABC, abstractmethod
from typing import List, Any

class BaseRepository(ABC):
    @abstractmethod
    def save(self, entity: Any) -> None:
        """Save a single entity"""
        pass

    @abstractmethod
    def save_batch(self, entities: List[Any]) -> None:
        """Save a batch of entities"""
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        """Retrieve all entities"""
        pass
