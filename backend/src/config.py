"""Configuração: OPENAI_AI_API_KEY e OPENAI_AI_MODEL. Use .env dentro de backend/."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Nomes dos campos = nomes das env (uppercase): OPENAI_AI_API_KEY, OPENAI_AI_MODEL
    openai_ai_api_key: str = Field(default="", description="Chave API OpenAI")
    openai_ai_model: str = Field(default="gpt-4o-mini", description="Modelo de chat")

    @property
    def openai_api_key(self) -> str:
        return self.openai_ai_api_key

    @property
    def openai_model(self) -> str:
        return self.openai_ai_model


@lru_cache
def get_settings() -> Settings:
    return Settings()
