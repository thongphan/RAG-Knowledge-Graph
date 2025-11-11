from langchain_openai import ChatOpenAI
from core.interfaces.base_chat_provider import BaseChatProvider


class OpenAIChatProvider(BaseChatProvider):
    """Chat provider implementation using OpenAI API."""

    def __init__(self, model: str = "gpt-4o-mini", api_key: str = None, temperature: float = 0.7):
        self.client = ChatOpenAI(model=model, api_key=api_key, temperature=temperature)

    def generate(self, prompt: str, context=None) -> str:
        """Generate response using OpenAI model."""
        result = self.client.invoke(prompt)
        return result.content
