import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../"
        )
    )
)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_screener_status_code():
    response = client.get("/api/v1/screener")

    assert response.status_code == 200


def test_screener_returns_list():
    response = client.get("/api/v1/screener")

    assert isinstance(response.json(), list)


def test_min_roe_filter():
    response = client.get(
        "/api/v1/screener?min_roe=15"
    )

    data = response.json()

    for company in data:
        assert company["return_on_equity_pct"] >= 15


def test_max_de_filter():
    response = client.get(
        "/api/v1/screener?max_de=1"
    )

    data = response.json()

    for company in data:
        assert company["debt_to_equity"] <= 1


def test_sector_filter():
    response = client.get(
        "/api/v1/screener?sector=Information Technology"
    )

    data = response.json()

    for company in data:
        assert company["broad_sector"] == "Information Technology"


def test_max_pe_filter():
    response = client.get(
        "/api/v1/screener?max_pe=30"
    )

    data = response.json()

    for company in data:
        assert company["pe_ratio"] <= 30


def test_invalid_min_roe():
    response = client.get(
        "/api/v1/screener?min_roe=-1"
    )

    assert response.status_code == 422


def test_required_fields_present():
    response = client.get("/api/v1/screener")

    company = response.json()[0]

    expected = [
        "id",
        "company_name",
        "broad_sector",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "pe_ratio"
    ]

    for field in expected:
        assert field in company