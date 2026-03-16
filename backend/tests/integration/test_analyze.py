"""Teste de integração: POST /api/v1/analyze (LLM mockado no conftest)."""

def test_analyze_returns_metrics_and_llm_fields(client):
    r = client.post("/api/v1/analyze", json={"prompt": "Hello world. Escreva um resumo."})
    assert r.status_code == 200
    data = r.json()
    assert data["word_count"] == 5
    assert data["char_count"] == 32
    assert data["line_count"] == 1
    assert "estimated_tokens" in data
    assert "sections" in data
    assert data["has_instructions"] is True
    assert "clarity_score" in data
    assert "suggestions" in data
    assert "summary" in data


def test_analyze_empty_prompt(client):
    r = client.post("/api/v1/analyze", json={"prompt": ""})
    assert r.status_code == 200
    data = r.json()
    assert data["word_count"] == 0
    assert data["char_count"] == 0
    assert data["clarity_score"] == 0
    assert data["summary"] == "Prompt vazio."


def test_analyze_missing_body_returns_422_with_request_id(client):
    r = client.post("/api/v1/analyze", json={})
    assert r.status_code == 422
    data = r.json()
    assert "request_id" in data
    assert data.get("code") == "VALIDATION_ERROR"


def test_analyze_increments_stats(client):
    r0 = client.get("/api/v1/stats")
    count_before = r0.json()["total_analyses"]
    client.post("/api/v1/analyze", json={"prompt": "Teste."})
    r1 = client.get("/api/v1/stats")
    assert r1.json()["total_analyses"] == count_before + 1
