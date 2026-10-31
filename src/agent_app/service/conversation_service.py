from typing import Any

from agent_app.models import ChatRequest, ChatResponse
from agent_app.service.scope_guard import OUT_OF_SCOPE_MESSAGE, is_in_scope


class AgentServiceError(RuntimeError):
    """Raised when the conversational agent cannot process a message."""


class ConversationService:
    def __init__(self, agent: Any) -> None:
        self.agent = agent

    def chat(self, request: ChatRequest) -> ChatResponse:
        thread_id = request.thread_id.strip()
        message = request.message.strip()
        if not message:
            raise ValueError("Message cannot be empty")
        if not thread_id:
            raise ValueError("Thread ID cannot be empty")
        if not is_in_scope(message):
            return ChatResponse(thread_id=thread_id, message=OUT_OF_SCOPE_MESSAGE)

        try:
            result = self.agent.invoke(
                {"messages": [{"role": "user", "content": message}]},
                config={"configurable": {"thread_id": thread_id}},
            )
            answer = self._extract_answer(result)
        except (ValueError, AgentServiceError):
            raise
        except Exception as exc:
            raise AgentServiceError("Unable to process the conversation") from exc

        return ChatResponse(thread_id=thread_id, message=answer)

    @staticmethod
    def _extract_answer(result: dict[str, Any]) -> str:
        messages = result.get("messages", [])
        if not messages:
            raise AgentServiceError("Agent returned no messages")

        last_message = messages[-1]
        if isinstance(last_message, dict):
            content = last_message.get("content", "")
        else:
            content = getattr(last_message, "content", "")
        if isinstance(content, list):
            content = "".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in content
            )
        if not isinstance(content, str) or not content.strip():
            raise AgentServiceError("Agent returned an empty response")
        return content.strip()

