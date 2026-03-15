"""Retriever RAG em memória: embeddings + similaridade por cosseno."""

import math
from threading import Lock
from typing import List

from src.application.interfaces.embeddings_gateway import EmbeddingsGateway
from src.application.interfaces.retriever_gateway import RetrieverGateway


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class MemoryRAGRetriever(RetrieverGateway):
    """Recupera chunks por similaridade semântica (embedding + cosseno). Inicialização lazy."""

    def __init__(self, embeddings_gateway: EmbeddingsGateway, chunks: List[str]) -> None:
        self._embeddings = embeddings_gateway
        self._chunks = list(chunks)
        self._store: List[List[float]] = []  # embeddings dos chunks
        self._lock = Lock()
        self._initialized = False

    def _ensure_initialized(self) -> None:
        with self._lock:
            if self._initialized:
                return
            for text in self._chunks:
                if (text or "").strip():
                    vec = self._embeddings.embed(text)
                    if vec:
                        self._store.append(vec)
                    else:
                        self._store.append([])
                else:
                    self._store.append([])
            self._initialized = True

    def search(self, query_text: str, top_k: int = 5) -> List[str]:
        if not (query_text or "").strip():
            return []
        self._ensure_initialized()
        query_embedding = self._embeddings.embed(query_text)
        if not query_embedding:
            return []
        scored: List[tuple[float, str]] = []
        for i, chunk in enumerate(self._chunks):
            if not chunk.strip():
                continue
            vec = self._store[i] if i < len(self._store) else []
            if not vec:
                continue
            sim = _cosine_similarity(query_embedding, vec)
            scored.append((sim, chunk))
        scored.sort(key=lambda x: -x[0])
        return [text for _, text in scored[:top_k]]
