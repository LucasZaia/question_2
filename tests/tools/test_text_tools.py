from agent_app.tools.text_tools import count_words


def test_count_words_returns_the_number_of_words() -> None:
    assert count_words.invoke({"text": "LangChain cria agentes conversacionais"}) == "4"


def test_get_agent_tools_exposes_count_words() -> None:
    from agent_app.tools import get_agent_tools

    tools = get_agent_tools()

    assert [tool.name for tool in tools] == ["count_words"]

