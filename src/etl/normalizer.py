import pandas as pd

def normalize_ticker(value):
    if value is None:
        return None

    return str(value).strip().upper()




def normalize_year(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value.upper() == "TTM":
        return "TTM"

    try:
        if "-" in value and len(value.split("-")[1]) == 2:

            month, year = value.split("-")

            year = int(year)

            if year < 50:
                year += 2000
            else:
                year += 1900

            return f"{year}-{pd.to_datetime(month, format='%b').month:02d}"

        dt = pd.to_datetime(value)

        return dt.strftime("%Y-%m")

    except:
        return value