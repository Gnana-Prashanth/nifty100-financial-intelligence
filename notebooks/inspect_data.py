import pandas as pd
import os

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
]

for file in files:
    path = f"data/raw/{file}"

    df = pd.read_excel(path, header=1)

    print("\n")
    print(file,df.shape)
    print(df.columns.tolist())