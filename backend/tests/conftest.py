"""Fixtures para testes."""

from typing import List

import pytest
from fastapi.testclient import TestClient

from src.application.interfaces.llm_analyzer import LLMAnalysisResult, LLMAnalyzerGateway
from src.application.interfaces.retriever_gateway import RetrieverGateway
from src.presentation.api.app import app
from src.presentation.api.routes import get_llm_analyzer, get_retriever


class FakeLLMGateway(LLMAnalyzerGateway):
    def analyze(self, prompt_text: str, context: List[str] | None = None) -> LLMAnalysisResult:
        return LLMAnalysisResult(
            clarity_score=7,
            has_instructions=bool(
                "escreva" in (prompt_text or "").lower()
                or "instruction" in (prompt_text or "").lower()
            ),
            has_examples="exemplo" in (prompt_text or "").lower()
            or "example" in (prompt_text or "").lower(),
            sections=["Seção 1"],
            suggestions=["Sugestão de teste."],
            summary="Resumo de teste.",
        )


class FakeRetriever(RetrieverGateway):
    def search(self, query_text: str, top_k: int = 5) -> List[str]:
        return ["Boas práticas chunk 1.", "Boas práticas chunk 2."][:top_k]


@pytest.fixture
def client():
    app.dependency_overrides[get_llm_analyzer] = lambda: FakeLLMGateway()
    app.dependency_overrides[get_retriever] = lambda: FakeRetriever()
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(get_llm_analyzer, None)
        app.dependency_overrides.pop(get_retriever, None)
