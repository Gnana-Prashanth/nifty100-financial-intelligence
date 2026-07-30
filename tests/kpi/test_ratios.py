#============== Imports ================ 

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

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    opm_cross_check,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover
)


#============== Net Profit Margin ================ 

def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


#============ Operating Profit Margin ============

def test_operating_profit_margin_normal():
    assert operating_profit_margin(250, 1000) == 25.0


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(250, 0) is None


#============== OPM Cross Check ================== 

def test_opm_cross_check_false():
    assert opm_cross_check(25.0, 25.5) is False


def test_opm_cross_check_true():
    assert opm_cross_check(25.0, 27.5) is True


def test_opm_cross_check_none():
    assert opm_cross_check(None, 25.0) is False


#===================== ROE ======================

def test_return_on_equity_positive():
    assert return_on_equity(200, 100, 900) == 20.0


def test_return_on_equity_negative_equity():
    assert return_on_equity(200, 100, -100) is None


#==================== ROCE ======================

def test_roce_normal():
    assert return_on_capital_employed(300, 100, 600, 300) == 30.0


def test_roce_negative_capital():
    assert return_on_capital_employed(300, -100, -200, 0) is None


#===================== ROA ======================

def test_roa_normal():
    assert return_on_assets(150, 3000) == 5.0


def test_roa_zero_assets():
    assert return_on_assets(150, 0) is None


#================ Debt-to-Equity =================

def test_debt_to_equity_normal():
    assert debt_to_equity(500, 100, 900) == 0.5


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 100, 900) == 0


def test_debt_to_equity_negative_equity():
    assert debt_to_equity(500, 100, -100) is None


#=============== High Leverage Flag ===============

def test_high_leverage_true():
    assert high_leverage_flag(6, "Technology") is True


def test_high_leverage_financials():
    assert high_leverage_flag(6, "Financials") is False


def test_high_leverage_low_ratio():
    assert high_leverage_flag(3, "Technology") is False


def test_high_leverage_none():
    assert high_leverage_flag(None, "Technology") is False


#============= Interest Coverage Ratio ==============

def test_interest_coverage_normal():
    assert interest_coverage_ratio(400, 100, 50) == 10


def test_interest_coverage_zero_interest():
    assert interest_coverage_ratio(400, 100, 0) is None


#=================== ICR Label =======================

def test_icr_label_none():
    assert icr_label(None) == "Debt Free"


def test_icr_label_normal():
    assert icr_label(10) is None


#=================== ICR Warning ====================

def test_icr_warning_true():
    assert icr_warning_flag(1.2) is True


def test_icr_warning_false():
    assert icr_warning_flag(2.5) is False


def test_icr_warning_none():
    assert icr_warning_flag(None) is False


#=================== Net Debt ======================

def test_net_debt_positive():
    assert net_debt(500, 150) == 350


def test_net_debt_negative():
    assert net_debt(100, 150) == -50


#================= Asset Turnover ===================

def test_asset_turnover_normal():
    assert asset_turnover(1000, 500) == 2


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None