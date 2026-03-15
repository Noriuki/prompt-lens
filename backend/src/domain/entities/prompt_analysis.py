"""Resultado da análise de um prompt (métricas locais + resultado da LLM)."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PromptAnalysis:
    """Métricas locais e análise semântica da LLM (RAG)."""

    word_count: int
    char_count: int
    line_count: int
    estimated_tokens: int
    sections: List[str]
    has_instructions: bool
    has_examples: bool
    clarity_score: int  # 1-10, da LLM
    suggestions: List[str]
    summary: str
