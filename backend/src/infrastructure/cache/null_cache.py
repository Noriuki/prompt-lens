"""Cache que não armazena nada (cache desabilitado)."""

from typing import Optional

from src.application.interfaces.cache_gateway import CacheGateway


class NullCache(CacheGateway):
    """Implementação que não persiste dados; get sempre retorna None."""

    def get(self, key: str) -> Optional[str]:
        return None

    def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        pass

    def delete(self, key: str) -> None:
        pass
