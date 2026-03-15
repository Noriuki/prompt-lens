"""Port para cache (análise de prompt, etc.)."""

from abc import ABC, abstractmethod
from typing import Optional


class CacheGateway(ABC):
    """Interface para armazenamento em cache."""

    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        """Retorna o valor associado à chave ou None se não existir/expirado."""
        ...

    @abstractmethod
    def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        """Armazena o valor com TTL opcional em segundos."""
        ...

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove a chave do cache."""
        ...
