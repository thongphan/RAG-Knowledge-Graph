from core.interfaces.base_chat_provider import BaseChatProvider

class ChatService:
    """High-level service orchestrating chat generation."""

    def __init__(self, provider: BaseChatProvider):
        self.provider = provider

    def chat(self, message: str, context=None) -> str:
        """Generate a model response from a user message."""
        if not message.strip():
            raise ValueError("Message cannot be empty.")
        return self.provider.generate(message, context)
