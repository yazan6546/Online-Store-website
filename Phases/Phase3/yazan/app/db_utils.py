# app/db_utils.py
from app import db

def get_db_connection():
    return db.engine.connect()