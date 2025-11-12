from langgraph.graph import StateGraph, END
from .duckdb_utils import get_conn, bootstrap, list_schema
from .state import GraphState
from .nodes.plan_sql import plan_sql
from .nodes.validate_sql import validate_sql
from .nodes.execute_sql import execute_sql
from .nodes.validate_answer import validate_answer
from .nodes.summarize import summarize
from .nodes.external_retrieval import external_retrieval
from app.chat_db import load_messages
import pandas as pd

con = get_conn()
bootstrap(con)
schema_df = list_schema(con)
schema_md = schema_df.to_markdown(index=False) if not schema_df.empty else "No tables found."

workflow = StateGraph(GraphState)

# ✅ Define nodes
workflow.add_node("plan_sql", lambda s: plan_sql(s))
workflow.add_node("validate_sql", lambda s: validate_sql(s, con))
workflow.add_node("execute_sql", lambda s: execute_sql(s, con))
workflow.add_node("validate_answer", validate_answer)
workflow.add_node("summarize", summarize)
workflow.add_node("external_retrieval", external_retrieval)

workflow.set_entry_point("plan_sql")

# ✅ Conditional edges
def on_sql_valid(s): 
    return "execute_sql" if s.sql_valid else "summarize"

def on_answer_valid(s): 
    return "summarize"

workflow.add_edge("plan_sql", "validate_sql")
workflow.add_conditional_edges("validate_sql", on_sql_valid, {"execute_sql": "execute_sql", "summarize": "summarize"})
workflow.add_edge("execute_sql", "validate_answer")
workflow.add_conditional_edges("validate_answer", on_answer_valid, {"summarize": "summarize"})
workflow.add_edge("summarize", "external_retrieval")
workflow.add_edge("external_retrieval", END)

# ✅ Proper compilation with recursion limit
graph = workflow.compile()


def run_graph(query: str, session_id: str = None):
    """
    Runs LangGraph workflow with chat context awareness.
    """
    # Load context (previous chat)
    context = ""
    if session_id:
        messages = load_messages(session_id)
        for role, msg in messages[-5:]:  # last 5 messages
            context += f"{role.upper()}: {msg}\n"

    # Merge context into query
    contextual_query = f"{context}\nUSER: {query}"

    state = GraphState(user_query=contextual_query, schema_md=schema_md)
    out = graph.invoke(state)

    if isinstance(out, dict):
        return out.get("summary") or out.get("external_info") or out.get("answer_feedback") or "No output."
    return getattr(out, "summary", "No output.")
