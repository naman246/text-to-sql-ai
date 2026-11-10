import sqlite3
from app.database import DB_FILE


def execute_query(sql: str):
    """Execute a SQL query and return column names + results."""

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    try:
        cursor.execute(sql)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        return {
            "columns": columns,
            "rows": rows
        }

    except sqlite3.Error as error:
        return {
            "error": str(error)
        }

    finally:
        connection.close()


if __name__ == "__main__":

    sql = """
SELECT
    customers.name,
    SUM(orders.amount) AS total_spending
FROM customers
JOIN orders
    ON customers.id = orders.customer_id
GROUP BY customers.id
ORDER BY total_spending DESC;
"""

    result = execute_query(sql)

    print(result)