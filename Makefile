# Prompt Lens — comandos via Make
# Uso: make help

.PHONY: help install install-backend install-frontend run run-backend run-frontend docker-up docker-down docker-build test test-backend lint lint-backend clean

# Default: mostra os comandos disponíveis
help:
	@echo "Prompt Lens — comandos disponíveis:"
	@echo ""
	@echo "  make install          Instala dependências (backend + frontend)"
	@echo "  make install-backend  Cria venv e instala deps do backend"
	@echo "  make install-frontend Instala deps do frontend (npm install)"
	@echo ""
	@echo "  make run-backend      Sobe a API (porta 8000)"
	@echo "  make run-frontend     Sobe o frontend (porta 5173)"
	@echo "  make run              Sobe backend e frontend (dois terminais)"
	@echo ""
	@echo "  make docker-up        Sobe API + web com Docker Compose"
	@echo "  make docker-down      Para os containers"
	@echo "  make docker-build     Build e sobe (docker compose up --build)"
	@echo ""
	@echo "  make test             Roda testes do backend (pytest)"
	@echo "  make lint             Roda lint do backend (ruff)"
	@echo "  make clean            Remove cache e artefatos"
	@echo ""

# --- Instalação ---
install: install-backend install-frontend

install-backend:
	cd backend && python3 -m venv .venv
	cd backend && .venv/bin/pip install --upgrade pip
	cd backend && .venv/bin/pip install -e ".[dev]"

install-frontend:
	cd frontend && npm install

# --- Execução local ---
run-backend:
	cd backend && .venv/bin/python run.py

run-frontend:
	cd frontend && npm run dev

# run: exibe instrução (não dá para rodar dois processos em foreground no mesmo make)
run:
	@echo "Rode em dois terminais:"
	@echo "  Terminal 1: make run-backend"
	@echo "  Terminal 2: make run-frontend"

# --- Docker ---
docker-up:
	docker compose up

docker-down:
	docker compose down

docker-build:
	docker compose up --build

# --- Testes e qualidade ---
test: test-backend

test-backend:
	cd backend && .venv/bin/python -m pytest tests/ -v

lint: lint-backend

lint-backend:
	cd backend && .venv/bin/ruff check src tests

# --- Limpeza ---
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cache Python removido. Para limpar node_modules: cd frontend && rm -rf node_modules"
