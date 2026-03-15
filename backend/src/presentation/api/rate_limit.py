"""Rate limiting por IP (in-memory). Limite fixo."""

import time
from collections import defaultdict
from threading import Lock

from fastapi import HTTPException, Request

RATE_LIMIT_PER_MINUTE = 20
_WINDOW_SECONDS = 60
_store: dict[str, list[float]] = defaultdict(list)
_lock = Lock()


def enforce_rate_limit(request: Request) -> None:
    """Dependency: levanta HTTPException(429) se o IP excedeu o limite."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    with _lock:
        times = _store[client_ip]
        times[:] = [t for t in times if now - t < _WINDOW_SECONDS]
        if len(times) >= RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {RATE_LIMIT_PER_MINUTE} analyses per minute.",
            )
        times.append(now)
