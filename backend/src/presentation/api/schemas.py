"""Pydantic schemas para request/response."""

from pydantic import BaseModel, Field


class PingResponse(BaseModel):
    pong: bool = True


class AnalyzeRequest(BaseModel):
    """Corpo da requisição de análise de prompt."""

    prompt: str = Field(..., description="Texto do prompt a analisar", max_length=50_000)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Você é um assistente. Escreva um resumo em 3 parágrafos sobre boas práticas de prompts para LLMs.",
                }
            ]
        }
    }


class AnalyzeResponse(BaseModel):
    """Resultado da análise: métricas e feedback da LLM."""

    word_count: int
    char_count: int
    line_count: int
    estimated_tokens: int
    sections: list[str]
    has_instructions: bool
    has_examples: bool
    clarity_score: int
    suggestions: list[str]
    summary: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "word_count": 28,
                    "char_count": 145,
                    "line_count": 1,
                    "estimated_tokens": 36,
                    "sections": ["Instrução de papel", "Tarefa"],
                    "has_instructions": True,
                    "has_examples": False,
                    "clarity_score": 8,
                    "suggestions": ["Adicione um exemplo de saída esperada."],
                    "summary": "Prompt claro com papel definido; poderia incluir exemplos.",
                }
            ]
        }
    }


class StatsResponse(BaseModel):
    """Métricas agregadas da API."""

    total_analyses: int = Field(..., description="Total de análises realizadas desde o start")
