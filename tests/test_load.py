import sqlite3
from src.load import load
from src.transform import transform
from tests.test_transform import SAMPLE


def test_load_is_idempotent(tmp_path):
    db = str(tmp_path / "t.db")
    df = transform(SAMPLE)
    load(df, db)
    load(df, db)  # second run must not create duplicates
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM exchange_rates").fetchone()[0] == 2
