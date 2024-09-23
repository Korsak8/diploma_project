import sqlite3
from os.path import join, dirname, abspath

DB_FILE_PATH = join(dirname(abspath(__file__)), 'user_activity.db')

def get_database_connection():
    con = sqlite3.connect(DB_FILE_PATH)
    return con

def create_user_history_table():
    with get_database_connection() as con:
        try:
            cur = con.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS user_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                task_type TEXT NOT NULL,
                matrix TEXT NOT NULL,
                alpha_value REAL,
                c_value REAL,
                timestamp TEXT NOT NULL DEFAULT (datetime(current_timestamp, 'localtime'))
                )
            ''')
            con.commit()
        except sqlite3.Error as e:
            print(e)