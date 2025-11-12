def execute_sql(state, con):
    try:
        if not state.sql_query:
            raise ValueError("No SQL to execute.")
        df = con.execute(state.sql_query).fetchdf()
        state.sql_result = df
    except Exception as e:
        import pandas as pd
        state.sql_result = pd.DataFrame({"error": [str(e)]})
    return state
