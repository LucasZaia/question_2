import pytest

from agent_app.models import ChatRequest
from agent_app.service.conversation_service import AgentServiceError, ConversationService


class FakeAgent:
    def __init__(self) -> None:
        self.calls: list[tuple[dict, dict]] = []

    def invoke(self, payload: dict, config: dict) -> dict:
        self.calls.append((payload, config))
        thread_id = config["configurable"]["thread_id"]
        message = payload["messages"][0]["content"]
        return {"messages": [{"content": f"Resposta para {thread_id}: {message}"}]}


def test_service_returns_the_agent_answer() -> None:
    agent = FakeAgent()
    service = ConversationService(agent)

    response = service.chat(ChatRequest(thread_id="conversation-1", message="Olá"))

    assert response.thread_id == "conversation-1"
    assert response.message == "Resposta para conversation-1: Olá"
    assert agent.calls[0][1] == {"configurable": {"thread_id": "conversation-1"}}


def test_service_keeps_threads_isolated_in_agent_configuration() -> None:
    agent = FakeAgent()
    service = ConversationService(agent)

    first = service.chat(ChatRequest(thread_id="first", message="Como uso Linux?"))
    second = service.chat(ChatRequest(thread_id="second", message="Como uso Python?"))

    assert first.message.startswith("Resposta para first")
    assert second.message.startswith("Resposta para second")
    assert agent.calls[0][1] != agent.calls[1][1]


def test_service_rejects_blank_messages() -> None:
    service = ConversationService(FakeAgent())

    with pytest.raises(ValueError, match="Message cannot be empty"):
        service.chat(ChatRequest(thread_id="conversation-1", message="   "))


def test_service_wraps_agent_errors() -> None:
    class BrokenAgent:
        def invoke(self, payload: dict, config: dict) -> dict:
            raise RuntimeError("tool failed")

    service = ConversationService(BrokenAgent())

    with pytest.raises(AgentServiceError, match="Unable to process the conversation"):
        service.chat(ChatRequest(thread_id="conversation-1", message="Olá"))


def test_service_blocks_unrelated_questions_without_calling_the_agent() -> None:
    agent = FakeAgent()
    service = ConversationService(agent)

    response = service.chat(
        ChatRequest(thread_id="conversation-1", message="Qual é a previsão do tempo?")
    )

    assert "Linux, programação e infraestrutura" in response.message
    assert agent.calls == []

