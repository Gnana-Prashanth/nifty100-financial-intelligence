import sqlite3
import pandas as pd


conn = sqlite3.connect("nifty100.db")

audit = []


def load_table(
    file_path,
    table_name,
    duplicates=None,
    header=1
):

    print(f"\nLoading {table_name}...")

    df = pd.read_excel(
        file_path,
        header=header
    )

    before = len(df)

    if duplicates:
        df = df.drop_duplicates(
            subset=duplicates
        )

    after = len(df)

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    audit.append({
        "table_name": table_name,
        "rows_loaded": after
    })

    print(
        f"{table_name}: "
        f"{before} -> {after} rows loaded"
    )

    return after


load_table(
    "data/raw/companies.xlsx",
    "companies",
    header=1
)

load_table(
    "data/raw/profitandloss.xlsx",
    "profitandloss",
    header=1,
    duplicates=["company_id", "year"]
)

load_table(
    "data/raw/balancesheet.xlsx",
    "balancesheet",
    header=1,
    duplicates=["company_id", "year"]
)

load_table(
    "data/raw/cashflow.xlsx",
    "cashflow",
    header=1,
    duplicates=["company_id", "year"]
)

load_table(
    "data/raw/analysis.xlsx",
    "analysis",
    header=1
)

load_table(
    "data/raw/documents.xlsx",
    "documents",
    header=1
)

load_table(
    "data/raw/prosandcons.xlsx",
    "prosandcons",
    header=1
)

load_table(
    "data/supporting/sectors.xlsx",
    "sectors",
    header=0
)

load_table(
    "data/supporting/market_cap.xlsx",
    "market_cap",
    header=0
)

load_table(
    "data/supporting/peer_groups.xlsx",
    "peer_groups",
    header=0
)

load_table(
    "data/supporting/stock_prices.xlsx",
    "stock_prices",
    header=0
)

load_table(
    "data/supporting/financial_ratios.xlsx",
    "financial_ratios",
    header=0,
    duplicates=["company_id", "year"]
)


print(
    "\nAll tables loaded successfully! ✅"
)


audit_df = pd.DataFrame(audit)

audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

print("\nAudit report created!")

conn.close()


















''' #WE CAN ADD TABLES ONE BY ONE LIKE THIS INSTEAD OF COMPLEX `load_table` function code used above

import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

df.to_sql(
    "companies",
    conn,
    if_exists="append",
    index=False
)

print("Companies loaded! ✅")


pl = pd.read_excel(
    "data/raw/profitandloss.xlsx",
    header=1
)

pl = pl.drop_duplicates(
    subset=["company_id", "year"]
)

pl.to_sql(
    "profitandloss",
    conn,
    if_exists="append",
    index=False
)

print("profit and loss loaded! ✅")

conn.close()
'''