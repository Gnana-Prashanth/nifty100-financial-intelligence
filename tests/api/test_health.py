import sys
import os

from fastapi.testclient import TestClient

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from src.api.main import app

client = TestClient(app)


def test_health_status_code():
    response = client.get("/api/v1/health")

    assert response.status_code == 200


def test_health_status():
    response = client.get("/api/v1/health")

    data = response.json()

    assert data["status"] == "ok"


def test_health_version():
    response = client.get("/api/v1/health")

    data = response.json()

    assert data["version"] == "1.0.0"


def test_health_has_db_row_counts():
    response = client.get("/api/v1/health")

    data = response.json()

    assert "db_row_counts" in data


def test_health_table_count():
    response = client.get("/api/v1/health")

    data = response.json()

    assert len(data["db_row_counts"]) == 10


def test_health_expected_tables():
    response = client.get("/api/v1/health")

    tables = response.json()["db_row_counts"]

    expected = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "sectors",
        "market_cap",
        "financial_ratios"
    ]

    for table in expected:
        assert table in tables


def test_health_row_counts_are_integers():
    response = client.get("/api/v1/health")

    tables = response.json()["db_row_counts"]

    for value in tables.values():
        assert isinstance(value, int)


def test_health_uptime_exists():
    response = client.get("/api/v1/health")

    data = response.json()

    assert "uptime_seconds" in data

    assert isinstance(data["uptime_seconds"], (int, float))