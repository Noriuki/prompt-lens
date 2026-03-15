"""Exemplo de interface de repositório. Substitua por suas entidades."""

from abc import ABC, abstractmethod


class ExampleRepository(ABC):
    """Interface de repositório (port). Implemente em infrastructure."""

    @abstractmethod
    def get(self, id: str):
        """Implemente: buscar por id."""
        ...
