from .utils import call_llm
from app.prompts import ANSWER_CRITIC

def validate_answer(state):
    df = state.sql_result
    head = df.head(10).to_markdown(index=False) if df is not None else "EMPTY"

    resp = call_llm(ANSWER_CRITIC.format(
        question=state.user_query,
        sql=state.sql_query,
        results_head=head
    ))

    state.answer_valid = '"is_valid": true' in resp.lower()
    state.answer_feedback = resp
    return state
