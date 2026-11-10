from app.llm import ask_llm
from app.schema_inspector import get_schema


def generate_sql(question: str) -> str:
    """Convert a natural-language question into safe SQLite SQL."""

    schema = get_schema()

    prompt = f"""
You are an expert SQLite SQL generator.

Convert the user's natural-language question into ONE
valid SQLite SELECT query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

IMPORTANT RULES:

1. Return ONLY the SQL query.
2. Do not use markdown.
3. Do not explain the query.
4. Use ONLY tables and columns present in the schema.
5. Respect the foreign-key relationships shown in the schema.
6. Use JOIN when information from multiple tables is required.
7. Generate read-only SQL only.
8. Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
   REPLACE, or TRUNCATE.
9. Use SQLite-compatible syntax.
10. If the question asks for the highest/lowest/top result,
    use appropriate ORDER BY and LIMIT clauses.
11. If aggregation is required, use appropriate GROUP BY.
12. Never invent data, tables, or columns.

SQL:
"""

    sql = ask_llm(prompt).strip()

    # Remove accidental Markdown code fences
    if sql.startswith("```"):
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

    return sql


if __name__ == "__main__":

    questions = [
        "Show me all customers from Delhi.",
        "Who are the top customers by total spending?",
        "What is the total amount of all orders?"
    ]

    for question in questions:

        print("\n" + "=" * 60)
        print("Question:")
        print(question)

        sql = generate_sql(question)

        print("\nGenerated SQL:")
        print(sql)