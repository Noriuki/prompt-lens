"""Stub de implementação. Substitua por implementações reais (LLM, cache, etc.)."""

from src.application.interfaces import ExampleGateway


class StubExampleGateway(ExampleGateway):
    """Implementação stub: levanta NotImplementedError."""

    def do_something(self, value: str) -> str:
        raise NotImplementedError("Implemente o gateway em infrastructure")
