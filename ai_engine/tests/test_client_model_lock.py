import pytest

from core.client import ModelPolicyError, OpenRouterClient
from core.config import ConfigError, Settings


def test_client_rejects_non_required_model():
    with pytest.raises(ModelPolicyError):
        OpenRouterClient(model="gpt-4o")


def test_client_accepts_required_model():
    client = OpenRouterClient(model="openrouter/free")
    assert client.model == "openrouter/free"


def test_settings_rejects_wrong_model_env(monkeypatch):
    monkeypatch.setenv("OPENROUTER_MODEL", "some-other-model")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    with pytest.raises(ConfigError):
        Settings()


def test_settings_rejects_missing_api_key(monkeypatch):
    monkeypatch.setenv("OPENROUTER_MODEL", "openrouter/free")
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    with pytest.raises(ConfigError):
        Settings()


def test_settings_accepts_valid_config(monkeypatch):
    monkeypatch.setenv("OPENROUTER_MODEL", "openrouter/free")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    settings = Settings()
    assert settings.model == "openrouter/free"
