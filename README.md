# CBU Exchange Rate ETL Pipeline

An end-to-end ETL pipeline that downloads the official daily exchange rates of the
Central Bank of Uzbekistan (CBU), cleans them with pandas and stores them in a
SQLite database for SQL analysis.

## Architecture

```
CBU public JSON API  ->  extract.py  ->  transform.py  ->  load.py  ->  SQLite (rates.db)  ->  sql/analysis.sql
```

| Step | File | What it does |
|------|------|--------------|
| Extract | `src/extract.py` | Downloads raw JSON for the latest or a given date |
| Transform | `src/transform.py` | Renames columns, fixes types and dates, normalises rates to one unit, drops invalid rows and duplicates |
| Load | `src/load.py` | Idempotent upsert into SQLite (re-running never creates duplicates) |
| Orchestrate | `src/pipeline.py` | CLI with latest, single-day and date-range backfill modes, logging and per-day error handling |

## Tech Stack
Python, pandas, requests, SQL (SQLite), pytest, Git

## How to Run

```bash
git clone https://github.com/jasurbek-makhammadjonov/cbu-exchange-rate-etl
cd cbu-exchange-rate-etl
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m src.pipeline                                        # latest rates
python -m src.pipeline --start 2026-09-01 --end 2026-09-30    # backfill a month
python -m pytest                                              # run tests
```

Then explore the data with the queries in `sql/analysis.sql`
(monthly averages, day-over-day change with window functions, most volatile currencies).

## Results
[Add a screenshot of a query result or a chart here]

## What I Learned
- Designing a modular ETL pipeline and making the load step idempotent
- Data cleaning and type handling with pandas
- Window functions and aggregations in SQL
- Writing unit tests for data transformations

## Next Steps
- Schedule daily runs (cron or Airflow)
- Move storage to PostgreSQL with Docker
- Add a dashboard (Streamlit)
