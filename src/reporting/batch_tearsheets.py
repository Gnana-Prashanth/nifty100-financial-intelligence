import pandas as pd
from pathlib import Path

from tearsheet import generate_tearsheet

BASE_DIR = Path(__file__).resolve().parents[2]

companies = pd.read_excel(
    BASE_DIR / "data/raw/companies.xlsx",
    header=1
)

ratios = pd.read_excel(
    BASE_DIR / "data/supporting/financial_ratios.xlsx"
)

company_ids = sorted(
    ratios["company_id"].unique()
)

tearsheet_dir = BASE_DIR / "reports" / "tearsheets"

tearsheet_dir.mkdir(
    parents=True,
    exist_ok=True
)

generated = 0
skipped = []

for company_id in company_ids:

    history = ratios[
        ratios["company_id"] == company_id
    ]

    if len(history) < 3:

        skipped.append({
            "company_id": company_id,
            "reason": "Less than 3 years of data"
        })

        continue

    try:

        generate_tearsheet(company_id)

        generated += 1

        print(f"Generated: {company_id}")

    except Exception as e:

        skipped.append({
            "company_id": company_id,
            "reason": str(e)
        })

skipped_df = pd.DataFrame(skipped)

skipped_df.to_csv(
    BASE_DIR / "output" / "skipped_tearsheets.csv",
    index=False
)

print("=" * 50)

print(f"Generated: {generated}")

print(f"Skipped : {len(skipped_df)}")


