import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../"
        )
    )
)

from src.etl.loader import load_excel
from src.etl.validator import check_duplicates


pl = load_excel(
    "data/raw/profitandloss.xlsx"
)

bs = load_excel(
    "data/raw/balancesheet.xlsx"
)

cf = load_excel(
    "data/raw/cashflow.xlsx"
)

print("Duplicates")

print(
    "Profit and loss:",
    check_duplicates(pl)
)

print(
    "Balance Sheet:",
    check_duplicates(bs)
)

print(
    "Cash Flow:",
    check_duplicates(cf)
)


# Testing Foreign Keys

companies = load_excel(
    "data/raw/companies.xlsx"
)

from src.etl.validator import foreign_key_check

extra_ids = foreign_key_check(
    pl,
    companies
)

print(
    "\nExtra IDs in profit and loss:"
)

print(extra_ids)


#Null values check
from src.etl.validator import null_value_check
print("\nNULL VALUES")
print(null_value_check(pl))

#print(f"Null values in bs: {bs.isnull().sum().sum()}")
#print(f"Null values in cf:\n{cf.isnull().sum()}")

#balance sheet check
from src.etl.validator import balance_sheet_check

print(
    "\nBalance Sheet Failures:",
    balance_sheet_check(bs)
)


#opm check
from src.etl.validator import opm_check

failures = opm_check(pl)

print(failures[
    [
        "company_id",
        "year",
        "sales",
        "operating_profit",
        "opm_percentage",
        "calculated_opm"
    ]
].head(10))


#positive sales check
from src.etl.validator import positive_sales_check

print(
    "\nSales Failures:",
    positive_sales_check(pl)
)

sales_failures = pl[
    pl["sales"] <= 0
]

print(sales_failures[
    ["company_id", "year", "sales"]
])