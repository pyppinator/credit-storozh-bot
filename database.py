import sqlite3
from datetime import datetime

DB_NAME = "credit_storozh.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            bank TEXT NOT NULL,
            product TEXT NOT NULL,
            last_rate TEXT,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            text TEXT NOT NULL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_subscription(user_id, username, bank, product, rate):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO subscriptions (user_id, username, bank, product, last_rate, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, username, bank, product, rate, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_user_subscriptions(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT bank, product, last_rate FROM subscriptions WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_user_subscriptions_with_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, bank, product, last_rate FROM subscriptions WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_subscription_by_id(sub_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM subscriptions WHERE id = ? AND user_id = ?", (sub_id, user_id))
    conn.commit()
    conn.close()

def add_request(user_id, username, text):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO requests (user_id, username, text, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, text, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# ============ НОВЫЕ ФУНКЦИИ ДЛЯ CHECKER ============

def get_unique_products():
    """Возвращает уникальные пары (банк, продукт) из всех подписок"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT bank, product FROM subscriptions")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_subscribers(bank, product):
    """Возвращает всех user_id, кто подписан на этот банк и продукт"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT user_id FROM subscriptions WHERE bank = ? AND product = ?",
        (bank, product)
    )
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]

def get_current_rate(bank, product):
    """Возвращает текущую ставку из базы для этой пары"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT last_rate FROM subscriptions WHERE bank = ? AND product = ? LIMIT 1",
        (bank, product)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def update_rate_for_all(bank, product, new_rate):
    """Обновляет ставку для ВСЕХ подписчиков этой пары"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "UPDATE subscriptions SET last_rate = ? WHERE bank = ? AND product = ?",
        (new_rate, bank, product)
    )
    conn.commit()
    conn.close()