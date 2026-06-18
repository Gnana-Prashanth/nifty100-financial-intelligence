import pandas as pd

files = {
    "profit and loss": "data/raw/profitandloss.xlsx",
    "balance sheet": "data/raw/balancesheet.xlsx",
    "cash flow": "data/raw/cashflow.xlsx"
}

for name,path in files.items():
    df = pd.read_excel(path,header=1)
    print("\n", name)
    print(df[["company_id", "year"]].head(3))
    print("-" * 40)


for name, path in files.items():
    df = pd.read_excel(path, header=1)    
    # Count duplicates based on company_id and year
    duplicates = df.duplicated(subset=["company_id", "year"]).sum()    
    print(f"\n{name}: {duplicates} duplicates")

    
