import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

capital = pd.read_csv(
    BASE_DIR / "output" / "capital_allocation.csv"
)

capital["year_date"] = pd.to_datetime(
    capital["year"],
    format="%b %Y",
    errors="coerce"
)

latest = (
    capital
    .sort_values("year_date")
    .groupby("company_id")
    .tail(1)
    .reset_index(drop=True)
)

capital = capital.sort_values(
    ["company_id", "year_date"]
)

distribution = (
    latest["pattern_label"]
    .value_counts()
    .reset_index()
)

distribution.columns = [
    "capital_allocation_pattern",
    "company_count"
]

print(distribution)
print(distribution.shape)

distribution.to_csv(
    BASE_DIR / "output" / "capital_allocation_distribution.csv",
    index=False
)


changes = []

for company, group in capital.groupby("company_id"):

    group = group.reset_index(drop=True)

    for i in range(1, len(group)):

        previous = group.loc[i - 1]
        current = group.loc[i]

        if previous["pattern_label"] != current["pattern_label"]:

            changes.append({

                "company_id": company,

                "from_year": previous["year"],

                "to_year": current["year"],

                "previous_pattern": previous["pattern_label"],

                "current_pattern": current["pattern_label"]

            })

changes_df = pd.DataFrame(changes)

changes_df.to_csv(
    BASE_DIR / "output" / "pattern_changes.csv",
    index=False
)

print(
    f"Companies with pattern changes: {len(changes_df)}"
)