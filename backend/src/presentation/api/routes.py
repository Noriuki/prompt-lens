"""Rotas da API."""

from fastapi import APIRouter, Depends, HTTPException, Request

from src.application.interfaces.cache_gateway import CacheGateway
from src.application.interfaces.llm_analyzer import LLMAnalyzerGateway
from src.application.interfaces.retriever_gateway import RetrieverGateway
from src.application.use_cases.analyze_prompt import analyze_prompt
from src.config import get_settings
from src.infrastructure.cache.memory_cache import InMemoryCache
from src.infrastructure.cache.null_cache import NullCache
from src.infrastructure.embeddings.openai_embeddings import OpenAIEmbeddings
from src.infrastructure.llm.openai_analyzer import OpenAIAnalyzer
from src.infrastructure.rag.knowledge import KNOWLEDGE_CHUNKS
from src.infrastructure.rag.memory_retriever import MemoryRAGRetriever
from src.infrastructure.stats import get_analyses_count, increment_analyses
from src.presentation.api.rate_limit import enforce_rate_limit
from src.presentation.api.schemas import AnalyzeRequest, AnalyzeResponse, StatsResponse

router = APIRouter(tags=["api"])


def get_llm_analyzer() -> LLMAnalyzerGateway:
    settings = get_settings()
    if not (settings.openai_api_key or settings.openai_api_key.strip()):
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY não configurada. Defina no .env para usar análise via LLM.",
        )
    return OpenAIAnalyzer(settings)


def get_cache() -> CacheGateway:
    settings = get_settings()
    if settings.cache_enabled:
        return InMemoryCache(default_ttl_seconds=settings.cache_ttl_seconds)
    return NullCache()


def get_retriever() -> RetrieverGateway:
    settings = get_settings()
    if not (settings.openai_api_key or settings.openai_api_key.strip()):
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY não configurada. Defina no .env para análise com RAG.",
        )
    embeddings = OpenAIEmbeddings(settings)
    return MemoryRAGRetriever(embeddings, KNOWLEDGE_CHUNKS)


@router.get("/ping")
def ping():
    """Confirma que a API está viva."""
    return {"pong": True}


@router.get("/stats", response_model=StatsResponse)
def stats():
    """Métricas simples: total de análises realizadas (útil para dashboards)."""
    return StatsResponse(total_analyses=get_analyses_count())


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analisar prompt",
    response_description="Métricas, clareza, sugestões e resumo da análise.",
)
def analyze(
    request: AnalyzeRequest,
    req: Request,
    llm: LLMAnalyzerGateway = Depends(get_llm_analyzer),
    retriever: RetrieverGateway = Depends(get_retriever),
    cache: CacheGateway = Depends(get_cache),
    _: None = Depends(enforce_rate_limit),
) -> AnalyzeResponse:
    """Analisa um prompt via LLM com RAG (boas práticas recuperadas por similaridade). Sujeito a rate limit por IP."""
    settings = get_settings()
    result = analyze_prompt(
        request.prompt,
        llm,
        retriever=retriever,
        cache=cache,
        cache_ttl_seconds=settings.cache_ttl_seconds if settings.cache_enabled else None,
    )
    increment_analyses()
    return AnalyzeResponse(
        word_count=result.word_count,
        char_count=result.char_count,
        line_count=result.line_count,
        estimated_tokens=result.estimated_tokens,
        sections=result.sections,
        has_instructions=result.has_instructions,
        has_examples=result.has_examples,
        clarity_score=result.clarity_score,
        suggestions=result.suggestions,
        summary=result.summary,
    )
