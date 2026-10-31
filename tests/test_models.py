import pytest
from pydantic import ValidationError

from agent_app.models import ChatRequest, ChatResponse


def test_chat_request_accepts_a_thread_and_message() -> None:
    request = ChatRequest(thread_id="conversation-1", message="Olá")

    assert request.thread_id == "conversation-1"
    assert request.message == "Olá"


def test_chat_request_rejects_empty_values() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(thread_id="", message="")


def test_chat_response_contains_the_thread_and_answer() -> None:
    response = ChatResponse(thread_id="conversation-1", message="Olá!")

    assert response.model_dump() == {
        "thread_id": "conversation-1",
        "message": "Olá!",
    }

