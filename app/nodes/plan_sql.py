from .utils import call_llm
from app.prompts import SQL_PLANNER

def plan_sql(state):
    prompt = SQL_PLANNER.format(
        schema=state.schema_md or "No schema available",
        question=state.user_query
    )
    sql = call_llm(prompt)
    state.sql_query = sql.strip().strip("```").replace("sql", "").strip()
    return state
