from .database import get_database_connection
from .models import UserHistory

def insert_user_activity(activity: UserHistory):
    with get_database_connection() as con:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO user_history (description, task_type, matrix, alpha_value, c_value)
        VALUES(?,?,?,?,?)
        ''', (activity.description, activity.task_type, activity.matrix, activity.alpha_value, activity.c_value))
        con.commit()

def get_all_activities():
    with get_database_connection() as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM user_history')
        return cur.fetchall()

def delete_activity(activity_id: int):
    with get_database_connection() as con:
        cur = con.cursor()
        cur.execute('DELETE FROM user_history WHERE id = ?', (activity_id,))
        con.commit()
        return cur.rowcount

def add_activity_description(activity_description: str, activity_id: int):
    with get_database_connection() as con:
        cur = con.cursor()
        cur.execute('UPDATE user_history SET description=? WHERE id=?',(activity_description,activity_id))
        con.commit()