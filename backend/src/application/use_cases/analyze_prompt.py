"""Use case: analisar um prompt (métricas locais + LLM com RAG, cache opcional)."""

import hashlib
import json
from typing import Optional

from src.application.interfaces.cache_gateway import CacheGateway
from src.application.interfaces.llm_analyzer import LLMAnalysisResult, LLMAnalyzerGateway
from src.application.interfaces.retriever_gateway import RetrieverGateway
from src.domain.entities.prompt_analysis import PromptAnalysis

RAG_TOP_K = 5


def _estimate_tokens(text: str) -> int:
    """Estimativa grosseira: ~4 chars por token."""
    if not text.strip():
        return 0
    return max(1, len(text) // 4)


def _cache_key(prompt_text: str) -> str:
    """Chave de cache baseada no conteúdo normalizado do prompt."""
    normalized = (prompt_text or "").strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def analyze_prompt(
    prompt_text: str,
    llm_gateway: LLMAnalyzerGateway,
    retriever: Optional[RetrieverGateway] = None,
    cache: Optional[CacheGateway] = None,
    cache_ttl_seconds: Optional[int] = None,
) -> PromptAnalysis:
    """
    Analisa o prompt: recupera contexto via RAG, chama a LLM com esse contexto e opcionalmente usa cache.
    """
    text = prompt_text or ""
    words = text.split()
    lines = [l for l in text.splitlines() if l.strip()]
    context: list[str] = []
    if retriever and text.strip():
        context = retriever.search(text, top_k=RAG_TOP_K)

    def build_result(llm_result: LLMAnalysisResult) -> PromptAnalysis:
        return PromptAnalysis(
            word_count=len(words),
            char_count=len(text),
            line_count=len(lines) or (1 if text.strip() else 0),
            estimated_tokens=_estimate_tokens(text),
            sections=llm_result.sections,
            has_instructions=llm_result.has_instructions,
            has_examples=llm_result.has_examples,
            clarity_score=llm_result.clarity_score,
            suggestions=llm_result.suggestions,
            summary=llm_result.summary,
        )

    if cache:
        key = _cache_key(text)
        cached = cache.get(key)
        if cached:
            try:
                data = json.loads(cached)
                return build_result(LLMAnalysisResult.from_dict(data))
            except (json.JSONDecodeError, TypeError, KeyError):
                pass

    llm_result = llm_gateway.analyze(text, context=context if context else None)
    if cache and cache_ttl_seconds is not None:
        cache.set(key, json.dumps(llm_result.to_dict()), ttl_seconds=cache_ttl_seconds)
    elif cache:
        cache.set(key, json.dumps(llm_result.to_dict()))

    return build_result(llm_result)
