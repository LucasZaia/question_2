from uuid import UUID

from agent_app.cli import run_cli
from agent_app.models import ChatResponse


class FakeService:
    def __init__(self) -> None:
        self.requests = []

    def chat(self, request):
        self.requests.append(request)
        return ChatResponse(thread_id=request.thread_id, message=f"Resposta: {request.message}")


def test_cli_forwards_messages_and_stops_on_exit_command() -> None:
    service = FakeService()
    inputs = iter(["Olá agente", "sair"])
    outputs: list[str] = []

    run_cli(service, input_fn=lambda _: next(inputs), output_fn=outputs.append)

    UUID(service.requests[0].thread_id)
    assert service.requests[0].message == "Olá agente"
    assert any("Resposta: Olá agente" in output for output in outputs)
    assert "Até logo!" in outputs


def test_cli_rejects_empty_messages_without_calling_service() -> None:
    service = FakeService()
    inputs = iter(["", "sair"])
    outputs: list[str] = []

    run_cli(service, input_fn=lambda _: next(inputs), output_fn=outputs.append)

    assert service.requests == []
    assert any("mensagem não pode estar vazia" in output.lower() for output in outputs)


def test_cli_reuses_generated_thread_id_for_the_whole_session() -> None:
    service = FakeService()
    inputs = iter(["Primeira mensagem", "Segunda mensagem", "sair"])

    run_cli(service, input_fn=lambda _: next(inputs), output_fn=lambda _: None)

    assert len(service.requests) == 2
    assert service.requests[0].thread_id == service.requests[1].thread_id


def test_cli_displays_example_questions_on_startup() -> None:
    service = FakeService()
    inputs = iter(["sair"])
    outputs: list[str] = []

    run_cli(service, input_fn=lambda _: next(inputs), output_fn=outputs.append)

    startup_message = "\n".join(outputs)
    assert "Como verificar o uso de memória no Linux?" in startup_message
    assert "Como criar uma função em Python?" in startup_message
    assert "O que é Docker?" in startup_message

