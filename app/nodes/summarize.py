from .utils import call_llm

def summarize(state):
    if state.sql_result is not None:
        summary_prompt = f"Summarize these query results:\n{state.sql_result.head(5).to_markdown(index=False)}"
        state.summary = call_llm(summary_prompt)
    else:
        state.summary = "No results found."
    return state
