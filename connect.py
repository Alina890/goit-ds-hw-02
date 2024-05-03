import sqlite3
from contextlib import contextmanager

database = "C:\\Users\\ruswh\\OneDrive\Рабочий стол\\CLI-bot\\SQLite.db"

@contextmanager
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(db_file)
    yield conn
    conn.rollback()
    conn.close()