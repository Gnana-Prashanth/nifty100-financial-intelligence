import streamlit as st
import pandas as pd
import requests

from utils.db import *

st.title("📄 Annual Reports")

reports = get_reports()

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company,
    "id"
].iloc[0]

company_reports = reports[
    reports["company_id"] == company_id
].sort_values(
    "Year",
    ascending=False
)


st.subheader("Available Annual Reports")

if company_reports.empty:
    st.warning("No annual reports available.")

else:  

    for _, row in company_reports.iterrows():

        year = row["Year"]
        url = row["Annual_Report"]

        st.markdown(
    f"📄 **{year}** - [Open Annual Report]({url})"
)