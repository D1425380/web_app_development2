import sqlite3
import os
from flask import current_app

class User:
    """使用者模型，負責處理使用者資料的資料庫操作"""

    @staticmethod
    def get_db_connection():
        """取得資料庫連線"""
        db_path = current_app.config['DATABASE']
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, username, email):
        """新增一筆使用者記錄"""
        conn = cls.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (username, email)
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
        """取得所有使用者記錄"""
        conn = cls.get_db_connection()
        try:
            users = conn.execute("SELECT * FROM users").fetchall()
            return [dict(user) for user in users]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, user_id):
        """取得單筆使用者記錄"""
        conn = cls.get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def update(cls, user_id, data):
        """更新使用者記錄"""
        conn = cls.get_db_connection()
        try:
            conn.execute(
                "UPDATE users SET username = ?, email = ? WHERE id = ?",
                (data['username'], data['email'], user_id)
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
    def delete(cls, user_id):
        """刪除使用者記錄"""
        conn = cls.get_db_connection()
        try:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
