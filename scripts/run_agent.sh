#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [[ ! -f ".env" ]]; then
  echo "Arquivo .env não encontrado em: $PROJECT_DIR" >&2
  echo "Crie o arquivo a partir de .env.example e informe OPENAI_API_KEY." >&2
  exit 1
fi

exec uv run python -m agent_app.main
