import pytest

from deepagents_cli import config


class DummyChatModel:
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs


@pytest.fixture(autouse=True)
def clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure provider-related environment variables are cleared between tests."""
    for key in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_BASE_URL"):
        monkeypatch.delenv(key, raising=False)


def test_create_model_applies_openai_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    import langchain_openai

    monkeypatch.setattr(langchain_openai, "ChatOpenAI", DummyChatModel)

    model = config.create_model(
        model_override="gpt-test",
        provider_override="openai",
        base_url_override="https://example.com/v1",
    )

    assert isinstance(model, DummyChatModel)
    assert model.kwargs["model"] == "gpt-test"
    assert model.kwargs["api_key"] == "test-key"
    assert model.kwargs["base_url"] == "https://example.com/v1"
    assert model.kwargs["temperature"] == 0.7


def test_create_model_uses_openai_compatible_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "router-key")

    import langchain_openai

    monkeypatch.setattr(langchain_openai, "ChatOpenAI", DummyChatModel)

    model = config.create_model(model_override="meta/llama3-70b-instruct")

    assert isinstance(model, DummyChatModel)
    assert model.kwargs["api_key"] == "router-key"
    assert model.kwargs["model"] == "meta/llama3-70b-instruct"


def test_create_model_requires_anthropic_key(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(SystemExit):
        config.create_model(provider_override="anthropic")


def test_create_model_with_anthropic_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-key")

    import langchain_anthropic

    monkeypatch.setattr(langchain_anthropic, "ChatAnthropic", DummyChatModel)

    model = config.create_model(provider_override="anthropic", model_override="claude-3-opus")

    assert isinstance(model, DummyChatModel)
    assert model.kwargs["model_name"] == "claude-3-opus"
    assert model.kwargs["max_tokens"] == 20000
