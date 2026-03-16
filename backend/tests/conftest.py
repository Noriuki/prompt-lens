import pytest
from fastapi.testclient import TestClient

from src.application.interfaces.llm_analyzer import LLMAnalysisResult, LLMAnalyzerGateway
from src.presentation.api.app import app
from src.presentation.api.routes import get_llm_analyzer


class FakeLLMGateway(LLMAnalyzerGateway):
    def analyze(self, prompt_text: str) -> LLMAnalysisResult:
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


@pytest.fixture
def client():
    app.dependency_overrides[get_llm_analyzer] = lambda: FakeLLMGateway()
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(get_llm_analyzer, None)
