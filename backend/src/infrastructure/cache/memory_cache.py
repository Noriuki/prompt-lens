"""Cache em memória com TTL opcional. É o cache padrão da aplicação (CACHE_ENABLED=true)."""

import time
from threading import Lock
from typing import Optional

from src.application.interfaces.cache_gateway import CacheGateway


class InMemoryCache(CacheGateway):
    """Implementação de cache em memória. Suporta TTL por entrada."""

    def __init__(self, default_ttl_seconds: Optional[int] = 3600) -> None:
        self._default_ttl = default_ttl_seconds
        self._store: dict[str, tuple[str, Optional[float]]] = {}  # key -> (value, expiry_time)
        self._lock = Lock()

    def get(self, key: str) -> Optional[str]:
        with self._lock:
            if key not in self._store:
                return None
            value, expiry = self._store[key]
            if expiry is not None and time.monotonic() > expiry:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        expiry = (time.monotonic() + ttl) if ttl else None
        with self._lock:
            self._store[key] = (value, expiry)

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)
