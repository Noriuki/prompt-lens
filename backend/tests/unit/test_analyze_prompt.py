from src.application.interfaces.llm_analyzer import LLMAnalysisResult, LLMAnalyzerGateway
from src.application.use_cases.analyze_prompt import analyze_prompt
from src.domain.entities.prompt_analysis import PromptAnalysis
from src.infrastructure.cache.memory_cache import InMemoryCache


class FakeLLMGateway(LLMAnalyzerGateway):
    def __init__(self):
        self.call_count = 0

    def analyze(self, prompt_text: str) -> LLMAnalysisResult:
        self.call_count += 1
        return LLMAnalysisResult(
            clarity_score=8,
            has_instructions=True,
            has_examples=False,
            sections=["Introdução", "Instruções"],
            suggestions=["Adicione exemplos."],
            summary="Prompt com instruções claras.",
        )


def test_analyze_uses_llm_result():
    gateway = FakeLLMGateway()
    r = analyze_prompt("Escreva um resumo em 3 parágrafos.", gateway)
    assert isinstance(r, PromptAnalysis)
    assert r.clarity_score == 8
    assert r.has_instructions is True
    assert r.has_examples is False
    assert r.sections == ["Introdução", "Instruções"]
    assert r.suggestions == ["Adicione exemplos."]
    assert r.summary == "Prompt com instruções claras."


def test_analyze_computes_local_metrics():
    gateway = FakeLLMGateway()
    r = analyze_prompt("uma duas três", gateway)
    assert r.word_count == 3
    assert r.char_count == 14
    assert r.line_count == 1
    assert r.estimated_tokens >= 1


def test_analyze_empty_prompt():
    gateway = FakeLLMGateway()
    r = analyze_prompt("", gateway)
    assert r.word_count == 0
    assert r.char_count == 0
    assert r.line_count == 0
    assert r.estimated_tokens == 0


def test_analyze_uses_cache_on_second_call():
    gateway = FakeLLMGateway()
    cache = InMemoryCache(default_ttl_seconds=60)
    prompt = "Mesmo prompt duas vezes."
    analyze_prompt(prompt, gateway, cache=cache, cache_ttl_seconds=60)
    assert gateway.call_count == 1
    analyze_prompt(prompt, gateway, cache=cache, cache_ttl_seconds=60)
    assert gateway.call_count == 1  # cache hit, LLM não chamada de novo
