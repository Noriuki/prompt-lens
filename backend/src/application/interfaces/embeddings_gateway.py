"""Port para geração de embeddings."""

from abc import ABC, abstractmethod
from typing import List


class EmbeddingsGateway(ABC):
    """Interface para obter vetores de embedding de texto."""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Retorna o vetor de embedding do texto (dimensão fixa do modelo)."""
        ...
