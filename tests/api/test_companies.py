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


def test_list_companies_status_code():
    response = client.get("/api/v1/companies")

    assert response.status_code == 200


def test_list_companies_returns_92_records():
    response = client.get("/api/v1/companies")

    data = response.json()

    assert len(data) == 92


def test_company_list_is_list():
    response = client.get("/api/v1/companies")

    assert isinstance(response.json(), list)


def test_company_contains_required_fields():
    response = client.get("/api/v1/companies")

    company = response.json()[0]

    expected = [
        "company_id",
        "company_name",
        "broad_sector",
        "sub_sector",
        "market_cap_category",
        "roe_pct",
        "roce_pct"
    ]

    for field in expected:
        assert field in company


def test_get_tcs_profile():
    response = client.get("/api/v1/companies/TCS")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "TCS"


def test_get_invalid_company():
    response = client.get("/api/v1/companies/INVALID")

    assert response.status_code == 404

    assert response.json()["detail"] == "Ticker not found"


def test_company_search():
    response = client.get(
        "/api/v1/companies?search=TCS"
    )

    data = response.json()

    assert len(data) >= 1

    assert data[0]["company_id"] == "TCS"


def test_company_sector_filter():
    response = client.get(
        "/api/v1/companies?sector=Information Technology"
    )

    assert response.status_code == 200

    data = response.json()

    for company in data:
        assert company["broad_sector"] == "Information Technology"


def test_market_cap_filter():
    response = client.get(
        "/api/v1/companies?market_cap_category=Large Cap"
    )

    assert response.status_code == 200

    data = response.json()

    for company in data:
        assert company["market_cap_category"] == "Large Cap"