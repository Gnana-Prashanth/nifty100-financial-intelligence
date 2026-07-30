#================ Imports ====================

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


from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
    fcf_cagr
)


#=========== Normal CAGR ===========

def test_calculate_cagr_normal():

    value, flag = calculate_cagr(
        100,
        200,
        5,
        5
    )

    assert round(value,2) == 14.87
    assert flag is None


#========= Insufficient Years =========

def test_calculate_cagr_insufficient():

    value, flag = calculate_cagr(
        100,
        200,
        5,
        3
    )

    assert value is None
    assert flag == "INSUFFICIENT"


#=========== Zero Base ===============

def test_calculate_cagr_zero_base():

    value, flag = calculate_cagr(
        0,
        100,
        5,
        5
    )

    assert value is None
    assert flag == "ZERO_BASE"


#============ Decline to Loss ===============

def test_calculate_cagr_decline_to_loss():

    value, flag = calculate_cagr(
        100,
        -50,
        5,
        5
    )

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


#============== Turnaround ==================

def test_calculate_cagr_turnaround():

    value, flag = calculate_cagr(
        -100,
        50,
        5,
        5
    )

    assert value is None
    assert flag == "TURNAROUND"


#============ Both Negative =================

def test_calculate_cagr_both_negative():

    value, flag = calculate_cagr(
        -100,
        -50,
        5,
        5
    )

    assert value is None
    assert flag == "BOTH_NEGATIVE"


#========= Wrapper Functions ===========

def test_revenue_cagr():

    value, flag = revenue_cagr(
        100,
        200,
        5,
        5
    )

    assert round(value,2) == 14.87
    assert flag is None


def test_pat_cagr():

    value, flag = pat_cagr(
        100,
        200,
        5,
        5
    )

    assert round(value,2) == 14.87


def test_eps_cagr():

    value, flag = eps_cagr(
        100,
        200,
        5,
        5
    )

    assert round(value,2) == 14.87


def test_fcf_cagr():

    value, flag = fcf_cagr(
        100,
        200,
        5,
        5
    )

    assert round(value,2) == 14.87


#pytest tests/kpi -v