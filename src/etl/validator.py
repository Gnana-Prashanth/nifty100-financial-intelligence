#not in this file
import pandas as pd

df = pd.read_excel("data/raw/profitandloss.xlsx", header=1)

print("profitandloss")
dups = df[df.duplicated(
    subset=["company_id","year"],
    keep=False
)]

print(dups[["company_id","year"]].sort_values(
    ["company_id","year"]
))


print("Unique values", df["company_id"].nunique())

print("Null values",df.isnull().sum().sum())
print("\n")



df = pd.read_excel("data/raw/balancesheet.xlsx", header=1)

print("balancesheet")
dups = df[df.duplicated(
    subset=["company_id","year"],
    keep=False
)]

print(dups[["company_id","year"]].sort_values(
    ["company_id","year"]
))


print("Unique values", df["company_id"].nunique())

print("Null values",df.isnull().sum().sum())
print("\n")




df = pd.read_excel("data/raw/cashflow.xlsx", header=1)

print("cashflow")
dups = df[df.duplicated(
    subset=["company_id","year"],
    keep=False
)]

print(dups[["company_id","year"]].sort_values(
    ["company_id","year"]
))


print("Unique values", df["company_id"].nunique())

print("Null values",df.isnull().sum().sum())

