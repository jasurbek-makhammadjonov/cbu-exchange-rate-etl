"""Load: store clean rates in a SQLite database (idempotent upsert)."""
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE IF NOT EXISTS exchange_rates (
    rate_date     TEXT NOT NULL,
    currency      TEXT NOT NULL,
    currency_name TEXT,
    nominal       REAL NOT NULL,
    rate          REAL NOT NULL,
    diff          REAL,
    rate_per_unit REAL NOT NULL,
    PRIMARY KEY (rate_date, currency)
);
"""


def load(df: pd.DataFrame, db_path: str = "data/rates.db") -> int:
    """Insert or update rows. Safe to run many times for the same date."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(SCHEMA)
        rows = df[["rate_date", "currency", "currency_name", "nominal",
                   "rate", "diff", "rate_per_unit"]].values.tolist()
        conn.executemany(
            "INSERT OR REPLACE INTO exchange_rates VALUES (?, ?, ?, ?, ?, ?, ?)", rows
        )
    return len(rows)
