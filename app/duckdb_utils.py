import duckdb
import os
import streamlit as st
 

# DB_PATH = os.getenv("DUCKDB_PATH", "./data/ecom.duckdb")
DB_PATH = st.secrets.get("DUCKDB_PATH", "./ecom.duckdb")


def get_conn():
    return duckdb.connect(DB_PATH, read_only=False)

def bootstrap(con):
    # You can load CSVs here if needed
    pass

def list_schema(con):
    tables = con.execute("SHOW TABLES").fetchdf()
    return tables
