import re


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "REPLACE",
    "TRUNCATE",
    "ATTACH",
    "DETACH",
]


def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Validate that SQL is a single read-only query.
    """

    if not sql or not sql.strip():
        return False, "SQL query is empty."

    sql_clean = sql.strip()

    # Remove one trailing semicolon
    if sql_clean.endswith(";"):
        sql_clean = sql_clean[:-1].strip()

    # Reject multiple statements
    if ";" in sql_clean:
        return False, "Multiple SQL statements are not allowed."

    # Reject SQL comments
    if "--" in sql_clean or "/*" in sql_clean or "*/" in sql_clean:
        return False, "SQL comments are not allowed."

    sql_upper = sql_clean.upper()

    # Only SELECT or WITH queries are allowed
    if not (
        sql_upper.startswith("SELECT ")
        or sql_upper.startswith("SELECT\n")
        or sql_upper.startswith("WITH ")
        or sql_upper.startswith("WITH\n")
    ):
        return False, "Only SELECT/WITH queries are allowed."

    # Check dangerous keywords
    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, sql_upper):
            return False, f"Forbidden SQL operation detected: {keyword}"

    return True, "SQL is safe."


if __name__ == "__main__":

    test_queries = [

        # Safe
        "SELECT * FROM customers;",

        "SELECT name FROM customers WHERE city = 'Delhi';",

        """
        SELECT customers.name, SUM(orders.amount)
        FROM customers
        JOIN orders
        ON customers.id = orders.customer_id
        GROUP BY customers.id;
        """,

        # Unsafe
        "DELETE FROM customers;",

        "DROP TABLE customers;",

        "UPDATE customers SET city = 'Delhi';",

        "INSERT INTO customers VALUES (5, 'Test', 'test@test.com', 'Delhi');",

        # Multiple statements
        "SELECT * FROM customers; DELETE FROM customers;",

        # Comment injection
        "SELECT * FROM customers -- DELETE FROM customers",
    ]

    for query in test_queries:

        valid, message = validate_sql(query)

        print("\nSQL:")
        print(query)

        print("Valid:", valid)
        print("Message:", message)