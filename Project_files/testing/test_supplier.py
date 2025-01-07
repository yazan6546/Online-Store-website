from sqlalchemy import text

from utils.db_utils import get_db_connection

rows = [
    {"first_name": "Alice", "last_name": "Smith", "email": "alice123@example.com", "passcode": "password123"},
    {"first_name": "Bob", "last_name": "Johnson", "email": "bob123@example.com", "passcode": "password456"},
    {"first_name": "Charlie", "last_name": "Williams", "email": "charlie123@example.com", "passcode": "password789"},
]

# Raw SQL query with named placeholders
query = text("""
INSERT INTO Person (first_name, last_name, email, passcode)
VALUES (:first_name, :last_name, :email, :passcode)
""")
conn = get_db_connection()
# Execute the query with the list of dictionaries
conn.execute(query, rows)
conn.commit()

conn.close()