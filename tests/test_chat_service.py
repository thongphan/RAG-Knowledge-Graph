import pytest
from unittest.mock import Mock
from service.chat_service import ChatService
from core.interfaces.base_chat_provider import BaseChatProvider


class MockChatProvider(BaseChatProvider):
    """Mock implementation of BaseChatProvider for testing."""

    def generate(self, prompt: str, context=None) -> str:
        return f"Mock response to: {prompt}"


@pytest.fixture
def mock_provider():
    """Fixture to provide a mock chat provider."""
    return MockChatProvider()


@pytest.fixture
def chat_service(mock_provider):
    """Fixture to provide a ChatService instance."""
    return ChatService(provider=mock_provider)


def test_chat_service_generates_response(chat_service):
    """Test that ChatService generates a valid response."""
    message = "Explain what is retrieval augmented generation (RAG)."
    response = chat_service.chat(message)
    assert isinstance(response, str)
    assert "Mock response" in response


def test_chat_service_raises_error_on_empty_message(chat_service):
    """Test that ChatService raises an error for empty input."""
    with pytest.raises(ValueError, match="Message cannot be empty."):
        chat_service.chat("  ")

@pytest.mark.integration
def test_chat_service_with_real_ollama():
    from llm.providers.ollama_chat_provider import OllamaProvider

    provider = OllamaProvider(model="llama3")
    service = ChatService(provider=provider)
    response = service.chat("What is RAG?")
    assert isinstance(response, str)
    print(response)
