SQL_PLANNER = """
You are an expert data analyst.
Generate a valid SQL query for the user's question using the given schema.

Schema:
{schema}

Question:
{question}

Return ONLY the SQL query. Do not include ```sql or explanations.
"""

ANSWER_CRITIC = """
You are a data validator. Check if the SQL result answers the question correctly.

Question:
{question}

SQL Query:
{sql}

Top rows of result:
{results_head}

Respond with:
"is_valid": true/false
"feedback": reasoning
"""
