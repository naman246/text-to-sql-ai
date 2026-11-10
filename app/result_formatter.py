from app.llm import ask_llm


def format_result(question: str, sql: str, result: dict) -> str:
    """Convert database results into a natural-language answer."""

    if "error" in result:
        return f"I couldn't execute the query: {result['error']}"

    prompt = f"""
You are a helpful database assistant.

Answer the user's question using ONLY the database result provided.

USER QUESTION:
{question}

SQL QUERY:
{sql}

DATABASE RESULT:
Columns: {result["columns"]}
Rows: {result["rows"]}

Rules:
1. Give a concise natural-language answer.
2. Use only information present in the database result.
3. Do not invent facts.
4. If there are multiple results, summarize them clearly.
5. Use currency formatting when the value represents money.
6. Do not mention SQL or internal system details unless necessary.

Answer:
"""

    return ask_llm(prompt).strip()


if __name__ == "__main__":

    question = "Who are the top customers by total spending?"

    sql = """
    SELECT customers.name,
           SUM(orders.amount) AS total_spending
    FROM customers
    JOIN orders
        ON customers.id = orders.customer_id
    GROUP BY customers.id
    ORDER BY total_spending DESC;
    """

    result = {
        "columns": ["name", "total_spending"],
        "rows": [
            ("Neha Gupta", 5000.0),
            ("Aman Verma", 4700.0),
            ("Rahul Sharma", 4300.0),
            ("Priya Singh", 4200.0)
        ]
    }

    answer = format_result(question, sql, result)

    print("\nAI Answer:")
    print(answer)