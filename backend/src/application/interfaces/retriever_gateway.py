"""Port para retrieval (RAG): busca de chunks relevantes por similaridade."""

from abc import ABC, abstractmethod
from typing import List


class RetrieverGateway(ABC):
    """Interface para recuperar trechos relevantes dado um texto de consulta."""

    @abstractmethod
    def search(self, query_text: str, top_k: int = 5) -> List[str]:
        """Retorna os top_k chunks mais relevantes para o query_text (ordem de relevância)."""
        ...
