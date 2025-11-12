import duckdb
import os
from dotenv import load_dotenv
load_dotenv()

DB_PATH = os.getenv("DUCKDB_PATH", "./data/ecom.duckdb")

def get_conn():
    return duckdb.connect(DB_PATH, read_only=False)

def bootstrap(con):
    # You can load CSVs here if needed
    pass

def list_schema(con):
    tables = con.execute("SHOW TABLES").fetchdf()
    return tables
