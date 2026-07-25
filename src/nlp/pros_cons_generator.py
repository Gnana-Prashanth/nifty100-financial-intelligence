import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ratios = pd.read_excel(
    BASE_DIR / "data" / "supporting" / "financial_ratios.xlsx"
)

companies = pd.read_excel(
    BASE_DIR / "data" / "raw" / "companies.xlsx",
    header=1
)

latest = (
    ratios.sort_values("year")
    .groupby("company_id")
    .tail(1)
    .reset_index(drop=True)
)

pros_cons = []

def company_history(company_id):
    return (
        ratios[ratios["company_id"] == company_id]
        .sort_values("year")
        .reset_index(drop=True)
    )

def increasing(series):
    return all(x < y for x, y in zip(series, series[1:]))

def decreasing(series):
    return all(x > y for x, y in zip(series, series[1:]))

def positive(series):
    return all(x > 0 for x in series)

def negative(series):
    return all(x < 0 for x in series)

def add_signal(company_id, signal_type, rule_id, text, confidence):

    pros_cons.append({
        "company_id": company_id,
        "type": signal_type,
        "rule_id": rule_id,
        "text": text,
        "confidence_pct": confidence
    })


for _, row in latest.iterrows():

    company_id = row["company_id"]

    # ----------------------------
    # PRO RULES
    # ----------------------------
    
    if row["return_on_equity_pct"] > 20: #Pro Rule 1 — ROE > 20%

        add_signal(
            company_id,
            "pro",
            "P01",
            "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
            95
        )

    if row["debt_to_equity"] == 0: #Pro Rule 3 — Debt Free

        add_signal(
            company_id,
            "pro",
            "P03",
            "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",
            90
        )

    if row["revenue_cagr_5yr"] > 15: #Pro Rule 4 — Revenue CAGR

        add_signal(
            company_id,
            "pro",
            "P04",
            "Revenue growing above 15% CAGR over five years reflects strong business momentum.",
            90
        )

    if row["operating_profit_margin_pct"] > 25: #Pro Rule 5 — Operating Margin

        add_signal(
            company_id,
            "pro",
            "P05",
            "Operating profit margin above 25% indicates strong pricing power and cost discipline.",
            85
        )

    if row["pat_cagr_5yr"] > 20: #Pro Rule 6 — PAT CAGR

        add_signal(
            company_id,
            "pro",
            "P06",
            "Net profit compounding above 20% over five years creates significant shareholder value.",
            90
        )

    if (                                 #Pro Rule 7 — Interest Coverage
        row["interest_coverage"] > 10
        or row["debt_to_equity"] == 0
    ):

        add_signal(
            company_id,
            "pro",
            "P07",
            "Very high interest coverage reflects negligible financial stress from debt servicing.",
            90
        )

    if row["eps_cagr_5yr"] > 15:  #Pro Rule 9 — EPS CAGR

        add_signal(
            company_id,
            "pro",
            "P09",
            "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding.",
            90
        )

    # ----------------------------
    # CON RULES
    # ----------------------------

    if row["debt_to_equity"] > 2:  #Con Rule 1 – High Debt

        add_signal(
            company_id,
            "con",
            "C01",
            f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} is elevated for a non-financial company and warrants monitoring.",
            90
        )

    if row["net_profit"] < 0:  #Con Rule 4 – Net Loss

        add_signal(
            company_id,
            "con",
            "C04",
            "Company reported a net loss in the most recent financial year.",
            95
        )

    if (                                    #Con Rule 6 – Low Interest Coverage
        pd.notna(row["interest_coverage"])
        and row["interest_coverage"] < 1.5
    ):

        add_signal(
            company_id,
            "con",
            "C06",
            "Interest coverage ratio below 1.5x indicates the company is at risk of not meeting its debt obligations.",
            95
        )

    if row["dividend_payout_ratio_pct"] > 100:  #Con Rule 7 – Unsustainable Dividend

        add_signal(
            company_id,
            "con",
            "C07",
            "Dividend payout ratio above 100% suggests dividends are being paid from reserves.",
            85
        )

    if row["return_on_capital_employed_pct"] < 10:  #Con Rule 10 - Low ROCE

        add_signal(
            company_id,
            "con",
            "C10",
            "Return on capital employed below 10% suggests poor capital efficiency.",
            85
        )

    if row["revenue_cagr_5yr"] < 5:  #Con Rule 12 – Weak Revenue Growth

        add_signal(
            company_id,
            "con",
            "C12",
            "Revenue growing below 5% CAGR over five years suggests limited business momentum.",
            85
        )

#P02 - Positive FCF for last 5 years
history = company_history(company_id)

if len(history) >= 5:

    if positive(history.tail(5)["free_cash_flow_cr"]):

        add_signal(
            company_id,
            "pro",
            "P02",
            "Free cash flow has remained positive for the last five years.",
            95
        )

#P10 – ROE improving for 3 years
if len(history) >= 3:

    if increasing(history.tail(3)["return_on_equity_pct"]):

        add_signal(
            company_id,
            "pro",
            "P10",
            "Return on equity has improved consistently over the last three years.",
            85
        )

#P11 – Revenue CAGR > PAT CAGR
if row["revenue_cagr_5yr"] > row["pat_cagr_5yr"]:

    add_signal(
        company_id,
        "pro",
        "P11",
        "Revenue is growing faster than profit, indicating future operating leverage potential.",
        75
    )

#P12 – Assets increasing while Debt decreasing
if len(history) >= 3:

    assets = history.tail(3)["total_assets"]
    debt = history.tail(3)["total_debt_cr"]

    if increasing(assets) and decreasing(debt):

        add_signal(
            company_id,
            "pro",
            "P12",
            "Assets are increasing while debt is reducing over time.",
            85
        )

#C02 – Negative FCF for 3 years
if len(history) >= 3:

    if negative(history.tail(3)["free_cash_flow_cr"]):

        add_signal(
            company_id,
            "con",
            "C02",
            "Free cash flow has remained negative for three consecutive years.",
            95
        )

#C03 – OPM declining
if len(history) >= 3:

    if decreasing(history.tail(3)["operating_profit_margin_pct"]):

        add_signal(
            company_id,
            "con",
            "C03",
            "Operating profit margin has declined consistently over the last three years.",
            85
        )

#C05 – Revenue declining
if len(history) >= 2:

    if decreasing(history.tail(2)["sales"]):

        add_signal(
            company_id,
            "con",
            "C05",
            "Revenue has declined for two consecutive years.",
            85
        )

#C08 – Debt increasing
if len(history) >= 3:

    if increasing(history.tail(3)["debt_to_equity"]):

        add_signal(
            company_id,
            "con",
            "C08",
            "Debt-to-equity ratio has increased over the last three years.",
            85
        )

#C09 – EPS declining
if len(history) >= 3:

    if decreasing(history.tail(3)["earnings_per_share"]):

        add_signal(
            company_id,
            "con",
            "C09",
            "Earnings per share has declined consistently over the last three years.",
            90
        )

# P08 skipped: dividend_yield column not available.
# C11 skipped: EBITDA not available.

pros_cons_df = pd.DataFrame(pros_cons)

pros_cons_df = pros_cons_df[
    pros_cons_df["confidence_pct"] > 60
]

pros_cons_df.to_csv(
    BASE_DIR / "output" / "pros_cons_generated.csv",
    index=False
)

print(f"Generated {len(pros_cons_df)} pros/cons signals.")