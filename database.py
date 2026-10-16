import sqlite3
import os
from datetime import datetime, timedelta

DB_FILE = "deals_history.db"

class Database:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posted_deals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    unique_key TEXT UNIQUE,
                    title TEXT,
                    price TEXT,
                    original_price TEXT,
                    discount INTEGER,
                    store TEXT,
                    product_url TEXT,
                    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def is_deal_posted(self, unique_key):
        """Returns True if the deal with unique_key was already posted."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM posted_deals WHERE unique_key = ?", (unique_key,))
            return cursor.fetchone() is not None

    def save_posted_deal(self, unique_key, title, price, original_price, discount, store, product_url):
        """Saves a posted deal to the database to prevent duplicate posting."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO posted_deals 
                    (unique_key, title, price, original_price, discount, store, product_url, posted_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    unique_key,
                    title,
                    str(price),
                    str(original_price),
                    int(discount) if str(discount).isdigit() else 0,
                    store,
                    product_url,
                    datetime.now().isoformat()
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB Error] Failed to save deal: {e}")
            return False

    def cleanup_old_deals(self, days=14):
        """Removes deals older than specified days to keep database lightweight."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posted_deals WHERE posted_at < ?", (cutoff,))
            conn.commit()
