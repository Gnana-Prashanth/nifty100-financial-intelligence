def free_cash_flow(
        operating_activity,
        investing_activity
):
    """
    Free Cash Flow = CFO + CFI
    """
    return operating_activity + investing_activity



def cfo_quality_score(cfo, pat):
    """
    CFO Quality Score = CFO / PAT
    """
    if pat == 0:
        return None, None

    score = cfo / pat

    if score > 1:
        label = "High Quality"
    elif score >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"
    return round(score, 2), label



def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity = abs(CFI) / Sales × 100
    """

    if sales == 0:
        return None, None

    intensity = (abs(investing_activity) / sales) * 100

    if intensity < 3:
        label = "Asset Light"

    elif intensity <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(intensity, 2), label



def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion Rate = FCF / Operating Profit × 100
    """

    if operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)



def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    cfo_quality_label=None
):
    """
    Classify capital allocation pattern.
    """

    cfo_pos = cfo >= 0
    cfi_pos = cfi >= 0
    cff_pos = cff >= 0

    if cfo_pos and not cfi_pos and not cff_pos:
        if cfo_quality_label == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    elif cfo_pos and cfi_pos and not cff_pos:
        return "Liquidating Assets"

    elif not cfo_pos and cfi_pos and cff_pos:
        return "Distress Signal"

    elif cfo_pos and not cfi_pos and cff_pos:
        return "Growth Funded by Debt"

    elif cfo_pos and cfi_pos and cff_pos:
        return "Cash Accumulator"

    elif not cfo_pos and not cfi_pos and not cff_pos:
        return "Pre-Revenue"

    return "Mixed"