#================ Imports =====================

import sys
import os
import pytest

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from src.etl.normalizer import (
    normalize_ticker,
    normalize_year
)


#================ Ticker Tests ==================

def test_ticker_lowercase():
    assert normalize_ticker("tcs") == "TCS"


def test_ticker_spaces():
    assert normalize_ticker("  tcs  ") == "TCS"


def test_ticker_mixed_case():
    assert normalize_ticker("InFy") == "INFY"


def test_ticker_none():
    assert normalize_ticker(None) is None


def test_ticker_empty():
    assert normalize_ticker("") == ""


#================== Year Tests ===================

def test_mar_2014():
    assert normalize_year("Mar 2014") == "2014-03"


def test_dec_2012():
    assert normalize_year("Dec 2012") == "2012-12"


def test_mar_dash_13():
    assert normalize_year("Mar-13") == "2013-03"


def test_mar_dash_14():
    assert normalize_year("Mar-14") == "2014-03"


def test_ttm():
    assert normalize_year("TTM") == "TTM"


def test_ttm_lowercase():
    assert normalize_year("ttm") == "TTM"


def test_spaces():
    assert normalize_year("  Mar 2014  ") == "2014-03"


def test_nan():
    assert normalize_year(float("nan")) is None


def test_none():
    assert normalize_year(None) is None


def test_invalid_string():
    assert normalize_year("Hello") == "Hello"


def test_numeric_year():
    assert normalize_year("2014") == "2014-01"


def test_full_date():
    assert normalize_year("2014-03-15") == "2014-03-15"


def test_dec_dash_99():
    assert normalize_year("Dec-99") == "1999-12"


def test_mar_dash_49():
    assert normalize_year("Mar-49") == "2049-03"


def test_mar_dash_50():
    assert normalize_year("Mar-50") == "1950-03"