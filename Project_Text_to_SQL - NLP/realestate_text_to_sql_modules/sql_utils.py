import sqlite3

def is_valid_sql(query: str, db_path: str = "data/processing/SQLite_real_estate.db") -> bool:
    """
    Check if a SQL query can be executed and returns non-empty results on the given database.

    Args:
        query (str): The SQL query to check.
        db_path (str): Path to the SQLite database.

    Returns:
        bool: True if the query executes successfully and returns rows; False otherwise.
    """
    try:
        conn = sqlite3.connect(db_path)
        rows = conn.execute(query).fetchall()
        conn.close()
        return len(rows) > 0
    except Exception:
        return False
