"""Exemplo de port (gateway). Adicione os que precisar (LLM, cache, etc.)."""

from abc import ABC, abstractmethod


class ExampleGateway(ABC):
    """Interface para dependência externa. Implemente em infrastructure."""

    @abstractmethod
    def do_something(self, value: str) -> str:
        """Implemente: chamada ao serviço externo."""
        ...
