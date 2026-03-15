"""Embeddings via OpenAI API."""

from openai import OpenAI

from src.application.interfaces.embeddings_gateway import EmbeddingsGateway
from src.config import Settings


class OpenAIEmbeddings(EmbeddingsGateway):
    """Implementação de embeddings usando a API OpenAI."""

    def __init__(self, settings: Settings) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key or None)
        self._model = settings.openai_embedding_model

    def embed(self, text: str) -> list[float]:
        if not (text or "").strip():
            return []
        response = self._client.embeddings.create(
            model=self._model,
            input=text.strip()[:8191],  # limite do modelo
        )
        return list(response.data[0].embedding)
