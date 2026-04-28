import sqlite3
from flask import current_app

class Task:
    """任務模型，負責處理任務資料的資料庫操作"""

    @staticmethod
    def get_db_connection():
        """取得資料庫連線"""
        db_path = current_app.config['DATABASE']
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, data):
        """新增一筆任務記錄"""
        conn = cls.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO tasks (title, description, priority, due_date, assigned_to) 
                   VALUES (?, ?, ?, ?, ?)""",
                (data['title'], data.get('description'), data.get('priority', '中'), 
                 data.get('due_date'), data.get('assigned_to'))
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        """取得所有任務記錄，並關聯使用者名稱"""
        conn = cls.get_db_connection()
        try:
            query = """
                SELECT t.*, u.username as assignee_name 
                FROM tasks t 
                LEFT JOIN users u ON t.assigned_to = u.id
                ORDER BY t.created_at DESC
            """
            tasks = conn.execute(query).fetchall()
            return [dict(task) for task in tasks]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, task_id):
        """取得單筆任務記錄"""
        conn = cls.get_db_connection()
        try:
            query = """
                SELECT t.*, u.username as assignee_name 
                FROM tasks t 
                LEFT JOIN users u ON t.assigned_to = u.id
                WHERE t.id = ?
            """
            task = conn.execute(query, (task_id,)).fetchone()
            return dict(task) if task else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def update(cls, task_id, data):
        """更新任務記錄"""
        conn = cls.get_db_connection()
        try:
            conn.execute(
                """UPDATE tasks 
                   SET title = ?, description = ?, status = ?, priority = ?, due_date = ?, assigned_to = ? 
                   WHERE id = ?""",
                (data['title'], data.get('description'), data.get('status'), 
                 data.get('priority'), data.get('due_date'), data.get('assigned_to'), task_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @classmethod
    def delete(cls, task_id):
        """刪除任務記錄"""
        conn = cls.get_db_connection()
        try:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
