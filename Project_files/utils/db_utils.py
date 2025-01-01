import os

from dotenv import load_dotenv
from flask import current_app, has_app_context
from sqlalchemy import create_engine, text

def get_db_connection():
    """
    Returns a database connection.

    Uses Flask app's SQLAlchemy engine if available. Otherwise, falls back
    to standalone SQLAlchemy engine for non-Flask usage.
    """
    if has_app_context() and "sqlalchemy" in current_app.extensions:
        # Correct way to get the SQLAlchemy engine
        engine = current_app.extensions["sqlalchemy"].get_engine()
        return engine.connect()
    else:
        DEFAULT_DB_URI = os.getenv('DATABASE_URL_TEST')

        if not DEFAULT_DB_URI:

            dir = os.path.abspath(os.path.dirname(__file__))
            dir = os.path.dirname(dir)
            load_dotenv(dotenv_path=os.path.join(dir, '.env'))
            DEFAULT_DB_URI = os.getenv('DATABASE_URL_TEST')
            # Fall back to the standalone engine

        standalone_engine = create_engine(DEFAULT_DB_URI)
        return standalone_engine.connect()



def reset_db():
    connection = get_db_connection()

    # Disable foreign key checks
    connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

    # Deleting all records from tables directly
    tables = [
        "Manager_Order_Line",
        "Manager_Order",
        "Customer_Order_Line",
        "Customer_Order",
        "Product",
        "Supplier",
        "Category",
        "Address",
        "Person"
    ]

    # Delete all records from each table
    for table in tables:
        connection.execute(text(f"DELETE FROM {table};"))

    # Reset auto-increment values for all tables
    for table in tables:
        connection.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1;"))

    # Enable foreign key checks
    connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    # Close the connection
    connection.close()


