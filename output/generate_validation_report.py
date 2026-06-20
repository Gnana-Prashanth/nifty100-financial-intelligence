import pandas as pd

validation_results = [

    ["DQ-01","CRITICAL","profitandloss",
     "Duplicate company-year records",13],

    ["DQ-01","CRITICAL","balancesheet",
     "Duplicate company-year records",87],

    ["DQ-01","CRITICAL","cashflow",
     "Duplicate company-year records",23],

    ["DQ-02","CRITICAL","profitandloss",
     "Foreign key violations",8],

    ["DQ-03","WARNING","profitandloss",
     "Null values",231],

    ["DQ-03","WARNING","cashflow",
     "Null values",8],

    ["DQ-04","WARNING","balancesheet",
     "Balance sheet mismatch",0],

    ["DQ-05","WARNING","profitandloss",
     "OPM mismatch",234],

    ["DQ-06","WARNING","profitandloss",
     "Non-positive sales",1]
]

report = pd.DataFrame(
    validation_results,
    columns=[
        "rule",
        "severity",
        "table",
        "description",
        "count"
    ]
)

report.to_csv(
    "output/validation_failures.csv",
    index=False
)

print(report)