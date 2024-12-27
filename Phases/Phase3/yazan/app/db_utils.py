# app/db_utils.py
# noinspection PyUnresolvedReferences
from app import db

def get_db_connection():
    return db.engine.connect()