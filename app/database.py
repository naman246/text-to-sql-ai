from pathlib import Path
import sqlite3


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database and SQL file locations
SQL_FILE = BASE_DIR / "data" / "database.sql"
DB_FILE = BASE_DIR / "data" / "app.db"


def create_database():
    """Create the SQLite database from database.sql."""

    # Connect to SQLite database
    connection = sqlite3.connect(DB_FILE)

    # Read SQL file
    sql_script = SQL_FILE.read_text(encoding="utf-8")

    # Execute all SQL commands
    connection.executescript(sql_script)

    connection.commit()
    connection.close()

    print(f"Database created successfully: {DB_FILE}")


if __name__ == "__main__":
    create_database()