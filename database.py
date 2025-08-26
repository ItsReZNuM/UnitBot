# database.py

import sqlite3
import logging
from config import DATABASE_FILE

logger = logging.getLogger(__name__)

def init_db():
    """جدول کاربران را در صورت عدم وجود ایجاد می‌کند."""
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT
                )
            ''')
            conn.commit()
            logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Database error on init: {e}")

def add_user(user_id, username, first_name):
    """یک کاربر جدید را به پایگاه داده اضافه می‌کند. اگر کاربر از قبل وجود داشته باشد، کاری انجام نمی‌دهد."""
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            # INSERT OR IGNORE از افزودن کاربر تکراری جلوگیری می‌کند
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name)
                VALUES (?, ?, ?)
            ''', (user_id, username if username else "ندارد", first_name))
            conn.commit()
            if cursor.rowcount > 0:
                logger.info(f"User {user_id} ({first_name}) added to the database.")
    except sqlite3.Error as e:
        logger.error(f"Failed to add user {user_id}: {e}")

def get_all_user_ids():
    """لیستی از تمام آیدی‌های کاربران را برای ارسال پیام همگانی برمی‌گرداند."""
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users")
            users = cursor.fetchall()
            # استخراج آیدی‌ها از لیست تاپل‌ها
            return [user[0] for user in users]
    except sqlite3.Error as e:
        logger.error(f"Failed to get all users: {e}")
        return []