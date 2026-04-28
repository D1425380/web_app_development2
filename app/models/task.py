import sqlite3
from datetime import datetime

class Task:
    def __init__(self, id, title, description, status, priority, due_date, assigned_to, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.assigned_to = assigned_to
        self.created_at = created_at

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect('instance/database.db')
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, title, description, priority='中', due_date=None, assigned_to=None):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO tasks (title, description, priority, due_date, assigned_to) 
                   VALUES (?, ?, ?, ?, ?)""",
                (title, description, priority, due_date, assigned_to)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        conn = cls.get_db_connection()
        # 關聯查詢使用者名稱
        query = """
            SELECT t.*, u.username as assignee_name 
            FROM tasks t 
            LEFT JOIN users u ON t.assigned_to = u.id
            ORDER BY t.created_at DESC
        """
        tasks = conn.execute(query).fetchall()
        conn.close()
        return [dict(task) for task in tasks]

    @classmethod
    def get_by_id(cls, task_id):
        conn = cls.get_db_connection()
        query = """
            SELECT t.*, u.username as assignee_name 
            FROM tasks t 
            LEFT JOIN users u ON t.assigned_to = u.id
            WHERE t.id = ?
        """
        task = conn.execute(query, (task_id,)).fetchone()
        conn.close()
        return dict(task) if task else None

    @classmethod
    def update(cls, task_id, title, description, status, priority, due_date, assigned_to):
        conn = cls.get_db_connection()
        conn.execute(
            """UPDATE tasks 
               SET title = ?, description = ?, status = ?, priority = ?, due_date = ?, assigned_to = ? 
               WHERE id = ?""",
            (title, description, status, priority, due_date, assigned_to, task_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def update_status(cls, task_id, status):
        conn = cls.get_db_connection()
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, task_id):
        conn = cls.get_db_connection()
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
