"""Run every query in sql/analysis.sql and print the results."""
import sqlite3
import pandas as pd

DB_PATH = "data/rates.db"
SQL_PATH = "sql/analysis.sql"


def main():
    with open(SQL_PATH, encoding="utf-8") as f:
        queries = [q.strip() for q in f.read().split(";") if q.strip()]

    with sqlite3.connect(DB_PATH) as conn:
        for i, query in enumerate(queries, start=1):
            print(f"\n=== Query {i} ===")
            print(pd.read_sql_query(query, conn).to_string(index=False))


if __name__ == "__main__":
    main()