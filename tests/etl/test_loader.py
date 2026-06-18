import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from src.etl.loader import load_excel

df = load_excel("data/raw/profitandloss.xlsx")

print(sorted(df["company_id"].unique()))