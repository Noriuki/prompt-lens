"""Respostas de erro estruturadas para a API."""

from typing import Any, Optional, Union

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def _get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


def error_response(
    status_code: int,
    detail: Union[str, list, dict],
    request: Request,
    code: Optional[str] = None,
    **extra: Any,
) -> JSONResponse:
    """Resposta de erro padronizada com request_id e code."""
    payload = {
        "detail": detail,
        "request_id": _get_request_id(request),
        "code": code or "ERROR",
        **extra,
    }
    return JSONResponse(status_code=status_code, content=payload)


async def http_exception_handler(request: Request, exc) -> JSONResponse:
    """Converte HTTPException em resposta estruturada com request_id."""
    if exc.status_code == 422:
        code = "VALIDATION_ERROR"
    elif exc.status_code == 429:
        code = "RATE_LIMIT_EXCEEDED"
    elif exc.status_code == 503:
        code = "SERVICE_UNAVAILABLE"
    else:
        code = "HTTP_ERROR"
    return error_response(exc.status_code, exc.detail, request, code=code)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Adiciona request_id às respostas 422 de validação."""
    return error_response(422, exc.errors(), request, code="VALIDATION_ERROR")


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Captura exceções não tratadas e retorna 500 com request_id (sem vazar stack)."""
    return error_response(
        500,
        "Internal server error. Use the request_id to trace this in logs.",
        request,
        code="INTERNAL_ERROR",
    )
