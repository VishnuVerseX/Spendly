import sqlite3
from calendar import monthrange
from datetime import date
from pathlib import Path

from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"

CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()

    existing = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()
    if existing["count"] > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    today = date.today()
    _, days_in_month = monthrange(today.year, today.month)

    # (day-of-month, category, amount, description) — 8 rows covering all 7
    # categories; Food appears twice to reach 8.
    sample_expenses = [
        (2, "Food", 12.50, "Groceries"),
        (4, "Transport", 8.00, "Bus fare"),
        (7, "Bills", 65.00, "Electricity bill"),
        (10, "Health", 22.75, "Pharmacy"),
        (14, "Entertainment", 15.00, "Movie ticket"),
        (18, "Shopping", 40.20, "New shoes"),
        (23, "Food", 9.99, "Lunch out"),
        (27, "Other", 5.00, "Miscellaneous"),
    ]

    for day, category, amount, description in sample_expenses:
        expense_date = today.replace(day=min(day, days_in_month))
        conn.execute(
            """
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, expense_date.isoformat(), description),
        )

    conn.commit()
    conn.close()
