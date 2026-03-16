"""Configuração: OPENAI_API_KEY e OPENAI_MODEL. Use .env dentro de backend/."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = Field(default="", description="Chave API OpenAI")
    openai_model: str = Field(default="gpt-4o-mini", description="Modelo de chat")


@lru_cache
def get_settings() -> Settings:
    return Settings()
