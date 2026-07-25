import re
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

analysis = pd.read_excel(BASE_DIR / "data" / "raw" / "analysis.xlsx",header=1)
ratios = pd.read_excel(BASE_DIR / "data" / "supporting" / "financial_ratios.xlsx")

pattern = re.compile(
    r"(\d+)\s*Years?.*?\s*([\d.]+)%" #Regex Pattern
)

metrics = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

parsed_rows = []
failed_rows = []


for _, row in analysis.iterrows():

    company_id = row["company_id"]

    for metric in metrics:

        if pd.isna(row[metric]):
            continue

        text = str(row[metric]).strip()

        match = pattern.search(text)

        if match:

            period = int(match.group(1))
            value = float(match.group(2))

            parsed_rows.append({
                "company_id": company_id,
                "metric_type": metric,
                "period_years": period,
                "value_pct": value
            })

        else:

            failed_rows.append({
                "company_id": company_id,
                "metric_type": metric,
                "raw_text": text
            })


parsed_df = pd.DataFrame(parsed_rows)
failed_df = pd.DataFrame(failed_rows)

parsed_df.to_csv(
    BASE_DIR / "output" / "analysis_parsed.csv",
    index=False
)

failed_df.to_csv(
    BASE_DIR / "output" / "parse_failures.csv",
    index=False
)

print(f"Parsed rows: {len(parsed_df)}")
print(f"Failed rows: {len(failed_df)}")


#------------------------------------------
#           Cross-Validation
#------------------------------------------

# ratios["year"] = (
#     ratios["year"]
#     .str.extract(r"(\d{4})")[0]
#     .astype(int)
# )

latest_ratios = (
    ratios.sort_values("year")
          .groupby("company_id")
          .tail(1)
)

sales = parsed_df[
    parsed_df["metric_type"] == "compounded_sales_growth"
]

sales = sales.merge(
    latest_ratios[
        [
            "company_id",
            "revenue_cagr_5yr"
        ]
    ],
    on="company_id",
    how="left"
)

sales["difference"] = (
    sales["value_pct"] -
    sales["revenue_cagr_5yr"]
).abs().round(2)

pat = parsed_df[
    parsed_df["metric_type"] == "compounded_profit_growth"
]

pat = pat.merge(
    latest_ratios[
        [
            "company_id",
            "pat_cagr_5yr"
        ]
    ],
    on="company_id",
    how="left"
)

pat["difference"] = (
    pat["value_pct"]
    - pat["pat_cagr_5yr"]
).abs().round(2)

roe = parsed_df[
    parsed_df["metric_type"] == "roe"
]

roe = roe.merge(
    latest_ratios[
        [
            "company_id",
            "return_on_equity_pct"
        ]
    ],
    on="company_id",
    how="left"
)

roe["difference"] = (
    roe["value_pct"]
    - roe["return_on_equity_pct"]
).abs().round(2)

comparison = pd.concat(
    [
        sales,
        pat,
        roe
    ],
    ignore_index=True
)

manual_review = comparison[
    comparison["difference"] > 5
]

manual_review.to_csv(
    BASE_DIR / "output" / "cagr_manual_review.csv",
    index=False
)

print(
    f"Manual review required: {len(manual_review)}"
)

print("Cross-validation completed.")