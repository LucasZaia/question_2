from collections.abc import Callable
from uuid import uuid4

from agent_app.models import ChatRequest
from agent_app.service.conversation_service import AgentServiceError


EXIT_COMMANDS = {"sair", "exit", "quit"}
EXAMPLE_QUESTIONS = (
    "Como verificar o uso de memória no Linux?",
    "Como criar uma função em Python?",
    "O que é Docker?",
)


def run_cli(
    service,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    output_fn("Agente conversacional iniciado. Digite 'sair' para encerrar.")
    output_fn("Exemplos de perguntas:")
    for question in EXAMPLE_QUESTIONS:
        output_fn(f"- {question}")
    thread_id = str(uuid4())
    output_fn(f"Conversa criada: {thread_id}")

    while True:
        message = input_fn("Você: ").strip()
        if message.lower() in EXIT_COMMANDS:
            output_fn("Até logo!")
            return
        if not message:
            output_fn("A mensagem não pode estar vazia.")
            continue

        try:
            response = service.chat(ChatRequest(thread_id=thread_id, message=message))
            output_fn(f"Agente: {response.message}")
        except (ValueError, AgentServiceError) as exc:
            output_fn(f"Erro: {exc}")

