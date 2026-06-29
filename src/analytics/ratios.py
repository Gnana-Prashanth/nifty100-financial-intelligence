#Net profit margin shows how much profit is earned after all expenses.
#This ratio tells us how much profit a company makes for every ₹1 (or $1) of sales. For example, a 20% margin means the company earns ₹0.20 in net profit for every ₹1 of revenue

def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = net_profit / sales * 100
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100



#operating_profit_margin() → Calculates the ratio from raw financial data.

def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin = operating_profit / sales * 100
    """
    
    if sales == 0:
        return None
    
    return (operating_profit / sales) * 100



#opm_cross_check() → Verifies whether our calculated value matches the value already present in the dataset, and flags differences greater than 1%.

def opm_cross_check(calculated_opm, source_opm):
    if calculated_opm is None or source_opm is None:
        return False
    return abs(calculated_opm - source_opm) > 1



#Return on Equity (ROE) tells us "For every ₹100 invested by shareholders, how much profit did the company earn?" 
# #It measures how efficiently a company uses shareholders' money.

def return_on_equity(net_profit, equity_capital, reserves):
    """
    ROE = Net Profit / (Equity Capital + Reserves) × 100
    """

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return (net_profit / total_equity) * 100



#Return on Capital Employed (ROCE) measures: "How efficiently is the company using all the capital invested in the business to generate profit?"  
#Unlike ROE (which considers only shareholders' money), ROCE also considers borrowed money.

def return_on_capital_employed(
    operating_profit,
    equity_capital,
    reserves,
    borrowings
):
    """
    ROCE = Operating Profit /
           (Equity + Reserves + Borrowings) × 100
    """

    capital_employed = (
        equity_capital +
        reserves +
        borrowings
    )

    if capital_employed <= 0:
        return None

    return (operating_profit / capital_employed) * 100



#Return on Assets (ROA) tells us: "How efficiently is the company using its total assets to generate profit?"
#Unlike ROE (shareholders' money) and ROCE (total capital), ROA considers all assets owned by the company.

def return_on_assets(net_profit, total_assets):
    """
    ROA = Net Profit / Total Assets × 100
    """

    if total_assets <= 0:
        return None

    return (net_profit / total_assets) * 100