from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from typing import List

class BaseChatProvider(ABC):
    """Abstract base for all chat model providers."""

    @abstractmethod
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a response from the model given a prompt."""
        pass
