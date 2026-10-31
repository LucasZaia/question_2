from agent_app.config import Settings
from agent_app.agent import factory


def test_factory_builds_an_agent_with_configured_openai_model(monkeypatch) -> None:
    settings = Settings(openai_api_key="test-key", openai_model="test-model", openai_temperature=0.3)
    captured: dict[str, object] = {}

    class FakeChatOpenAI:
        def __init__(self, **kwargs):
            captured["model_kwargs"] = kwargs

    def fake_create_agent(**kwargs):
        captured["agent_kwargs"] = kwargs
        return "fake-agent"

    monkeypatch.setattr(factory, "ChatOpenAI", FakeChatOpenAI)
    monkeypatch.setattr(factory, "create_agent", fake_create_agent)

    result = factory.create_react_agent(settings)

    assert result == "fake-agent"
    assert captured["model_kwargs"] == {
        "api_key": "test-key",
        "model": "test-model",
        "temperature": 0.3,
    }
    assert captured["agent_kwargs"]["system_prompt"]
    assert captured["agent_kwargs"]["tools"]
    assert "Linux" in captured["agent_kwargs"]["system_prompt"]
    assert "programming" in captured["agent_kwargs"]["system_prompt"]

