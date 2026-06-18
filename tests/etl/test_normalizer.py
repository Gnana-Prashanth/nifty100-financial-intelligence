import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from src.etl.normalizer import normalize_ticker, normalize_year

print(normalize_ticker(" tcs "))
print(normalize_year("Mar 2014"))
print(normalize_year("Dec 2012"))
print(normalize_year("TTM"))



test_years = [
    "Dec 2012",
    "Mar 2014",
    "Mar-13",
    "Mar-14",
    "TTM"
]

for y in test_years:
    print(y, "-->", normalize_year(y))