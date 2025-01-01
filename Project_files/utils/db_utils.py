import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask import current_app, has_app_context

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


    # Call the function to reset the database
    reset_db()

