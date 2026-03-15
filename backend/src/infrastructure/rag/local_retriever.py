"""Retriever RAG local: similaridade por sobreposição de termos (sem embeddings)."""

import re
from typing import List

from src.application.interfaces.retriever_gateway import RetrieverGateway


def _tokenize(text: str) -> set[str]:
    """Extrai tokens em minúsculo (palavras com 2+ caracteres)."""
    text = (text or "").lower().strip()
    if not text:
        return set()
    tokens = set(re.findall(r"\b[a-z0-9áéíóúàèìòùâêîôûãõç]{2,}\b", text))
    return tokens


def _score_chunk(query_tokens: set[str], chunk_tokens: set[str]) -> float:
    """Score por Jaccard-like: termos da query que aparecem no chunk."""
    if not query_tokens:
        return 0.0
    overlap = len(query_tokens & chunk_tokens) / len(query_tokens)
    return overlap


class LocalRetriever(RetrieverGateway):
    """Recupera chunks por sobreposição de termos (100% local, sem API)."""

    def __init__(self, chunks: List[str]) -> None:
        self._chunks = [c for c in chunks if (c or "").strip()]
        self._chunk_tokens: List[set[str]] = [_tokenize(c) for c in self._chunks]

    def search(self, query_text: str, top_k: int = 5) -> List[str]:
        if not (query_text or "").strip():
            return []
        query_tokens = _tokenize(query_text)
        if not query_tokens:
            return self._chunks[:top_k]
        scored: List[tuple[float, str]] = []
        for chunk, ct in zip(self._chunks, self._chunk_tokens):
            score = _score_chunk(query_tokens, ct)
            scored.append((score, chunk))
        scored.sort(key=lambda x: -x[0])
        return [chunk for _, chunk in scored[:top_k]]
