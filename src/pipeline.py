"""Run the ETL pipeline.

Examples:
    python -m src.pipeline                              # latest rates
    python -m src.pipeline --date 2026-09-25            # one day
    python -m src.pipeline --start 2026-09-01 --end 2026-09-30   # backfill
"""
import argparse
import logging
from datetime import date, timedelta

from src.extract import fetch_rates
from src.load import load
from src.transform import transform

log = logging.getLogger("pipeline")


def run(day: str | None, db_path: str) -> int:
    raw = fetch_rates(day)
    df = transform(raw)
    count = load(df, db_path)
    log.info("Loaded %d rows for %s", count, day or "latest")
    return count


def daterange(start: str, end: str):
    d, last = date.fromisoformat(start), date.fromisoformat(end)
    while d <= last:
        yield d.isoformat()
        d += timedelta(days=1)


def main():
    parser = argparse.ArgumentParser(description="CBU exchange rate ETL")
    parser.add_argument("--date")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--db", default="data/rates.db")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.start and args.end:
        for day in daterange(args.start, args.end):
            try:
                run(day, args.db)
            except Exception as exc:  # keep going if one day fails
                log.error("Failed for %s: %s", day, exc)
    else:
        run(args.date, args.db)


if __name__ == "__main__":
    main()
