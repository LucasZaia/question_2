import re
import unicodedata


OUT_OF_SCOPE_MESSAGE = (
    "Posso ajudar apenas com comandos Linux, programação e infraestrutura. "
    "Reformule sua pergunta dentro desses temas."
)

_ALLOWED_TERMS = (
    "linux",
    "ubuntu",
    "debian",
    "bash",
    "shell",
    "terminal",
    "comando",
    "sudo",
    "chmod",
    "grep",
    "awk",
    "sed",
    "ssh",
    "docker",
    "kubernetes",
    "terraform",
    "ansible",
    "cloud",
    "aws",
    "azure",
    "gcp",
    "deploy",
    "servidor",
    "infra",
    "rede",
    "dns",
    "nginx",
    "python",
    "program",
    "codigo",
    "algoritmo",
    "funcao",
    "classe",
    "variavel",
    "api",
    "http",
    "sql",
    "git",
    "github",
    "javascript",
    "typescript",
    "java",
    "rust",
    "fastapi",
    "django",
    "flask",
    "react",
    "node",
    "npm",
    "uv",
    "pip",
    "banco de dados",
    "sqlite",
    "postgres",
    "redis",
)

_GREETING_TERMS = {"oi", "ola", "olá", "ajuda", "help"}


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    return "".join(character for character in normalized if not unicodedata.combining(character))


def is_in_scope(message: str) -> bool:
    normalized = _normalize(message)
    if normalized.strip() in {_normalize(term) for term in _GREETING_TERMS}:
        return True
    return any(
        re.search(rf"\b{re.escape(_normalize(term))}\b", normalized)
        for term in _ALLOWED_TERMS
    )

