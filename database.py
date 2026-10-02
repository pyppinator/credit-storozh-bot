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

def check_subscription_exists(user_id, bank, product):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM subscriptions WHERE user_id = ? AND bank = ? AND product = ?",
        (user_id, bank, product)
    )
    count = cur.fetchone()[0]
    conn.close()
    return count > 0

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

def get_unique_products():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT bank, product FROM subscriptions")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_subscribers(bank, product):
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
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "UPDATE subscriptions SET last_rate = ? WHERE bank = ? AND product = ?",
        (new_rate, bank, product)
    )
    conn.commit()
    conn.close()

def get_all_subscriptions():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, username, bank, product, last_rate, created_at
        FROM subscriptions
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(DISTINCT user_id) FROM subscriptions")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM subscriptions")
    total_subs = cur.fetchone()[0]

    cur.execute("""
        SELECT bank, product, COUNT(*) as cnt
        FROM subscriptions
        GROUP BY bank, product
        ORDER BY cnt DESC
        LIMIT 5
    """)
    top_products = cur.fetchall()

    cur.execute("""
        SELECT bank, COUNT(*) as cnt
        FROM subscriptions
        GROUP BY bank
        ORDER BY cnt DESC
    """)
    bank_stats = cur.fetchall()

    cur.execute("SELECT MAX(created_at) FROM subscriptions")
    last_sub = cur.fetchone()[0]

    conn.close()
    return {
        "total_users": total_users,
        "total_subs": total_subs,
        "top_products": top_products,
        "bank_stats": bank_stats,
        "last_sub": last_sub
    }