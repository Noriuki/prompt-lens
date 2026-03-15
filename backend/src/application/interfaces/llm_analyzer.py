"""Port para análise de prompt via LLM."""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, List, Optional


@dataclass
class LLMAnalysisResult:
    """Resultado da análise semântica feita pela LLM."""

    clarity_score: int  # 1-10
    has_instructions: bool
    has_examples: bool
    sections: List[str]
    suggestions: List[str]
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LLMAnalysisResult":
        return cls(
            clarity_score=int(data.get("clarity_score", 5)),
            has_instructions=bool(data.get("has_instructions")),
            has_examples=bool(data.get("has_examples")),
            sections=list(data.get("sections") or []),
            suggestions=list(data.get("suggestions") or []),
            summary=str(data.get("summary", "")),
        )


class LLMAnalyzerGateway(ABC):
    """Interface para análise de prompt via modelo de linguagem (com contexto RAG opcional)."""

    @abstractmethod
    def analyze(self, prompt_text: str, context: Optional[List[str]] = None) -> LLMAnalysisResult:
        """Analisa o texto do prompt; context = chunks recuperados pelo RAG (opcional)."""
        ...
