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


def test_sectors_status_code():
    response = client.get("/api/v1/sectors")

    assert response.status_code == 200


def test_sectors_returns_list():
    response = client.get("/api/v1/sectors")

    assert isinstance(response.json(), list)


def test_total_sectors():
    response = client.get("/api/v1/sectors")

    data = response.json()

    assert len(data) == 10


def test_sector_required_fields():
    response = client.get("/api/v1/sectors")

    sector = response.json()[0]

    expected = [
        "sector",
        "company_count",
        "median_roe",
        "median_pe",
        "median_de"
    ]

    for field in expected:
        assert field in sector


def test_sector_companies_status():
    response = client.get(
        "/api/v1/sectors/Information Technology/companies"
    )

    assert response.status_code == 200


def test_sector_companies_returns_list():
    response = client.get(
        "/api/v1/sectors/Information Technology/companies"
    )

    assert isinstance(response.json(), list)


def test_sector_companies_are_correct():
    response = client.get(
        "/api/v1/sectors/Information Technology/companies"
    )

    data = response.json()

    for company in data:
        assert company["company_name"] is not None
        assert company["year"] != "TTM"


def test_invalid_sector():
    response = client.get(
        "/api/v1/sectors/INVALID/companies"
    )

    assert response.status_code == 200
    assert response.json() == []