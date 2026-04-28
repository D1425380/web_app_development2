import sqlite3
from datetime import datetime

class User:
    def __init__(self, id, username, email, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at

    @staticmethod
    def get_db_connection():
        # 假設資料庫路徑在 instance/database.db
        conn = sqlite3.connect('instance/database.db')
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, username, email):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (username, email)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        conn = cls.get_db_connection()
        users = conn.execute("SELECT * FROM users").fetchall()
        conn.close()
        return [dict(user) for user in users]

    @classmethod
    def get_by_id(cls, user_id):
        conn = cls.get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @classmethod
    def update(cls, user_id, username, email):
        conn = cls.get_db_connection()
        conn.execute(
            "UPDATE users SET username = ?, email = ? WHERE id = ?",
            (username, email, user_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, user_id):
        conn = cls.get_db_connection()
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
