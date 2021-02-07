# db_utils.py
import os
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'urls.db')


def create_url_table():
    creation_sql = """
            CREATE TABLE IF NOT EXISTS Url (
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 ORIGINAL TEXT NOT NULL,
                 EXPIRATION_DATE int NOT NULL)"""
    con = db_connect()
    cursor = con.cursor()
    with con:
        cursor.execute(creation_sql)


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con
