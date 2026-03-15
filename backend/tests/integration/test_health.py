"""Teste de integração: health check e observabilidade."""

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "uptime_seconds" in data
    assert "checks" in data
    assert "llm_configured" in data["checks"]


def test_health_returns_request_id(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert "X-Request-ID" in r.headers


def test_stats(client):
    r = client.get("/api/v1/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_analyses" in data
    assert isinstance(data["total_analyses"], int)
