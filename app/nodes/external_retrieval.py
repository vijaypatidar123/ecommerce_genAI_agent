def external_retrieval(state):
    if getattr(state, "needs_external", False):
        state.external_info = "No database result found; external retrieval would go here."
    else:
        state.external_info = "Query answered from local data."
    return state
