import pandas as pd

def check_duplicates(df):
    
    duplicates = df.duplicated(subset=["company_id","year"]).sum()
    return duplicates



def foreign_key_check(
        child_df,
        parent_df,
        child_col = "company_id",
        parent_col = "id"
):
    child_ids = set(
        child_df[child_col].dropna().unique()
    )

    parent_ids = set(
        parent_df[parent_col].dropna().unique()
    )

    extra_ids = child_ids - parent_ids
    return sorted(extra_ids)



def null_value_check(df):
    nulls = df.isnull().sum()
    return nulls[nulls > 0]



def balance_sheet_check(df):

    failures = df[
        abs(df["total_assets"] - df["total_liabilities"])
        > (df["total_assets"] * 0.01)
    ]

    return len(failures)



def opm_check(df):

    temp = df.copy()

    temp["calculated_opm"] = (
        temp["operating_profit"]
        / temp["sales"]
    ) * 100

    failures = temp[
        abs(
            temp["calculated_opm"]
            - temp["opm_percentage"]
        ) > 1
    ]

    return failures



def positive_sales_check(df):

    failures = df[
        df["sales"] <= 0
    ]

    return len(failures)