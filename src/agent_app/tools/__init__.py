from langchain_core.tools import BaseTool

from agent_app.tools.text_tools import count_words


def get_agent_tools() -> list[BaseTool]:
    return [count_words]

