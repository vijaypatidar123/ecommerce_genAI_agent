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

# import os
# import duckdb
# import streamlit as st
# import pandas as pd

# # -------------------------------
# # ✅ Resolve absolute DB path safely
# # -------------------------------
# # Find the repo root (one level up from this file)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # Default path for local + Streamlit
# DEFAULT_DB_PATH = os.path.join(BASE_DIR, "data", "ecom.duckdb")

# # Use Streamlit Secrets if available
# DB_PATH = st.secrets.get("DUCKDB_PATH", DEFAULT_DB_PATH)

# # -------------------------------
# # ✅ Connection Helper
# # -------------------------------
# def get_conn():
#     """Get a DuckDB connection, fallback to in-memory mode if DB not found."""
#     if not os.path.exists(DB_PATH):
#         st.warning(f"⚠️ DuckDB not found at {DB_PATH}. Using in-memory mode.")
#         return duckdb.connect(":memory:")

#     return duckdb.connect(DB_PATH, read_only=True)


# # -------------------------------
# # ✅ Optional: Bootstrap Demo Data (if DB is missing)
# # -------------------------------
# def bootstrap(con):
#     """Bootstrap tables from CSVs if DB doesn't exist."""
#     base_data_dir = os.path.join(BASE_DIR, "data")

#     if not os.path.exists(DB_PATH):
#         st.info("🧩 Bootstrapping DuckDB from CSV files...")

#         csv_files = {
#             "olist_orders": "olist_orders_dataset.csv",
#             "olist_order_items": "olist_order_items_dataset.csv",
#             "olist_products": "olist_products_dataset.csv",
#             "olist_customers": "olist_customers_dataset.csv",
#         }

#         for table_name, csv_file in csv_files.items():
#             csv_path = os.path.join(base_data_dir, csv_file)
#             if os.path.exists(csv_path):
#                 df = pd.read_csv(csv_path)
#                 con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df;")
#                 st.info(f"✅ Created table {table_name} from {csv_file}")
#             else:
#                 st.warning(f"⚠️ Missing CSV for table: {table_name}")


# # -------------------------------
# # ✅ Schema Inspection Helper
# # -------------------------------
# def list_schema(con):
#     """Return a DataFrame of all available tables."""
#     try:
#         tables = con.execute("SHOW TABLES").fetchdf()
#         return tables
#     except Exception as e:
#         st.error(f"Error loading schema: {e}")
#         return None

