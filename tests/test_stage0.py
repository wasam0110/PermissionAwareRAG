from pathlib import Path

from fastapi.testclient import TestClient

from backend.core.config import Settings
from backend.main import app


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["x-request-id"]


def test_client_request_id_is_preserved() -> None:
    with TestClient(app) as client:
        response = client.get("/health", headers={"X-Request-ID": "test-request-1"})
    assert response.headers["x-request-id"] == "test-request-1"


def test_readiness_has_dependency_report() -> None:
    with TestClient(app) as client:
        response = client.get("/ready")
    assert response.status_code in (200, 503)
    assert set(response.json()["dependencies"]) == {"database", "redis"}


def test_configuration_loads() -> None:
    settings = Settings(app_env="test", database_url="sqlite+aiosqlite:///./test.db", redis_url="redis://localhost")
    assert settings.app_env == "test"
    assert settings.frontend_origin.startswith("http")


def test_frontend_has_no_server_secret_names() -> None:
    contents = "\n".join(p.read_text(errors="ignore") for p in Path("frontend").rglob("*.ts*"))
    for secret_name in ("DATABASE_URL", "JWT_SECRET_KEY", "REDIS_URL", "OPENAI_API_KEY"):
        assert secret_name not in contents
