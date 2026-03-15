"""Métricas simples em memória (total de análises)."""

from threading import Lock

_lock = Lock()
_analyses_count: int = 0


def increment_analyses() -> None:
    global _analyses_count
    with _lock:
        _analyses_count += 1


def get_analyses_count() -> int:
    with _lock:
        return _analyses_count
