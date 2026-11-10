import sqlite3
from app.database import DB_FILE


def get_schema():
    """Read tables, columns, and relationships from the database."""

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Get all tables
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%';
    """)

    tables = cursor.fetchall()

    schema = []

    for (table_name,) in tables:

        schema.append(f"Table: {table_name}")

        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for column in columns:
            column_name = column[1]
            data_type = column[2]
            is_primary_key = column[5]

            pk_text = " PRIMARY KEY" if is_primary_key else ""

            schema.append(
                f"  - {column_name} ({data_type}){pk_text}"
            )

        # Get foreign keys
        cursor.execute(
            f"PRAGMA foreign_key_list({table_name})"
        )

        foreign_keys = cursor.fetchall()

        for fk in foreign_keys:
            referenced_table = fk[2]
            column = fk[3]
            referenced_column = fk[4]

            schema.append(
                f"  - FOREIGN KEY: {column} "
                f"→ {referenced_table}.{referenced_column}"
            )

        schema.append("")

    connection.close()

    return "\n".join(schema)


if __name__ == "__main__":
    print(get_schema())