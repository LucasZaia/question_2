## Requisitos

- Python 3.11+
- `uv`
- Uma chave de API da OpenAI

## Configuração

Sincronize as dependências:

```bash
uv sync --extra dev
```

Copie o arquivo de ambiente e preencha sua chave:

```bash
cp .env.example .env
```

Variáveis disponíveis:

```env
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-5-mini
OPENAI_TEMPERATURE=0
```

## Scripts

O projeto possui o script `scripts/run_agent.sh`, que automatiza a execução do agente a partir da raiz do projeto. Antes de iniciar, ele verifica se o arquivo `.env` existe.

Execute:

```bash
./scripts/run_agent.sh
```

Se o `.env` não existir, crie-o com base no exemplo:

```bash
cp .env.example .env
```

Para executar sem o script:

```bash
uv run python -m agent_app.main
```

O script não recebe parâmetros. A entrada é feita de forma interativa no terminal; use `sair`, `exit` ou `quit` para encerrar.

Ao iniciar, o programa gera automaticamente um identificador para a conversa e exibe algumas sugestões:

```text
Agente conversacional iniciado. Digite 'sair' para encerrar.
Exemplos de perguntas:
- Como verificar o uso de memória no Linux?
- Como criar uma função em Python?
- O que é Docker?
Conversa criada: 4c2b6a46-6cc2-4ac8-9d90-1df3b9b5a14b
```

## Escopo e guardrails

O agente é um auxiliar tecnológico especializado em:

- Comandos e administração Linux;
- Programação e desenvolvimento de software;
- Infraestrutura, servidores, redes, cloud e deploy.

Existe uma proteção em duas camadas. O `system prompt` instrui o modelo a recusar assuntos fora desse escopo, e o `ConversationService` bloqueia perguntas claramente não relacionadas antes de chamar o modelo. Por exemplo, perguntas sobre previsão do tempo, receitas ou outros assuntos gerais recebem uma mensagem de orientação e não consomem uma chamada ao agente.

Essa proteção não deve ser considerada autenticação ou filtro de segurança completo para produção; ela é uma barreira de escopo da primeira versão.

## Memória por conversa

O contexto é mantido em memória pelo LangGraph e separado pelo `thread_id`. Mensagens usando o mesmo identificador pertencem à mesma conversa; identificadores diferentes não compartilham histórico. A memória atual existe apenas enquanto o processo está em execução.

## Testes

Os testes não fazem chamadas reais à OpenAI. A factory e o service usam mocks/fakes para validar configuração, ferramentas, isolamento de threads, erros e CLI.

```bash
uv run python -m pytest -q
```

