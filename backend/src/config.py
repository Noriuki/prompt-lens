"""Configuração a partir de variáveis de ambiente."""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    cors_origins: str = Field(default="*", description="CORS origins (comma-separated or *)")
    log_level: str = Field(default="INFO", description="LOG_LEVEL")
    openai_api_key: str = Field(default="", description="OPENAI_API_KEY para análise via LLM")
    openai_model: str = Field(default="gpt-4o-mini", description="Modelo OpenAI (ex.: gpt-4o-mini)")
    openai_embedding_model: str = Field(
        default="text-embedding-3-small", description="Modelo de embeddings OpenAI"
    )
    cache_enabled: bool = Field(default=True, description="Habilitar cache da análise (em memória)")
    cache_ttl_seconds: int = Field(default=3600, description="TTL do cache em segundos")
    rate_limit_per_minute: int = Field(
        default=20,
        description="Máximo de análises por IP por minuto (0 = desativado)",
    )

    def cors_origins_list(self) -> List[str]:
        if not self.cors_origins or self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
