"""Rate limiting simples por IP (in-memory)."""

import time
from collections import defaultdict
from threading import Lock

from fastapi import HTTPException, Request

from src.config import get_settings

_store: dict[str, list[float]] = defaultdict(list)
_lock = Lock()
_WINDOW_SECONDS = 60


def enforce_rate_limit(request: Request) -> None:
    """Dependency: levanta HTTPException(429) se o IP excedeu o limite."""
    settings = get_settings()
    if settings.rate_limit_per_minute <= 0:
        return
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    with _lock:
        times = _store[client_ip]
        times[:] = [t for t in times if now - t < _WINDOW_SECONDS]
        if len(times) >= settings.rate_limit_per_minute:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {settings.rate_limit_per_minute} analyses per minute.",
            )
        times.append(now)
