def cfo_pat_ratio(operating_activity, net_profit):
    """
    Calculate Cash From Operations / Net Profit

    Returns None when net profit is zero.
    """

    if net_profit == 0:
        return None

    return operating_activity / net_profit