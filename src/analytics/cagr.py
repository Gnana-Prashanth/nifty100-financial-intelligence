def calculate_cagr(start_value, end_value, years, available_years):
    """
    Calculate CAGR with edge case handling.
    Returns:
        (cagr_value, flag)
    """

    # Less than required years
    if available_years < years:
        return None, "INSUFFICIENT"

    # Zero base
    if start_value == 0:
        return None, "ZERO_BASE"

    # Positive -> Negative
    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    # Negative -> Positive
    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    # Negative -> Negative
    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    # Normal CAGR
    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return round(cagr, 2), None



def revenue_cagr(start_revenue, end_revenue, years, available_years):
    """
    Calculate Revenue CAGR
    """
    return calculate_cagr(
        start_revenue,
        end_revenue,
        years,
        available_years
    )



def pat_cagr(start_pat, end_pat, years, available_years):
    """
    Calculate Profit After Tax (PAT) CAGR
    """
    return calculate_cagr(
        start_pat,
        end_pat,
        years,
        available_years
    )



def eps_cagr(start_eps, end_eps, years, available_years):
    """
    Calculate Earnings Per Share CAGR
    """
    return calculate_cagr(
        start_eps,
        end_eps,
        years,
        available_years
    )