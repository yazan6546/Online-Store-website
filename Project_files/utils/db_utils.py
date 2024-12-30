from sqlalchemy import create_engine
from flask import current_app, has_app_context

# Default standalone engine for non-Flask apps
DEFAULT_DB_URI = 'mysql://root:osaid@localhost/Store'
standalone_engine = create_engine(DEFAULT_DB_URI)


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
        # Fall back to the standalone engine
        return standalone_engine.connect()

