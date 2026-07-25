import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ratios = pd.read_excel(
    BASE_DIR / "data" / "supporting" / "financial_ratios.xlsx"
)

companies = pd.read_excel(
    BASE_DIR / "data" / "raw" / "companies.xlsx",
    header=1
)

sectors = pd.read_excel(
    BASE_DIR / "data" / "supporting" / "sectors.xlsx",
    header=0
)

capital = pd.read_csv(
    BASE_DIR / "output" / "capital_allocation.csv"
)

latest = (
    ratios.sort_values("year")
          .groupby("company_id")
          .tail(1)
          .reset_index(drop=True)
)

def history(company_id):
    return (
        ratios[ratios["company_id"] == company_id]
        .sort_values("year")
        .reset_index(drop=True)
    )

results = []


for _, row in latest.iterrows():

    company = row["company_id"]

    hist = history(company)

    cfo_quality = hist["cfo_pat_ratio"].dropna().mean()

    if cfo_quality > 1:
        cfo_label = "High Quality"

    elif cfo_quality >= 0.5:
        cfo_label = "Moderate"

    else:
        cfo_label = "Accrual Risk"


    if row["sales"] == 0:
        capex_pct = None
    else:
        capex_pct = abs(row["investing_activity"]) / row["sales"] * 100


    if capex_pct < 3:
        capex_label = "Asset Light"

    elif capex_pct <= 8:
        capex_label = "Moderate"

    else:
        capex_label = "Capital Intensive"


    distress_flag = (
        row["cash_from_operations_cr"] < 0
        and row["financing_activity"] > 0
    )

    if len(hist) >= 2:

        previous = hist.iloc[-2]

        deleveraging_flag = (
            row["financing_activity"] < 0
            and row["borrowings"] < previous["borrowings"]
        )

    else:

        deleveraging_flag = False


    results.append({
    "company_id": row["company_id"],
    "cfo_quality_score": round(cfo_quality, 2),
    "cfo_quality_label": cfo_label,
    "capex_intensity_pct": round(capex_pct, 2),
    "capex_label": capex_label,
    "fcf_cagr_5yr": row["fcf_cagr_5yr"],
    "fcf_conversion_pct": round(row["cfo_pat_ratio"] * 100, 2),
    "distress_flag": distress_flag,
    "deleveraging_flag": deleveraging_flag
    })


results_df = pd.DataFrame(results)

results_df = results_df.merge(
    sectors[
        [
            "company_id",
            "broad_sector"
        ]
    ],
    on="company_id",
    how="left"
)

results_df.rename(
    columns={
        "broad_sector": "sector"
    },
    inplace=True
)

capital = (
    capital[
        ["company_id", "pattern_label"]
    ]
    .drop_duplicates(subset="company_id")
)

results_df = results_df.merge(
    capital[
        [
            "company_id",
            "pattern_label"
        ]
    ],
    on="company_id",
    how="left"
)

results_df.rename(
    columns={
        "pattern_label": "capital_allocation_label"
    },
    inplace=True
)

results_df = results_df[
    [
        "company_id",
        "sector",
        "cfo_quality_score",
        "cfo_quality_label",
        "capex_intensity_pct",
        "capex_label",
        "fcf_cagr_5yr",
        "fcf_conversion_pct",
        "distress_flag",
        "deleveraging_flag",
        "capital_allocation_label",
    ]
]


results_df.to_excel(
    BASE_DIR / "output" / "cashflow_intelligence.xlsx",
    index=False
)

alerts = results_df[
    results_df["distress_flag"]
]

alerts = alerts.merge(
    latest[
        [
            "company_id",
            "cash_from_operations_cr",
            "financing_activity",
            "net_profit"
        ]
    ],
    on="company_id"
)

alerts.to_csv(
    BASE_DIR / "output" / "distress_alerts.csv",
    index=False
)

print(f"Cashflow intelligence generated: {len(results_df)} companies")
print(f"Distress alerts generated: {len(alerts)} companies")
