import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.etl.loader import load_excel
from src.etl.normalizer import normalize_ticker, normalize_year

df = load_excel("data/raw/profitandloss.xlsx")

print("     profit and loss dataset dataset\n")
print("BEFORE")
print(df[["company_id","year"]].head())

df["company_id"] = df["company_id"].apply(normalize_ticker)
df["year"] = df["year"].apply(normalize_year)

print("\nAFTER")
print(df[["company_id","year"]].head())
print("-" * 40,"\n")



from src.etl.loader import load_excel
from src.etl.normalizer import normalize_ticker, normalize_year

df = load_excel("data/raw/balancesheet.xlsx")

print("     balance sheet dataset\n")
print("BEFORE")
print(df[["company_id","year"]].head())

df["company_id"] = df["company_id"].apply(normalize_ticker)
df["year"] = df["year"].apply(normalize_year)

print("\nAFTER")
print(df[["company_id","year"]].head())
print("-" * 40,"\n")



from src.etl.loader import load_excel
from src.etl.normalizer import normalize_ticker, normalize_year

df = load_excel("data/raw/cashflow.xlsx")

print("     Cashflow dataset\n")
print("BEFORE")
print(df[["company_id","year"]].head())

df["company_id"] = df["company_id"].apply(normalize_ticker)
df["year"] = df["year"].apply(normalize_year)

print("\nAFTER")
print(df[["company_id","year"]].head())
print("-" * 40,"\n")



from src.etl.loader import load_excel
from src.etl.normalizer import normalize_ticker, normalize_year

df = load_excel("data/raw/documents.xlsx")

print("     Documents dataset\n")
print("BEFORE")
print(df[["company_id","Year"]].head())

df["company_id"] = df["company_id"].apply(normalize_ticker)
df["Year"] = df["Year"].apply(normalize_year)

print("\nAFTER")
print(df[["company_id","Year"]].head())
print("-" * 40,"\n")
