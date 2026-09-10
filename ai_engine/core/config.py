"""AI Engine configuration.

The model name is intentionally not a free-form setting: the task that
commissioned this module mandates `openrouter/free` and forbids silent
substitution. `REQUIRED_MODEL` is the single source of truth: if
OPENROUTER_MODEL is ever set to something else, startup fails loudly
instead of quietly calling a different model.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

REQUIRED_MODEL = "openrouter/free"


class ConfigError(RuntimeError):
    pass


class Settings:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("OPENROUTER_MODEL", REQUIRED_MODEL)

        if self.model != REQUIRED_MODEL:
            raise ConfigError(
                f"OPENROUTER_MODEL is set to '{self.model}' but this module is "
                f"restricted to '{REQUIRED_MODEL}'. Not substituting a different "
                f"model — fix the .env value."
            )
        if not self.api_key:
            raise ConfigError(
                "OPENROUTER_API_KEY is not set. Copy .env.example to .env and fill it in."
            )

    @property
    def data_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent / "data"


_settings: Settings | None = None


def get_settings() -> Settings:
    """Lazily constructed singleton so importing this module never fails
    just because .env isn't loaded yet (e.g. during test collection)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
