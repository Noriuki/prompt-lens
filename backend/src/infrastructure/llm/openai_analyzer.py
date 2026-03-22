# Libraries
import json
import logging
import re
from typing import List

# Application
from openai import OpenAI

# Infrastructure
from src.application.interfaces.llm_analyzer import LLMAnalysisResult, LLMAnalyzerGateway
from src.config import Settings

# Logging
logger = logging.getLogger(__name__)

SYSTEM_PROMPT_BASE = """Você é um analisador de prompts para uso com LLMs. Analise o prompt do usuário e responda APENAS com um único objeto JSON válido, sem markdown e sem texto antes ou depois, no formato:
{
    "clarity_score": <número de 1 a 10>,
    "has_instructions": <true ou false>,
    "has_examples": <true ou false>,
    "sections": [<lista de strings: um rótulo curto por bloco/seção do prompt>],
    "suggestions": [<até 5 sugestões curtas de melhoria>],
    "summary": "<resumo em 1 ou 2 frases>"
}

Idioma: "suggestions" e "summary" no mesmo idioma do texto principal do prompt (idioma dominante das frases/regras).

Regra obrigatória para "sections": cada string deve ser um rótulo legível NO IDIOMA DOMINANTE das instruções e regras do prompt (não o idioma das tags técnicas). Se o prompt usar tags em inglês (<scheduling>, <generic>) mas as regras estiverem em português, escreva rótulos em português que descrevam o bloco (ex.: "Agendamento", "Regras gerais"), e NÃO liste só o nome da tag em inglês. Só use nomes de tags literais quando o próprio conteúdo do prompt estiver integralmente nesse idioma.
Responda somente com o JSON."""


def _parse_json_from_content(content: str) -> dict:
    """Extrai e parseia JSON do texto da resposta (pode vir com markdown)."""
    text = content.strip()
    # Remove blocos de código markdown se existirem
    if "```" in text:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            text = match.group(1).strip()
    return json.loads(text)


def _safe_list(value, default: List[str]) -> List[str]:
    if value is None:
        return default
    if isinstance(value, list):
        return [str(item) for item in value[:20]]
    return default


def _safe_int(value: int, low: int, high: int, default: int) -> int:
    if value is None or not isinstance(value, (int, float)):
        return default
    n = int(value)
    return max(low, min(high, n))


def _safe_bool(value) -> bool:
    return bool(value) if value is not None else False


def _safe_str(value, default: str = "") -> str:
    return str(value).strip() if value is not None else default


class OpenAIAnalyzer(LLMAnalyzerGateway):
    """Implementação do analisador usando OpenAI API."""

    def __init__(self, settings: Settings) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key or None)
        self._model = settings.openai_model

    def analyze(self, prompt_text: str) -> LLMAnalysisResult:
        if not (prompt_text or "").strip():
            return LLMAnalysisResult(
                clarity_score=0,
                has_instructions=False,
                has_examples=False,
                sections=[],
                suggestions=[],
                summary="Prompt vazio.",
            )
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_BASE},
                {"role": "user", "content": prompt_text},
            ],
            temperature=0.2,
        )
        raw = response.choices[0].message.content
        try:
            data = _parse_json_from_content(raw)
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning("LLM respondeu com JSON inválido: %s", e)
            return LLMAnalysisResult(
                clarity_score=5,
                has_instructions=False,
                has_examples=False,
                sections=[],
                suggestions=["Não foi possível interpretar a análise."],
                summary="Resposta da LLM em formato inválido.",
            )
        return LLMAnalysisResult(
            clarity_score=_safe_int(data.get("clarity_score"), 1, 10, 5),
            has_instructions=_safe_bool(data.get("has_instructions")),
            has_examples=_safe_bool(data.get("has_examples")),
            sections=_safe_list(data.get("sections"), []),
            suggestions=_safe_list(data.get("suggestions"), [])[:5],
            summary=_safe_str(data.get("summary"), "—"),
        )
