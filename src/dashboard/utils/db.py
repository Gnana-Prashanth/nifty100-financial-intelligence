import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    query = """
    SELECT
        c.id,
        c.company_name,
        c.company_logo,
        s.broad_sector,
        s.sub_sector,
        s.market_cap_category
    FROM companies c
    LEFT JOIN sectors s
    ON c.id = s.company_id
    ORDER BY c.company_name
            """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    conn = get_connection()

    if year:
        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ? AND year = ?
        """
        df = pd.read_sql(query, conn, params=(ticker, year))
    else:
        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC
        """
        df = pd.read_sql(query, conn, params=(ticker,))

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_pl(ticker):
    conn = get_connection()

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id = ?
    ORDER BY year DESC
    """

    df = pd.read_sql(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_bs(ticker):
    conn = get_connection()

    query = """
    SELECT *
    FROM balancesheet
    WHERE company_id = ?
    ORDER BY year DESC
    """

    df = pd.read_sql(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_cf(ticker):
    conn = get_connection()

    query = """
    SELECT *
    FROM cashflow
    WHERE company_id = ?
    ORDER BY year DESC
    """

    df = pd.read_sql(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_sectors():
    conn = get_connection()

    query = """
    SELECT *
    FROM sectors
    ORDER BY broad_sector
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_peers(group_name):
    conn = get_connection()

    query = """
    SELECT *
    FROM peer_groups
    WHERE peer_group_name = ?
    """

    df = pd.read_sql(query, conn, params=(group_name,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_valuation(ticker):
    """
    Placeholder for Sprint 4 valuation module.
    """
    return pd.DataFrame()

@st.cache_data(ttl=600)
def get_all_ratios(year):
    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE year = ?
    """

    df = pd.read_sql(query, conn, params=(year,))
    conn.close()

    return df

@st.cache_data(ttl=600)
def get_pros_cons(company_id):
    conn = get_connection()

    query = """
    SELECT *
    FROM prosandcons
    WHERE company_id = ?
    """

    df = pd.read_sql_query(query, conn, params=(company_id,))
    conn.close()
    return df

@st.cache_data(ttl=600)
def get_screener():
    df = pd.read_csv("output/screener.csv")

    df = df.rename(columns={"year_x": "year"})

    df = (
        df.sort_values(["company_id", "year"])
          .drop_duplicates(subset=["company_id", "year"], keep="first")
    )

    df = df[df["year"] == "Mar 2024"]

    return df

@st.cache_data(ttl=600)
def get_peer_groups():
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM peer_groups",
        conn
    )

    conn.close()
    return df

@st.cache_data
def get_capital_allocation():
    return pd.read_csv("output/capital_allocation.csv")

@st.cache_data
def get_reports():
    return pd.read_sql(
        "SELECT * FROM documents",
        get_connection()
    )