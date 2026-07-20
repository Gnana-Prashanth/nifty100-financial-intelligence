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
    SELECT company_id, company_name, broad_sector, sector, sub_sector
    FROM companies
    ORDER BY company_name
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