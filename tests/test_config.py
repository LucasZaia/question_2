import pytest
from pydantic import ValidationError

from agent_app.config import Settings


def test_settings_use_expected_defaults() -> None:
    settings = Settings(openai_api_key="test-key")

    assert settings.openai_model == "gpt-5-mini"
    assert settings.openai_temperature == 0


def test_settings_require_an_openai_api_key() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None)

