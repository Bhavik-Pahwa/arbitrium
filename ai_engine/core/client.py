"""Thin OpenRouter wrapper. Uses the OpenAI SDK against OpenRouter's
OpenAI-compatible endpoint, pinned to the single allowed model.
"""

from openai import OpenAI

from core.config import REQUIRED_MODEL, get_settings


class ModelPolicyError(RuntimeError):
    pass


class OpenRouterClient:
    def __init__(self, model: str | None = None):
        settings = get_settings()
        requested = model or settings.model
        if requested != REQUIRED_MODEL:
            raise ModelPolicyError(
                f"Refusing to use model '{requested}': this module is locked to "
                f"'{REQUIRED_MODEL}' and does not substitute other models."
            )
        self.model = REQUIRED_MODEL
        self._client = OpenAI(api_key=settings.api_key, base_url=settings.base_url)

    def chat(self, messages: list[dict], tools: list[dict] | None = None, **kwargs):
        kwargs.setdefault("temperature", 0)
        return self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            **kwargs,
        )
