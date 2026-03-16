# Prompt Lens

**Análise de prompts** com RAG (boas práticas), cache e observabilidade. **Full-stack:** API FastAPI + **interface web** React.

**Stack:** Python 3.11+, FastAPI, React 18, Vite, Docker Compose.

---

## Frontend (web app)

A aplicação web em `frontend/` permite colar um prompt, clicar em **Analisar** e ver em tempo real:

- **Resumo** e **nota de clareza (1–10)** da LLM  
- **Métricas**: palavras, caracteres, linhas, tokens estimados  
- **Flags**: tem instruções? tem exemplos?  
- **Sugestões de melhoria** e **seções detectadas**  

A UI consome a API (`POST /api/v1/analyze`), exibe erros com `request_id` quando a API retorna erro estruturado e trata rate limit (429) com mensagem amigável.

**Como rodar o front:** `cd frontend` → `npm install` → `npm run dev` → http://localhost:5173

---

## Features (destaques para recrutadores)

- **RAG (Retrieval-Augmented Generation)** — Análise do prompt enriquecida com chunks de boas práticas recuperados **localmente** por sobreposição de termos (sem embeddings, sem API extra).
- **Cache em memória** — Resultados de análise cacheados por hash do prompt (TTL configurável), reduzindo chamadas à LLM.
- **Rate limiting** — Limite de requisições por IP por minuto (configurável), com resposta 429 estruturada.
- **Request ID** — Todo request e response incluem `X-Request-ID` para rastreabilidade em logs e suporte.
- **Erros estruturados** — Respostas de erro padronizadas com `detail`, `request_id` e `code` (ex.: `VALIDATION_ERROR`, `RATE_LIMIT_EXCEEDED`).
- **Health check enriquecido** — `GET /health` com `version`, `uptime_seconds` e status de dependências (ex.: `llm_configured`).
- **Métricas simples** — `GET /api/v1/stats` com total de análises (útil para dashboards e monitoramento).
- **OpenAPI com exemplos** — Documentação em `/docs` e `/redoc` com exemplos de request/response.
- **Clean Architecture** — Domínio, use cases, ports (interfaces) e adapters (infra) bem separados.

---

## Estrutura

```
prompt-lens/
├── docker-compose.yml   # api (8000) + web (5173)
├── backend/             # FastAPI, Clean Architecture
│   └── src/
│       ├── domain/           # entidades
│       ├── application/      # use cases + interfaces (ports)
│       ├── infrastructure/   # LLM, cache, RAG, stats
│       └── presentation/     # API, middleware, errors
├── frontend/            # React + Vite
└── README.md
```

---

## Como rodar

Há um **Makefile** na raiz do projeto. Use `make help` para ver todos os comandos.

```bash
make help          # lista os comandos
make install       # instala backend + frontend
make run-backend   # sobe a API (8000)
make run-frontend  # sobe o front (5173)
make docker-build  # sobe tudo com Docker
make test          # testes do backend
make lint          # ruff no backend
```

**Docker:** copie `.env.example` para `.env`, configure `OPENAI_API_KEY` e depois:

```bash
make docker-build
# ou: docker compose up --build
```

→ **Web app** http://localhost:5173 · **API** http://localhost:8000 · **Docs** http://localhost:8000/docs

**Local – backend:**  
`make install-backend` (uma vez) e depois `make run-backend`

**Local – frontend:**  
`make install-frontend` (uma vez) e depois `make run-frontend`

---

## Configuração (.env)

Apenas duas variáveis:

| Variável | Descrição | Default |
|----------|-----------|---------|
| `OPENAI_API_KEY` | Chave da API OpenAI (obrigatória) | — |
| `OPENAI_MODEL` | Modelo de chat (ex.: gpt-4o-mini) | `gpt-4o-mini` |

Cache (em memória) e rate limit são obrigatórios e usam valores fixos no código. O retrieval RAG é local (por termos), sem embeddings.

---

## Endpoints principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Health check (versão, uptime, checks) |
| GET | `/api/v1/stats` | Total de análises |
| POST | `/api/v1/analyze` | Analisa um prompt (RAG + LLM); sujeito a rate limit |

---

## License

MIT
