from agent_app.agent import create_react_agent
from agent_app.cli import run_cli
from agent_app.config import get_settings
from agent_app.service import ConversationService


def main() -> None:
    settings = get_settings()
    agent = create_react_agent(settings)
    service = ConversationService(agent)
    run_cli(service)


if __name__ == "__main__":
    main()

