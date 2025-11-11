from langchain_ollama import ChatOllama
from core.interfaces.base_chat_provider import BaseChatProvider

class OllamaProvider(BaseChatProvider):
    """Chat provider implementation using Ollama."""

    def __init__(self, model: str = "llama3", temperature: float = 0.7, base_url: str = "http://localhost:11434"):
        self.client = ChatOllama(model=model, temperature=temperature, base_url=base_url)

    def generate(self, prompt: str, context=None) -> str:
        """Generate response using Ollama model."""
        result = self.client.invoke(prompt)
        return result.content

