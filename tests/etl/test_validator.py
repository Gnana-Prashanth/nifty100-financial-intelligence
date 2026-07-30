import sys
import os
import pandas as pd
import pytest

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../"
        )
    )
)

from src.etl.validator import (
    check_duplicates,
    foreign_key_check,
    null_value_check,
    balance_sheet_check,
    opm_check,
    positive_sales_check
)


# ================ Duplicate Tests ==================

def test_check_duplicates_none():

    df = pd.DataFrame({
        "company_id": ["TCS", "INFY"],
        "year": ["2024", "2024"]
    })

    assert check_duplicates(df) == 0


def test_check_duplicates_present():

    df = pd.DataFrame({
        "company_id": ["TCS", "TCS"],
        "year": ["2024", "2024"]
    })

    assert check_duplicates(df) == 1


# =============== Foreign Key Tests =================

def test_foreign_key_valid():

    child = pd.DataFrame({
        "company_id": [1, 2]
    })

    parent = pd.DataFrame({
        "id": [1, 2, 3]
    })

    assert foreign_key_check(child, parent) == []


def test_foreign_key_extra():

    child = pd.DataFrame({
        "company_id": [1, 5]
    })

    parent = pd.DataFrame({
        "id": [1, 2]
    })

    assert foreign_key_check(child, parent) == [5]


# =============== Null Value Tests =================

def test_null_value_none():

    df = pd.DataFrame({
        "sales": [10, 20]
    })

    result = null_value_check(df)

    assert result.empty


def test_null_value_present():

    df = pd.DataFrame({
        "sales": [10, None]
    })

    result = null_value_check(df)

    assert result["sales"] == 1


# ============== Balance Sheet Tests ================

def test_balance_sheet_valid():

    df = pd.DataFrame({
        "total_assets": [100],
        "total_liabilities": [100]
    })

    assert balance_sheet_check(df) == 0


def test_balance_sheet_failure():

    df = pd.DataFrame({
        "total_assets": [100],
        "total_liabilities": [80]
    })

    assert balance_sheet_check(df) == 1


# ================== OPM Tests ====================

def test_opm_valid():

    df = pd.DataFrame({
        "sales": [100],
        "operating_profit": [25],
        "opm_percentage": [25]
    })

    assert len(opm_check(df)) == 0


def test_opm_failure():

    df = pd.DataFrame({
        "sales": [100],
        "operating_profit": [25],
        "opm_percentage": [40]
    })

    assert len(opm_check(df)) == 1


# ============= Positive Sales Tests ===============

def test_positive_sales_valid():

    df = pd.DataFrame({
        "sales": [100, 200]
    })

    assert positive_sales_check(df) == 0


def test_positive_sales_failure():

    df = pd.DataFrame({
        "sales": [100, -50]
    })

    assert positive_sales_check(df) == 1
