"""FastAPI: API com observabilidade, rate limit e health check."""

import logging
import sys
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from src.config import get_settings
from src.presentation.api.errors import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from src.presentation.api.middleware import RequestIDMiddleware
from src.presentation.api.routes import router

logger = logging.getLogger(__name__)

_start_time: float = 0.0


def _version() -> str:
    try:
        from importlib.metadata import version
        return version("prompt-lens")
    except Exception:
        return "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _start_time
    _start_time = time.monotonic()
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
    )
    logger.info("Prompt Lens version=%s", _version())
    yield


app = FastAPI(
    title="Prompt Lens API",
    description="API para análise de prompts com cache e métricas.",
    version=_version(),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def index():
    return {"name": "Prompt Lens", "version": _version(), "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    """Health check com versão e status das dependências (para probes e dashboards)."""
    settings = get_settings()
    llm_configured = bool(settings.openai_api_key and settings.openai_api_key.strip())
    uptime_seconds = round(time.monotonic() - _start_time, 1) if _start_time else 0
    return {
        "status": "ok",
        "version": _version(),
        "uptime_seconds": uptime_seconds,
        "checks": {
            "llm_configured": llm_configured,
        },
    }
