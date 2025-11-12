def validate_sql(state, con):
    sql = (state.sql_query or "").strip()
    if not sql:
        state.sql_valid = False
        return state

    disallowed = ["DROP", "DELETE", "UPDATE", "ALTER", "INSERT"]
    if any(word in sql.upper() for word in disallowed):
        state.sql_valid = False
        return state

    try:
        con.execute(f"EXPLAIN {sql}")
        state.sql_valid = True
    except Exception as e:
        state.sql_valid = False
        state.answer_feedback = f"SQL Error: {e}"
    return state
