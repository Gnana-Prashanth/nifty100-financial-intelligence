import sys
import os
import pandas as pd
import pytest

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from src.etl.loader import load_excel



def test_load_companies():
    df = load_excel("data/raw/companies.xlsx")

    assert not df.empty


def test_load_profit_loss():
    df = load_excel("data/raw/profitandloss.xlsx")

    assert not df.empty


def test_load_balance_sheet():
    df = load_excel("data/raw/balancesheet.xlsx")

    assert not df.empty


def test_load_cashflow():
    df = load_excel("data/raw/cashflow.xlsx")

    assert not df.empty


def test_companies_has_company_id():
    df = load_excel("data/raw/companies.xlsx")

    assert "id" in df.columns


def test_profit_loss_has_year():
    df = load_excel("data/raw/profitandloss.xlsx")

    assert "year" in df.columns


def test_balance_sheet_has_year():
    df = load_excel("data/raw/balancesheet.xlsx")

    assert "year" in df.columns


def test_cashflow_has_year():
    df = load_excel("data/raw/cashflow.xlsx")

    assert "year" in df.columns


def test_invalid_path():
    with pytest.raises(FileNotFoundError):
        load_excel("wrong.xlsx")


def test_returns_dataframe():
    df = load_excel("data/raw/companies.xlsx")

    assert isinstance(df, pd.DataFrame)


#pytest tests/etl -v