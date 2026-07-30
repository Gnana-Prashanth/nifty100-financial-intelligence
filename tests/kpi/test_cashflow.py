#=============== Imports ====================

import sys
import os
import pytest

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../"
        )
    )
)


from src.analytics.cashflow import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)


#================ Free Cash Flow ===============

def test_free_cash_flow_positive():
    assert free_cash_flow(500, -200) == 300


def test_free_cash_flow_negative():
    assert free_cash_flow(-100, -50) == -150


#============== CFO Quality Score ===============

def test_cfo_quality_high():
    score, label = cfo_quality_score(200, 100)

    assert score == 2.0
    assert label == "High Quality"


def test_cfo_quality_moderate():
    score, label = cfo_quality_score(75, 100)

    assert score == 0.75
    assert label == "Moderate"


def test_cfo_quality_accrual():
    score, label = cfo_quality_score(30, 100)

    assert score == 0.30
    assert label == "Accrual Risk"


def test_cfo_quality_zero_pat():
    score, label = cfo_quality_score(100, 0)

    assert score is None
    assert label is None


#=============== CapEx Intensity ================

def test_capex_asset_light():
    value, label = capex_intensity(-20, 1000)

    assert value == 2.0
    assert label == "Asset Light"


def test_capex_moderate():
    value, label = capex_intensity(-50, 1000)

    assert value == 5.0
    assert label == "Moderate"


def test_capex_capital_intensive():
    value, label = capex_intensity(-120, 1000)

    assert value == 12.0
    assert label == "Capital Intensive"


def test_capex_zero_sales():
    value, label = capex_intensity(-100, 0)

    assert value is None
    assert label is None


#=============== FCF Conversion ================

def test_fcf_conversion_normal():
    assert fcf_conversion_rate(300, 400) == 75.0


def test_fcf_conversion_zero_profit():
    assert fcf_conversion_rate(300, 0) is None


#========= Capital Allocation Pattern ===========

def test_pattern_reinvestor():
    assert (
        capital_allocation_pattern(
            100,
            -50,
            -20
        )
        == "Reinvestor"
    )


def test_pattern_shareholder_returns():
    assert (
        capital_allocation_pattern(
            100,
            -50,
            -20,
            "High Quality"
        )
        == "Shareholder Returns"
    )


def test_pattern_liquidating_assets():
    assert (
        capital_allocation_pattern(
            100,
            50,
            -10
        )
        == "Liquidating Assets"
    )


def test_pattern_distress():
    assert (
        capital_allocation_pattern(
            -100,
            50,
            40
        )
        == "Distress Signal"
    )


def test_pattern_growth_debt():
    assert (
        capital_allocation_pattern(
            100,
            -50,
            40
        )
        == "Growth Funded by Debt"
    )


def test_pattern_cash_accumulator():
    assert (
        capital_allocation_pattern(
            100,
            20,
            40
        )
        == "Cash Accumulator"
    )


def test_pattern_pre_revenue():
    assert (
        capital_allocation_pattern(
            -10,
            -20,
            -30
        )
        == "Pre-Revenue"
    )


def test_pattern_mixed():
    assert (
        capital_allocation_pattern(
            -10,
            -20,
            30
        )
        == "Mixed"
    )